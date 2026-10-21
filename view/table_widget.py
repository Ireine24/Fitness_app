import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QHeaderView, QAbstractItemView,
    QLabel, QSplitter, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from view.entry_form import EntryFormWidget
from model.workout_program import WORKOUT_PROGRAMS


class TableWidget(QWidget):
    set_item_changed = pyqtSignal(int, int, str)
    session_meta_changed = pyqtSignal(str, str, str)
    delete_set_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # 1. Indtastningsformular øverst
        self.entry_form = EntryFormWidget()
        layout.addWidget(self.entry_form)

        # 2. Splitter til tabellerne
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Træningspas oversigt
        top_container = QWidget()
        top_layout = QVBoxLayout(top_container)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_sessions = QLabel("Træningspas (Klik på et pas for at se alle løft):")
        lbl_sessions.setStyleSheet("font-weight: bold; font-size: 13px; color: #4CAF50;")
        top_layout.addWidget(lbl_sessions)

        self.table_sessions = QTableWidget()
        self.table_sessions.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_sessions.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_sessions.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        top_layout.addWidget(self.table_sessions)
        splitter.addWidget(top_container)

        # Detaljer / enkelte løft
        bottom_container = QWidget()
        bottom_layout = QVBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(0, 6, 0, 0)

        self.lbl_details = QLabel("Enkelte løft for det valgte pas (klik i cellerne for at rette):")
        self.lbl_details.setStyleSheet("font-weight: bold; font-size: 13px; color: #64B5F6;")
        bottom_layout.addWidget(self.lbl_details)

        self.table_details = QTableWidget()
        self.table_details.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_details.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_details.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked 
            | QAbstractItemView.EditTrigger.EditKeyPressed 
            | QAbstractItemView.EditTrigger.SelectedClicked
        )
        bottom_layout.addWidget(self.table_details)
        self.table_details.cellChanged.connect(self._on_cell_changed)

        # Slet-knap til enkelt sæt
        btn_del_set_layout = QHBoxLayout()
        btn_del_set_layout.addStretch()
        self.btn_delete_set = QPushButton("Slet valgt sæt / løft")
        self.btn_delete_set.setStyleSheet("background-color: #8E24AA; color: white; padding: 4px 10px; font-weight: bold; border-radius: 4px;")
        self.btn_delete_set.clicked.connect(self._on_delete_set_clicked)
        btn_del_set_layout.addWidget(self.btn_delete_set)
        bottom_layout.addLayout(btn_del_set_layout)

        splitter.addWidget(bottom_container)
        layout.addWidget(splitter, stretch=1)

        # Slet-knap til hele passet i bunden
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_delete = QPushButton("Slet valgt træningspas")
        self.btn_delete.setStyleSheet("background-color: #7a1f1d; color: white; padding: 6px 14px; font-weight: bold; border-radius: 4px;")
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        self._is_populating = False

    def _on_cell_changed(self, row: int, col: int):
        if self._is_populating:
            return
        item = self.table_details.item(row, col)
        if item:
            self.set_item_changed.emit(row, col, item.text())

    def _on_delete_set_clicked(self):
        selected_rows = self.table_details.selectionModel().selectedRows()
        if selected_rows:
            self.delete_set_signal.emit(selected_rows[0].row())

    def _get_traening_options(self, program_name: str) -> list[str]:
        options = ["-- Vælg træning --"]
        if program_name in WORKOUT_PROGRAMS:
            for dag, info in WORKOUT_PROGRAMS[program_name].items():
                options.append(f"{dag} ({info['title']})")
        else:
            for prog_dict in WORKOUT_PROGRAMS.values():
                for dag, info in prog_dict.items():
                    label = f"{dag} ({info['title']})"
                    if label not in options:
                        options.append(label)
        return options

    def populate_sessions(self, df_sessions: pd.DataFrame | None):
        self._is_populating = True
        self.table_sessions.clear()
        if df_sessions is None or df_sessions.empty:
            self.table_sessions.setRowCount(0)
            self.table_sessions.setColumnCount(0)
            self.table_details.clear()
            self.table_details.setRowCount(0)
            self._is_populating = False
            return

        cols = ["Dato", "Træningspas", "Træningsprogram", "Træning (Dag / Split)", "Sæt", "Total volumen (kg)", "Maks 1RM (kg)"]
        self.table_sessions.setColumnCount(len(cols))
        self.table_sessions.setHorizontalHeaderLabels(cols)
        self.table_sessions.setRowCount(len(df_sessions))

        program_options = ["-- Vælg program --"] + list(WORKOUT_PROGRAMS.keys())

        for row_idx, (_, row) in enumerate(df_sessions.iterrows()):
            dato_str = str(row["Dato"])
            pas_str = str(row["Træningspas"])
            saved_prog = str(row.get("Program", "") or "")
            saved_tr = str(row.get("Træning", "") or "")

            self.table_sessions.setItem(row_idx, 0, QTableWidgetItem(dato_str))
            self.table_sessions.setItem(row_idx, 1, QTableWidgetItem(pas_str))

            combo_prog = QComboBox()
            combo_prog.addItems(program_options)
            if saved_prog and saved_prog in program_options:
                combo_prog.setCurrentText(saved_prog)
            else:
                combo_prog.setCurrentIndex(0)

            combo_tr = QComboBox()
            tr_options = self._get_traening_options(saved_prog)
            combo_tr.addItems(tr_options)
            if saved_tr:
                if saved_tr not in tr_options:
                    combo_tr.addItem(saved_tr)
                combo_tr.setCurrentText(saved_tr)
            else:
                combo_tr.setCurrentIndex(0)

            combo_prog.currentTextChanged.connect(
                lambda text, r=row_idx, d=dato_str, cb_tr=combo_tr: self._on_row_program_changed(r, d, text, cb_tr)
            )
            combo_tr.currentTextChanged.connect(
                lambda text, r=row_idx, d=dato_str, cb_pr=combo_prog: self._on_row_traening_changed(r, d, cb_pr.currentText(), text)
            )

            self.table_sessions.setCellWidget(row_idx, 2, combo_prog)
            self.table_sessions.setCellWidget(row_idx, 3, combo_tr)

            self.table_sessions.setItem(row_idx, 4, QTableWidgetItem(str(row["Sæt"])))
            self.table_sessions.setItem(row_idx, 5, QTableWidgetItem(f"{float(row['Total volumen (kg)']):.1f} kg"))
            self.table_sessions.setItem(row_idx, 6, QTableWidgetItem(f"{float(row['Maks 1RM (kg)']):.1f} kg"))

        header = self.table_sessions.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        self._is_populating = False

        if len(df_sessions) > 0 and self.table_sessions.currentRow() < 0:
            self.table_sessions.selectRow(len(df_sessions) - 1)

    def _on_row_program_changed(self, row_idx: int, dato: str, new_prog: str, combo_tr: QComboBox):
        if self._is_populating:
            return
        self.table_sessions.selectRow(row_idx)
        clean_prog = "" if new_prog.startswith("--") else new_prog

        combo_tr.blockSignals(True)
        current_tr = combo_tr.currentText()
        combo_tr.clear()
        new_options = self._get_traening_options(clean_prog)
        combo_tr.addItems(new_options)
        if current_tr in new_options:
            combo_tr.setCurrentText(current_tr)
        else:
            combo_tr.setCurrentIndex(0)
        combo_tr.blockSignals(False)

        clean_tr = "" if combo_tr.currentText().startswith("--") else combo_tr.currentText()
        self.session_meta_changed.emit(dato, clean_prog, clean_tr)

    def _on_row_traening_changed(self, row_idx: int, dato: str, current_prog: str, new_tr: str):
        if self._is_populating:
            return
        self.table_sessions.selectRow(row_idx)
        clean_prog = "" if current_prog.startswith("--") else current_prog
        clean_tr = "" if new_tr.startswith("--") else new_tr
        self.session_meta_changed.emit(dato, clean_prog, clean_tr)

    def populate_session_details(self, df_details: pd.DataFrame | None, dato_str: str, session_navn: str = ""):
        self._is_populating = True
        self.table_details.clear()
        titel = f"{session_navn} ({dato_str})" if session_navn else dato_str
        self.lbl_details.setText(f"Enkelte løft for {titel} (Klik på en celle for at redigere):")
        
        if df_details is None or df_details.empty:
            self.table_details.setRowCount(0)
            self.table_details.setColumnCount(0)
            self._is_populating = False
            return

        cols = ["Øvelse", "Vægt (kg)", "Reps", "Estimeret 1RM (kg)", "Noter"]
        self.table_details.setColumnCount(len(cols))
        self.table_details.setHorizontalHeaderLabels(cols)
        self.table_details.setRowCount(len(df_details))

        for row_idx, (_, row) in enumerate(df_details.iterrows()):
            self.table_details.setItem(row_idx, 0, QTableWidgetItem(str(row.get("Øvelse", ""))))
            w_val = float(row.get("Vægt (kg)", 0))
            self.table_details.setItem(row_idx, 1, QTableWidgetItem(str(w_val)))
            r_val = int(row.get("Reps", 0))
            self.table_details.setItem(row_idx, 2, QTableWidgetItem(str(r_val)))
            
            est_val = float(row.get("Estimeret 1RM (kg)", 0.0))
            item_1rm = QTableWidgetItem(f"{est_val:.1f}")
            item_1rm.setFlags(item_1rm.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_details.setItem(row_idx, 3, item_1rm)
            
            self.table_details.setItem(row_idx, 4, QTableWidgetItem(str(row.get("Noter", ""))))

        header = self.table_details.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

        self._is_populating = False

    def get_selected_session_info(self) -> tuple[str | None, str | None]:
        selected_rows = self.table_sessions.selectionModel().selectedRows()
        if not selected_rows:
            return None, None
        row = selected_rows[0].row()
        item_date = self.table_sessions.item(row, 0)
        item_name = self.table_sessions.item(row, 1)
        dato = item_date.text() if item_date else None
        navn = item_name.text() if item_name else None

        combo_tr = self.table_sessions.cellWidget(row, 3)
        if isinstance(combo_tr, QComboBox):
            tr_text = combo_tr.currentText()
            if not tr_text.startswith("--"):
                navn = f"{navn} - {tr_text}"
        return dato, navn