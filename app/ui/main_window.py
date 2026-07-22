"""Main application window."""

import logging
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from app.constants import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH, WINDOW_TITLE
from app.exceptions import ApplicationError
from app.models.calculation_result import CalculationResult
from app.services.calculation_service import CalculationService
from app.services.export_service import ExportService
from app.services.history_service import HistoryService
from app.services.settings_service import SettingsService
from app.ui.cutting_view import CuttingView
from app.ui.dialogs import show_error, show_info
from app.ui.widgets import FieldEdit, MutedLabel, ReportView
from app.utils.formatting import format_dimensions, format_weight

LOGGER = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main PySide6 window composed from services and widgets."""

    def __init__(
        self,
        calculation_service: CalculationService,
        history_service: HistoryService,
        export_service: ExportService,
        settings_service: SettingsService,
    ) -> None:
        super().__init__()
        self._calculation_service = calculation_service
        self._history_service = history_service
        self._export_service = export_service
        self._settings_service = settings_service
        self._last_result: CalculationResult | None = None
        self._init_ui()
        self._load_settings()

    def _init_ui(self) -> None:
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self._create_widgets()
        self._create_layouts()
        self._create_toolbar()
        self._create_menu()
        self._connect_signals()
        self._apply_styles()

    def _create_widgets(self) -> None:
        self.width_edit = FieldEdit("например 55")
        self.length_edit = FieldEdit("300, 450 или 600")
        self.quantity_edit = FieldEdit("например 128")
        self.calculate_button = QPushButton("Рассчитать упаковку")
        self.demo_button = QPushButton("Пример")
        self.clear_button = QPushButton("Очистить")
        self.export_button = QPushButton("Экспорт CSV")
        self.report_view = ReportView()
        self.cutting_view = CuttingView()

    def _create_layouts(self) -> None:
        root = QWidget(self)
        root_layout = QHBoxLayout(root)
        form_layout = QVBoxLayout()
        report_layout = QVBoxLayout()
        self._add_form_rows(form_layout)
        self._add_buttons(form_layout)
        report_layout.addWidget(QLabel("Отчет по упаковке"))
        report_layout.addWidget(self.report_view)
        report_layout.addWidget(self.cutting_view)
        root_layout.addLayout(form_layout, 1)
        root_layout.addLayout(report_layout, 2)
        self.setCentralWidget(root)

    def _add_form_rows(self, layout: QVBoxLayout) -> None:
        layout.addWidget(QLabel("Параметры"))
        layout.addWidget(QLabel("Ширина рулона (мм)"))
        layout.addWidget(self.width_edit)
        layout.addWidget(QLabel("Намотка (м)"))
        layout.addWidget(self.length_edit)
        layout.addWidget(QLabel("Количество"))
        layout.addWidget(self.quantity_edit)
        layout.addWidget(MutedLabel("Поддерживается ввод с точкой или запятой."))
        layout.addStretch(1)

    def _add_buttons(self, layout: QVBoxLayout) -> None:
        row = QHBoxLayout()
        row.addWidget(self.calculate_button)
        row.addWidget(self.demo_button)
        row.addWidget(self.clear_button)
        layout.addLayout(row)
        layout.addWidget(self.export_button)

    def _create_toolbar(self) -> None:
        toolbar = QToolBar("Основные действия", self)
        toolbar.setMovable(False)
        toolbar.addAction("Рассчитать", self._on_calculate)
        toolbar.addAction("Очистить", self._on_clear)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    def _create_menu(self) -> None:
        file_menu = self.menuBar().addMenu("Файл")
        file_menu.addAction("Экспорт CSV", self._on_export)
        file_menu.addAction("Выход", self.close)

    def _connect_signals(self) -> None:
        self.calculate_button.clicked.connect(self._on_calculate)
        self.demo_button.clicked.connect(self._on_demo)
        self.clear_button.clicked.connect(self._on_clear)
        self.export_button.clicked.connect(self._on_export)
        self.quantity_edit.returnPressed.connect(self._on_calculate)

    def _load_settings(self) -> None:
        geometry = self._settings_service.geometry()
        if geometry is not None:
            self.restoreGeometry(geometry)
        width, length, quantity = self._settings_service.last_inputs()
        self.width_edit.setText(width)
        self.length_edit.setText(length)
        self.quantity_edit.setText(quantity)

    def _save_settings(self) -> None:
        self._settings_service.set_geometry(self.saveGeometry())
        self._settings_service.set_last_inputs(
            self.width_edit.text(),
            self.length_edit.text(),
            self.quantity_edit.text(),
        )

    def _on_calculate(self) -> None:
        try:
            result = self._calculation_service.calculate(
                self.width_edit.text(),
                self.length_edit.text(),
                self.quantity_edit.text(),
            )
            self._last_result = result
            self._history_service.record(result)
            self._render_report(result)
        except ApplicationError as exc:
            LOGGER.warning("Calculation failed: %s", exc)
            show_error(self, "Ошибка расчета", str(exc))

    def _on_demo(self) -> None:
        self.width_edit.setText("55")
        self.length_edit.setText("450")
        self.quantity_edit.setText("128")
        self._on_calculate()

    def _on_clear(self) -> None:
        self.width_edit.clear()
        self.length_edit.clear()
        self.quantity_edit.clear()
        self.report_view.clear()
        self._last_result = None
        self.width_edit.setFocus()

    def _on_export(self) -> None:
        if self._last_result is None:
            show_info(self, "Экспорт", "Сначала выполните расчет.")
            return
        path = self._choose_export_path()
        if path is None:
            return
        self._export_result(path)

    def _choose_export_path(self) -> Path | None:
        folder = self._settings_service.last_folder()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Экспорт CSV",
            str(folder / "packing_report.csv"),
            "CSV files (*.csv)",
        )
        return Path(file_name) if file_name else None

    def _export_result(self, path: Path) -> None:
        if self._last_result is None:
            show_info(self, "Экспорт", "Сначала выполните расчет.")
            return
        try:
            self._export_service.export_csv(self._last_result, path)
            self._settings_service.set_last_folder(path.parent)
            show_info(self, "Экспорт", "Отчет успешно экспортирован.")
        except ApplicationError as exc:
            LOGGER.exception("Export failed")
            show_error(self, "Ошибка экспорта", str(exc))

    def _render_report(self, result: CalculationResult) -> None:
        lines = [
            "СВОДКА УПАКОВКИ ГОТОВЫХ РУЛОНОВ",
            f"Параметры: ширина {result.width_mm:.0f} мм, "
            f"намотка {result.length_m:.0f} м, количество {result.quantity} шт.",
            "",
        ]
        for index, item in enumerate(result.boxes, start=1):
            box = item.box
            lines.append(
                f"{index:02d}. Коробка "
                f"{format_dimensions(box.width, box.length, box.height)} мм | "
                f"рулонов: {item.roll_count} | "
                f"вес брутто: {format_weight(item.gross_weight)}"
            )
        lines.extend(self._summary_lines(result))
        self.report_view.setPlainText("\n".join(lines))

    @staticmethod
    def _summary_lines(result: CalculationResult) -> list[str]:
        return [
            "",
            f"Итого коробок: {result.total_boxes}",
            f"Итого рулонов: {result.total_rolls}",
            f"Общий вес партии: {format_weight(result.total_weight)}",
        ]

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            "QMainWindow, QWidget { background: #050B1A; color: #D7E7FF; }"
            "QLineEdit, QTextEdit { background: #13233B; color: #D7E7FF; "
            "border: 1px solid #2B4E78; padding: 8px; }"
            "QPushButton { background: #68C96B; color: #04111F; "
            "border: 1px solid #2B4E78; padding: 8px; font-weight: 700; }"
            "#mutedLabel { color: #7B91B7; }"
        )

    def closeEvent(self, event: object) -> None:
        """Persist settings before closing."""
        self._save_settings()
        super().closeEvent(event)
