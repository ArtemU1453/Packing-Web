import tkinter as tk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from models import Roll
from packing_logic import pack_rolls
from visualization import (
    build_layer_animation_data,
    draw_layered_frame,
)


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("Промышленная система упаковки")
        self.root.geometry("1180x760")
        self.root.minsize(980, 640)
        self.root.configure(bg="#0F1114")

        self.layer_animation_state = None
        self.layer_after_id = None
        self.layer_canvas = None

        self._build_ui()

    def _build_ui(self):
        self.palette = {
            "bg": "#0F1114",
            "panel": "#171A1E",
            "panel_alt": "#1E2329",
            "text": "#E1E5EA",
            "muted": "#9AA3AD",
            "metal": "#B8C0C7",
            "accent": "#C39B64",
            "line": "#3A424B",
            "entry_bg": "#232A31",
        }
        header = tk.Frame(self.root, bg=self.palette["panel_alt"], height=86)
        header.pack(fill="x", padx=16, pady=(14, 10))
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="ПРОМЫШЛЕННЫЙ КОНТРОЛЬ УПАКОВКИ",
            fg=self.palette["metal"],
            bg=self.palette["panel_alt"],
            font=("Bahnschrift", 18, "bold"),
            anchor="w",
        )
        title.pack(fill="x", padx=16, pady=(12, 0))

        subtitle = tk.Label(
            header,
            text="Графитовый интерфейс | Анимация по слоям",
            fg=self.palette["muted"],
            bg=self.palette["panel_alt"],
            font=("Consolas", 10),
            anchor="w",
        )
        subtitle.pack(fill="x", padx=16, pady=(2, 0))

        body = tk.Frame(self.root, bg=self.palette["bg"])
        body.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        left = tk.Frame(body, bg=self.palette["panel"], width=330)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        right = tk.Frame(
            body,
            bg=self.palette["panel"],
            bd=1,
            highlightbackground=self.palette["line"],
            highlightthickness=1,
        )
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        self._build_inputs(left)
        self._build_output_and_visuals(right)

    def _build_inputs(self, parent):
        panel_title = tk.Label(
            parent,
            text="Параметры",
            bg=self.palette["panel"],
            fg=self.palette["metal"],
            font=("Bahnschrift", 14, "bold"),
        )
        panel_title.pack(anchor="w", padx=16, pady=(16, 12))

        fields = tk.Frame(parent, bg=self.palette["panel"])
        fields.pack(fill="x", padx=16)

        self.width_entry = self._labeled_entry(fields, "Ширина рулона (мм)", "50")
        self.length_entry = self._labeled_entry(fields, "Намотка (м)", "300")
        self.qty_entry = self._labeled_entry(fields, "Количество", "100")

        calc_btn = tk.Button(
            parent,
            text="Рассчитать упаковку",
            command=self.calculate,
            bg=self.palette["accent"],
            fg="#101317",
            activebackground="#D0AC7B",
            activeforeground="#101317",
            relief="flat",
            font=("Bahnschrift", 12, "bold"),
            cursor="hand2",
            padx=12,
            pady=8,
        )
        calc_btn.pack(fill="x", padx=16, pady=(18, 8))

        hint = tk.Label(
            parent,
            text="Анимация укладки отображается ниже, внутри этого окна.",
            wraplength=290,
            justify="left",
            bg=self.palette["panel"],
            fg=self.palette["muted"],
            font=("Consolas", 9),
        )
        hint.pack(anchor="w", padx=16, pady=(4, 0))

    def _labeled_entry(self, parent, label_text, default_value):
        label = tk.Label(
            parent,
            text=label_text,
            bg=self.palette["panel"],
            fg=self.palette["text"],
            font=("Bahnschrift", 11),
            anchor="w",
        )
        label.pack(fill="x", pady=(0, 5))

        entry = tk.Entry(
            parent,
            bg=self.palette["entry_bg"],
            fg=self.palette["metal"],
            insertbackground=self.palette["metal"],
            relief="flat",
            font=("Consolas", 11),
            highlightthickness=1,
            highlightbackground=self.palette["line"],
            highlightcolor=self.palette["accent"],
        )
        entry.pack(fill="x", ipady=7, pady=(0, 12))
        entry.insert(0, default_value)
        return entry

    def _build_output_and_visuals(self, parent):
        title = tk.Label(
            parent,
            text="Отчет по упаковке",
            bg=self.palette["panel"],
            fg=self.palette["metal"],
            font=("Bahnschrift", 14, "bold"),
            anchor="w",
        )
        title.pack(fill="x", padx=16, pady=(14, 8))

        self.output = tk.Text(
            parent,
            bg="#11161B",
            fg="#D4DBE2",
            insertbackground="#D4DBE2",
            relief="flat",
            font=("Consolas", 10),
            height=12,
            padx=12,
            pady=10,
            wrap="word",
        )
        self.output.pack(fill="x", padx=16, pady=(0, 10))

        self.output.tag_configure("header", foreground="#D8B07A", font=("Consolas", 10, "bold"))
        self.output.tag_configure("muted", foreground="#9AA3AD")

        visual_title = tk.Label(
            parent,
            text="Анимация укладки",
            bg=self.palette["panel"],
            fg=self.palette["metal"],
            font=("Bahnschrift", 12, "bold"),
            anchor="w",
        )
        visual_title.pack(fill="x", padx=16, pady=(2, 6))

        self.animation_tab = tk.Frame(
            parent,
            bg="#12171D",
            bd=1,
            highlightbackground=self.palette["line"],
            highlightthickness=1,
        )
        self.animation_tab.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def _parse_inputs(self):
        try:
            width = float(self.width_entry.get())
            length = float(self.length_entry.get())
            qty = int(self.qty_entry.get())
        except ValueError as exc:
            raise ValueError("Введите числовые значения ширины, намотки и количества.") from exc

        if width <= 0 or length <= 0 or qty <= 0:
            raise ValueError("Все значения должны быть больше нуля.")

        return width, length, qty

    def _reset_visuals(self):
        if self.layer_after_id is not None:
            self.root.after_cancel(self.layer_after_id)
            self.layer_after_id = None

        self.layer_animation_state = None

        for widget in self.animation_tab.winfo_children():
            widget.destroy()

        self.layer_canvas = None

    def _render_embedded_layer_animation(self, box, roll, quantity):
        positions, max_layer = build_layer_animation_data(box, roll, quantity)
        if not positions:
            tk.Label(
                self.animation_tab,
                text="Недостаточно данных для построения анимации укладки.",
                bg="#12171D",
                fg="#D4DBE2",
                font=("Consolas", 10),
            ).pack(padx=12, pady=12, anchor="w")
            return

        fig = Figure(figsize=(7.0, 4.8), dpi=100)
        ax = fig.add_subplot(111, projection="3d")

        canvas = FigureCanvasTkAgg(fig, master=self.animation_tab)
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.layer_canvas = canvas
        self.layer_animation_state = {
            "ax": ax,
            "box": box,
            "roll": roll,
            "positions": positions,
            "max_layer": max_layer,
            "current_layer": 0,
        }

        self._tick_layer_animation()

    def _tick_layer_animation(self):
        if not self.layer_animation_state or not self.layer_canvas:
            return

        state = self.layer_animation_state
        draw_layered_frame(
            state["ax"],
            state["box"],
            state["roll"],
            state["positions"],
            state["current_layer"],
            state["max_layer"],
        )
        self.layer_canvas.draw_idle()

        state["current_layer"] += 1
        if state["current_layer"] > state["max_layer"]:
            state["current_layer"] = 0

        self.layer_after_id = self.root.after(650, self._tick_layer_animation)

    def calculate(self):
        try:
            width, length, qty = self._parse_inputs()
            roll = Roll(width, length)
            result = pack_rolls(roll, qty)
            if not result:
                raise ValueError("Модуль упаковки вернул пустой результат.")
        except Exception as exc:
            messagebox.showerror("Ошибка расчета", str(exc))
            return

        self._reset_visuals()

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "СВОДКА УПАКОВКИ\n", "header")

        total_weight = 0.0

        for idx, (box, count) in enumerate(result, 1):
            box_weight = count * roll.weight() + box.weight
            total_weight += box_weight
            self.output.insert(
                tk.END,
                f"{idx:02d}. Коробка {box.width}x{box.length}x{box.height} мм | "
                f"рулонов: {count} | вес брутто: {box_weight:.2f} кг\n",
            )

        self.output.insert(tk.END, f"\nОбщий вес партии: {total_weight:.2f} кг\n", "muted")

        first_box, first_count = result[0]
        self._render_embedded_layer_animation(first_box, roll, first_count)

