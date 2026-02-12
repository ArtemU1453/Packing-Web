import tkinter as tk
from tkinter import messagebox
import math

from models import Roll
from packing_logic import pack_rolls


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор упаковки риббона")
        self.root.geometry("980x640")
        self.root.minsize(820, 560)
        self.root.configure(bg="#050B1A")

        self._build_ui()
        self.root.bind("<Return>", self.calculate)
        self.root.bind("<KP_Enter>", self.calculate)

    def _build_ui(self):
        self.palette = {
            "bg": "#050B1A",
            "panel": "#0C1629",
            "panel_alt": "#11233E",
            "panel_deep": "#091225",
            "text": "#D7E7FF",
            "muted": "#7B91B7",
            "metal": "#C6D8F6",
            "accent_gold": "#F1C65A",
            "accent_gold_active": "#FFD775",
            "accent_green": "#68C96B",
            "accent_green_active": "#7DDA80",
            "accent_cyan": "#3CB8D9",
            "accent_cyan_active": "#54CBE9",
            "line": "#2B4E78",
            "line_soft": "#1A3457",
            "entry_bg": "#13233B",
            "output_bg": "#0B1324",
            "output_text": "#D0DEFA",
        }

        self.bg_canvas = tk.Canvas(self.root, bd=0, highlightthickness=0, relief="flat")
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_canvas.bind("<Configure>", self._draw_background)

        ui_root = tk.Frame(self.root, bg=self.palette["bg"])
        ui_root.place(x=0, y=0, relwidth=1, relheight=1)

        header = tk.Frame(
            ui_root,
            bg=self.palette["panel_alt"],
            height=86,
            bd=0,
            highlightbackground=self.palette["line"],
            highlightthickness=1,
        )
        header.pack(fill="x", padx=16, pady=(14, 10))
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="РАСЧЕТ УПАКОВКИ",
            fg=self.palette["metal"],
            bg=self.palette["panel_alt"],
            font=("Bahnschrift", 18, "bold"),
            anchor="w",
        )
        title.pack(fill="x", padx=16, pady=(12, 0))

        subtitle = tk.Label(
            header,
            text="Ввод параметров и отчет по упаковке готовых рулонов",
            fg=self.palette["muted"],
            bg=self.palette["panel_alt"],
            font=("Consolas", 10),
            anchor="w",
        )
        subtitle.pack(fill="x", padx=16, pady=(2, 0))

        body = tk.Frame(ui_root, bg=self.palette["bg"])
        body.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        left = tk.Frame(
            body,
            bg=self.palette["panel"],
            width=330,
            bd=0,
            highlightbackground=self.palette["line_soft"],
            highlightthickness=1,
        )
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        right = tk.Frame(
            body,
            bg=self.palette["panel"],
            bd=0,
            highlightbackground=self.palette["line_soft"],
            highlightthickness=1,
        )
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        self._build_inputs(left)
        self._build_output(right)

    @staticmethod
    def _mix_hex(start_color, end_color, ratio):
        ratio = max(0.0, min(1.0, ratio))
        start_rgb = [int(start_color[i : i + 2], 16) for i in (1, 3, 5)]
        end_rgb = [int(end_color[i : i + 2], 16) for i in (1, 3, 5)]
        mixed = [
            int(start_rgb[index] + (end_rgb[index] - start_rgb[index]) * ratio)
            for index in range(3)
        ]
        return f"#{mixed[0]:02X}{mixed[1]:02X}{mixed[2]:02X}"

    def _draw_background(self, event=None):
        width = self.bg_canvas.winfo_width()
        height = self.bg_canvas.winfo_height()
        if width <= 1 or height <= 1:
            return

        self.bg_canvas.delete("all")

        top_color = "#020814"
        bottom_color = "#0B1A32"
        for y in range(height):
            mix = y / max(height - 1, 1)
            line_color = self._mix_hex(top_color, bottom_color, mix)
            self.bg_canvas.create_line(0, y, width, y, fill=line_color)

        glow_y_top = min(96, int(height * 0.15))
        glow_y_bottom = max(height - 70, int(height * 0.9))
        self.bg_canvas.create_line(0, glow_y_top, width, glow_y_top, fill="#2B5D92", width=2)
        self.bg_canvas.create_line(0, glow_y_bottom, width, glow_y_bottom, fill="#2B5D92", width=2)

        # Subtle industrial texture without external assets.
        for y in range(0, height, 10):
            row_offset = (y * 5) % 17
            for x in range(row_offset, width, 17):
                if (x + y) % 31 == 0:
                    self.bg_canvas.create_rectangle(
                        x,
                        y,
                        x + 1,
                        y + 1,
                        fill="#17355C",
                        outline="",
                    )

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

        self.width_entry = self._labeled_entry(fields, "Ширина рулона (мм)", " ")
        self.length_entry = self._labeled_entry(fields, "Намотка (м)", " ")
        self.qty_entry = self._labeled_entry(fields, "Количество", " ")

        buttons = tk.Frame(parent, bg=self.palette["panel"])
        buttons.pack(fill="x", padx=16, pady=(18, 8))

        calc_btn = tk.Button(
            buttons,
            text="Рассчитать упаковку",
            command=self.calculate,
            bg=self.palette["accent_green"],
            fg="#04111F",
            activebackground=self.palette["accent_green_active"],
            activeforeground="#04111F",
            relief="flat",
            font=("Bahnschrift", 12, "bold"),
            cursor="hand2",
            padx=12,
            pady=8,
            highlightthickness=1,
            highlightbackground=self.palette["line"],
        )
        calc_btn.pack(side="left", fill="x", expand=True)

        clear_btn = tk.Button(
            buttons,
            text="Очистить",
            command=self.clear_inputs,
            bg=self.palette["accent_gold"],
            fg="#1A1D24",
            activebackground=self.palette["accent_gold_active"],
            activeforeground="#1A1D24",
            relief="flat",
            font=("Bahnschrift", 11, "bold"),
            cursor="hand2",
            padx=12,
            pady=8,
            highlightthickness=1,
            highlightbackground=self.palette["line"],
        )
        clear_btn.pack(side="left", padx=(10, 0))

        hint = tk.Label(
            parent,
            text="После расчета справа формируется отчет по коробкам и весу партии.",
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
            highlightcolor=self.palette["accent_cyan"],
        )
        entry.pack(fill="x", ipady=7, pady=(0, 12))
        entry.insert(0, default_value)
        return entry

    def _build_output(self, parent):
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
            bg=self.palette["output_bg"],
            fg=self.palette["output_text"],
            insertbackground=self.palette["output_text"],
            relief="flat",
            font=("Consolas", 10),
            padx=12,
            pady=10,
            wrap="word",
            highlightthickness=1,
            highlightbackground=self.palette["line"],
            selectbackground="#1A3A66",
            selectforeground=self.palette["text"],
        )
        self.output.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.output.tag_configure("header", foreground=self.palette["accent_gold"], font=("Consolas", 10, "bold"))
        self.output.tag_configure("muted", foreground=self.palette["muted"])

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

    def clear_inputs(self):
        self.width_entry.delete(0, tk.END)
        self.length_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)

    def calculate(self, event=None):
        try:
            width, length, qty = self._parse_inputs()
            roll = Roll(width, length)
            result = pack_rolls(roll, qty)
            if not result:
                raise ValueError("Модуль упаковки вернул пустой результат.")
        except Exception as exc:
            messagebox.showerror("Ошибка расчета", str(exc))
            if event is not None:
                return "break"
            return

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "СВОДКА УПАКОВКИ ГОТОВЫХ РУЛОНОВ\n", "header")
        self.output.insert(
            tk.END,
            (
                f"Параметры: ширина {width:.0f} мм, намотка {length:.0f} м, "
                f"количество {qty} шт.\n\n"
            ),
            "muted",
        )

        total_weight = 0.0
        total_rolls = 0

        for idx, (box, count) in enumerate(result, 1):
            box_weight = count * roll.weight() + box.weight
            total_weight += box_weight
            total_rolls += count
            box_weight_report = math.ceil(box_weight * 10) / 10
            self.output.insert(
                tk.END,
                f"{idx:02d}. Коробка {box.width}x{box.length}x{box.height} мм | "
                f"рулонов: {count} | вес брутто: {box_weight_report:.1f} кг\n",
            )

        total_weight_report = math.ceil(total_weight * 10) / 10

        self.output.insert(
            tk.END,
            (
                f"\nИтого коробок: {len(result)}\n"
                f"Итого рулонов: {total_rolls}\n"
                f"Общий вес партии: {total_weight_report:.1f} кг\n"
            ),
            "muted",
        )

        if event is not None:
            return "break"
