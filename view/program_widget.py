from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QScrollArea, QFrame, QPushButton, QDialog, QLineEdit,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialogButtonBox, QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from model.workout_program import WORKOUT_PROGRAMS, save_programs

class ProgramEditorDialog(QDialog):
    def __init__(self, program_name="", program_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rediger Træningsprogram")
        self.resize(700, 550)
        self.program_data = program_data or {}
        
        layout = QVBoxLayout(self)
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Program Navn:"))
        self.input_name = QLineEdit(program_name)
        name_layout.addWidget(self.input_name)
        layout.addLayout(name_layout)
        
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        day_btn_layout = QHBoxLayout()
        btn_add_day = QPushButton("+ Tilføj Dag")
        btn_add_day.clicked.connect(self._add_day)
        btn_del_day = QPushButton("- Slet Valgt Dag")
        btn_del_day.clicked.connect(self._del_day)
        day_btn_layout.addWidget(btn_add_day)
        day_btn_layout.addWidget(btn_del_day)
        day_btn_layout.addStretch()
        layout.addLayout(day_btn_layout)
        
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
        
        self._load_data()
        
    def _load_data(self):
        for day, info in self.program_data.items():
            self._create_day_tab(day, info)
            
    def _create_day_tab(self, day_name: str, info: dict):
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Titel:"))
        title_edit = QLineEdit(info.get("title", ""))
        h_layout.addWidget(title_edit)
        
        h_layout.addWidget(QLabel("Ekstra info:"))
        extra_edit = QLineEdit(info.get("extra", ""))
        h_layout.addWidget(extra_edit)
        tab_layout.addLayout(h_layout)
        
        table = QTableWidget(0, 2)
        table.setHorizontalHeaderLabels(["Øvelse", "Sæt × Reps"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for ex in info.get("exercises", []):
            if len(ex) >= 2:
                r = table.rowCount()
                table.insertRow(r)
                table.setItem(r, 0, QTableWidgetItem(ex[0]))
                table.setItem(r, 1, QTableWidgetItem(ex[1]))
            
        tab_layout.addWidget(table)
        
        tb_btn_layout = QHBoxLayout()
        btn_add_ex = QPushButton("Tilføj Øvelse")
        btn_add_ex.clicked.connect(lambda: table.insertRow(table.rowCount()))
        btn_del_ex = QPushButton("Slet Valgt Øvelse")
        btn_del_ex.clicked.connect(lambda: table.removeRow(table.currentRow()) if table.currentRow() >= 0 else None)
        tb_btn_layout.addWidget(btn_add_ex)
        tb_btn_layout.addWidget(btn_del_ex)
        tb_btn_layout.addStretch()
        tab_layout.addLayout(tb_btn_layout)
        
        tab.title_edit = title_edit
        tab.extra_edit = extra_edit
        tab.table = table
        
        self.tabs.addTab(tab, day_name)
        
    def _add_day(self):
        day_name, ok = QInputDialog.getText(self, "Ny Dag", "Indtast ugedag (f.eks. Mandag):")
        if ok and day_name:
            self._create_day_tab(day_name, {"title": "", "extra": "", "exercises": []})
            
    def _del_day(self):
        idx = self.tabs.currentIndex()
        if idx >= 0:
            self.tabs.removeTab(idx)
            
    def get_program_data(self) -> tuple[str, dict]:
        name = self.input_name.text().strip()
        data = {}
        for i in range(self.tabs.count()):
            day_name = self.tabs.tabText(i)
            tab = self.tabs.widget(i)
            title = tab.title_edit.text().strip()
            extra = tab.extra_edit.text().strip()
            
            exercises = []
            for r in range(tab.table.rowCount()):
                ex_item = tab.table.item(r, 0)
                rep_item = tab.table.item(r, 1)
                if ex_item and ex_item.text().strip():
                    ex_text = ex_item.text().strip()
                    rep_text = rep_item.text().strip() if rep_item else ""
                    exercises.append((ex_text, rep_text))
                    
            data[day_name] = {
                "title": title,
                "extra": extra,
                "exercises": exercises
            }
        return name, data


class ProgramWidget(QWidget):
    programs_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        top_layout = QHBoxLayout()
        lbl_select = QLabel("Vælg træningsprogram:")
        lbl_select.setStyleSheet("font-weight: bold; color: #4CAF50;")
        top_layout.addWidget(lbl_select)

        self.combo_programs = QComboBox()
        self.combo_programs.addItems(list(WORKOUT_PROGRAMS.keys()))
        self.combo_programs.currentTextChanged.connect(self.display_program)
        top_layout.addWidget(self.combo_programs)

        self.btn_add = QPushButton("Tilføj Nyt")
        self.btn_add.setStyleSheet("background-color: #2E7D32; color: white; font-weight: bold; border-radius: 4px; padding: 5px 12px;")
        self.btn_add.clicked.connect(self._add_program)
        top_layout.addWidget(self.btn_add)

        self.btn_edit = QPushButton("Rediger")
        self.btn_edit.setStyleSheet("background-color: #1565C0; color: white; font-weight: bold; border-radius: 4px; padding: 5px 12px;")
        self.btn_edit.clicked.connect(self._edit_program)
        top_layout.addWidget(self.btn_edit)

        self.btn_del = QPushButton("Slet")
        self.btn_del.setStyleSheet("background-color: #7a1f1d; color: white; font-weight: bold; border-radius: 4px; padding: 5px 12px;")
        self.btn_del.clicked.connect(self._delete_program)
        top_layout.addWidget(self.btn_del)

        top_layout.addStretch()
        layout.addLayout(top_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        self.container = QWidget()
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.scroll_area.setWidget(self.container)
        
        layout.addWidget(self.scroll_area, stretch=1)

        if WORKOUT_PROGRAMS:
            self.display_program(self.combo_programs.currentText())

    def _add_program(self):
        dialog = ProgramEditorDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, data = dialog.get_program_data()
            if name:
                WORKOUT_PROGRAMS[name] = data
                save_programs(WORKOUT_PROGRAMS)
                self._refresh_combobox(name)
                self.programs_changed.emit()

    def _edit_program(self):
        prog_name = self.combo_programs.currentText()
        if not prog_name or prog_name not in WORKOUT_PROGRAMS:
            return
        
        dialog = ProgramEditorDialog(prog_name, WORKOUT_PROGRAMS[prog_name], parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_name, data = dialog.get_program_data()
            if new_name:
                if new_name != prog_name:
                    del WORKOUT_PROGRAMS[prog_name]
                WORKOUT_PROGRAMS[new_name] = data
                save_programs(WORKOUT_PROGRAMS)
                self._refresh_combobox(new_name)
                self.programs_changed.emit()

    def _delete_program(self):
        prog_name = self.combo_programs.currentText()
        if not prog_name:
            return
        reply = QMessageBox.question(self, "Bekræft", f"Slet programmet '{prog_name}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            del WORKOUT_PROGRAMS[prog_name]
            save_programs(WORKOUT_PROGRAMS)
            self._refresh_combobox()
            self.programs_changed.emit()

    def _refresh_combobox(self, set_name=None):
        self.combo_programs.blockSignals(True)
        self.combo_programs.clear()
        self.combo_programs.addItems(list(WORKOUT_PROGRAMS.keys()))
        if set_name and set_name in WORKOUT_PROGRAMS:
            self.combo_programs.setCurrentText(set_name)
        self.combo_programs.blockSignals(False)
        self.display_program(self.combo_programs.currentText())

    def display_program(self, prog_name: str):
        while self.container_layout.count():
            child = self.container_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        program = WORKOUT_PROGRAMS.get(prog_name, {})
        
        for day, info in program.items():
            card = QFrame()
            card.setFixedWidth(240)
            card.setStyleSheet("QFrame { background-color: #2b2b2b; border-radius: 8px; border: 1px solid #444; }")
            card_layout = QVBoxLayout(card)
            card_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            
            lbl_day = QLabel(day)
            lbl_day.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50; border: none;")
            lbl_day.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(lbl_day)
            
            lbl_title = QLabel(info.get("title", ""))
            lbl_title.setStyleSheet("font-size: 14px; font-weight: bold; color: white; border: none;")
            lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(lbl_title)
            
            # Altid opret label, så de fylder det samme vertikalt, selvom teksten er tom
            extra = info.get("extra", "")
            lbl_extra = QLabel(extra if extra else " ")
            lbl_extra.setStyleSheet("font-size: 12px; font-weight: bold; color: #E91E63; border: none;")
            lbl_extra.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(lbl_extra)
                
            div = QFrame()
            div.setFrameShape(QFrame.Shape.HLine)
            div.setStyleSheet("border: 1px solid #444;")
            card_layout.addWidget(div)
            
            for ex in info.get("exercises", []):
                if len(ex) >= 2:
                    ex_box = QWidget()
                    # Sæt en fast højde så alle øvelsesbokse flugter perfekt vandret
                    ex_box.setFixedHeight(75) 
                    ex_box.setStyleSheet("border: 1px solid #444; border-radius: 4px; background-color: #333;")
                    ex_layout = QVBoxLayout(ex_box)
                    ex_layout.setContentsMargins(5, 5, 5, 5)
                    
                    lbl_ex = QLabel(ex[0])
                    lbl_ex.setStyleSheet("color: #ccc; border: none; font-size: 12px;")
                    lbl_ex.setWordWrap(True)
                    ex_layout.addWidget(lbl_ex)
                    
                    lbl_reps = QLabel(ex[1])
                    lbl_reps.setStyleSheet("color: #ff5252; border: none; font-weight: bold; font-size: 11px;")
                    ex_layout.addWidget(lbl_reps)
                    
                    card_layout.addWidget(ex_box)
                    
            self.container_layout.addWidget(card)