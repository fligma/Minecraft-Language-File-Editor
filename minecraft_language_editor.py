import sys
import json
import os
import glob
import configparser
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QLabel, QStackedWidget, QScrollArea, QInputDialog, QMessageBox, 
                             QFileDialog, QLineEdit, QFormLayout, QColorDialog, QGroupBox, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCloseEvent, QColor

# flyonisis (2026)
script_path = os.path.dirname(os.path.abspath(__file__))

DEFAULT_THEME = {
    "name": "DarkSheets",
    "bg_main": "#131314","fg_main": "#e3e3e3",
    "bg_button": "#303134","bg_button_hover": "#3c4043",
    "border_color": "#444746",
    "bg_table": "#1e1f22","bg_header": "#202124",
    "fg_header": "#9aa0a6",
    "selection_bg": "#3c4043","selection_fg": "#8ab4f8",
    "accent_color": "#8ab4f8","accent_fg": "#202124",
    "input_bg": "#202124"
}

THEME_KEYS = {
    "bg_main": "Main Background","fg_main": "Main Text",
    "bg_button": "Button Background","bg_button_hover": "Button Hover",
    "border_color": "Borders",
    "bg_table": "Table Background","bg_header": "Header / Alt Background",
    "fg_header": "Header / Sub Text",
    "selection_bg": "Selection Background","selection_fg": "Selection Text",
    "accent_color": "Accent Background","accent_fg": "Accent Text",
    "input_bg": "Input Background"
}

def generate_stylesheet(t: dict) -> str:
    return f"""
        QMainWindow, QWidget {{
            background-color: {t.get('bg_main', '#131314')};
            color: {t.get('fg_main', '#e3e3e3')};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        QPushButton {{
            background-color: {t.get('bg_button', '#303134')};
            color: {t.get('fg_main', '#e3e3e3')};
            border: 1px solid {t.get('border_color', '#444746')};
            padding: 8px 16px;
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: {t.get('bg_button_hover', '#3c4043')};
        }}
        QPushButton#accent {{
            background-color: {t.get('accent_color', '#8ab4f8')};
            color: {t.get('accent_fg', '#202124')};
            font-weight: bold;
        }}
        QPushButton#accent:hover {{
            background-color: {t.get('selection_fg', '#aecbfa')}; 
        }}
        QPushButton#fileCard {{
            background-color: {t.get('input_bg', '#202124')};
            border: 1px solid {t.get('border_color', '#444746')};
            border-radius: 8px;
            text-align: left;
            padding: 10px;
        }}
        QPushButton#fileCard:hover {{
            background-color: {t.get('bg_button', '#303134')};
            border: 1px solid {t.get('accent_color', '#8ab4f8')};
        }}
        QTableWidget {{
            background-color: {t.get('bg_table', '#1e1f22')};
            color: {t.get('fg_main', '#e3e3e3')};
            gridline-color: {t.get('border_color', '#444746')};
            border: 1px solid {t.get('border_color', '#444746')};
            selection-background-color: {t.get('selection_bg', '#3c4043')};
            selection-color: {t.get('selection_fg', '#8ab4f8')};
        }}
        QHeaderView::section {{
            background-color: {t.get('bg_header', '#202124')};
            color: {t.get('fg_header', '#9aa0a6')};
            border: 1px solid {t.get('border_color', '#444746')};
            border-top: 0px;
            border-left: 0px;
            padding: 4px;
            font-weight: bold;
        }}
        QTableCornerButton::section {{
            background-color: {t.get('bg_header', '#202124')};
            border: 1px solid {t.get('border_color', '#444746')};
        }}
        QLineEdit, QInputDialog, QComboBox {{
            background-color: {t.get('input_bg', '#202124')};
            color: {t.get('fg_main', '#e3e3e3')};
            border: 1px solid {t.get('border_color', '#444746')};
            padding: 6px;
            border-radius: 4px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {t.get('input_bg', '#202124')};
            color: {t.get('fg_main', '#e3e3e3')};
            selection-background-color: {t.get('selection_bg', '#3c4043')};
        }}
        QScrollBar:vertical {{
            background: {t.get('bg_main', '#131314')};
            width: 12px;
        }}
        QScrollBar::handle:vertical {{
            background: {t.get('border_color', '#444746')};
            min-height: 20px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {t.get('bg_button_hover', '#3c4043')};
        }}
        QMessageBox {{
            background-color: {t.get('bg_header', '#202124')};
        }}
        QLabel#subText {{
            color: {t.get('fg_header', '#9aa0a6')};
        }}
        QScrollArea {{
            border: 1px solid {t.get('border_color', '#444746')};
            background-color: {t.get('bg_table', '#1e1f22')};
            border-radius: 8px;
        }}
        QGroupBox {{
            border: 1px solid {t.get('border_color', '#444746')};
            border-radius: 8px;
            margin-top: 1ex;
            padding-top: 20px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
            color: {t.get('fg_header', '#9aa0a6')};
        }}
    """

def jio(o:str, p:str, d:dict=None) -> dict:
    """#######jio o=op p=path d=data\n# (ops)\n#  'r' = read json\n#  'w' = write json\n#######"""
    if d is None: d = {}
    try:
        if o == 'r':
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif o == 'w':
            with open(p, 'w', encoding='utf-8') as f:
                json.dump(d, f, indent=4, ensure_ascii=False)
            return {}
    except Exception as e:
        print(f"File operation error: {e}")
        return {}

config_file = os.path.join(script_path, 'config.ini')
config = configparser.ConfigParser()

def load_config():
    if not os.path.exists(config_file):
        config['Preferences'] = {
            'Theme': 'DarkSheets',
            'SavePath': 'langs',
            'TemplatePath': 'templates'
        }
        save_config()
    else:
        config.read(config_file)
    ensure_directories()

def save_config():
    with open(config_file, 'w', encoding='utf-8') as f:
        config.write(f)

def ensure_directories():
    save_path = get_save_path()
    template_path = get_template_path()
    theme_path = os.path.join(script_path, 'themes')
    
    os.makedirs(save_path, exist_ok=True)
    os.makedirs(template_path, exist_ok=True)
    os.makedirs(theme_path, exist_ok=True)

    # default template
    if not glob.glob(os.path.join(template_path, "*.json")):
        default_template = os.path.join(template_path, "default_template.json")
        jio('w', default_template, {
            "language.code": "en_ca",
            "language.name": "English",
            "language.region": "Canada",
            "gui.done": "Done",
            "gui.cancel": "Cancel"
        })
        
    # default theme
    default_theme_file = os.path.join(theme_path, "DarkSheets.json")
    if not os.path.exists(default_theme_file):
        jio('w', default_theme_file, DEFAULT_THEME)

def get_save_path():
    path = config.get('Preferences', 'SavePath', fallback='langs')
    return path if os.path.isabs(path) else os.path.join(script_path, path)

def get_template_path():
    path = config.get('Preferences', 'TemplatePath', fallback='templates')
    return path if os.path.isabs(path) else os.path.join(script_path, path)

class ThemeEditorWidget(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.draft_theme = DEFAULT_THEME.copy()
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Theme Maker")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        btn_back = QPushButton("Back to Settings")
        btn_back.clicked.connect(lambda: self.parent_app.stacked_widget.setCurrentWidget(self.parent_app.settings_view))
        header_layout.addWidget(btn_back)
        self.layout.addLayout(header_layout)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(40)

        # editor
        form_container = QWidget()
        self.form_layout = QFormLayout(form_container)
        self.color_buttons = {}
        
        for key, name in THEME_KEYS.items():
            btn = QPushButton()
            btn.setFixedSize(50, 25)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, k=key: self.pick_color(k))
            self.color_buttons[key] = btn
            self.form_layout.addRow(name + ":", btn)
            
        content_layout.addWidget(form_container)

        # Preview
        self.preview_box = QGroupBox("Live Preview")
        preview_layout = QVBoxLayout(self.preview_box)
        preview_layout.setSpacing(15)
        
        preview_table = QTableWidget(2, 2)
        preview_table.setHorizontalHeaderLabels(["Key", "Value"])
        preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        preview_table.setItem(0, 0, QTableWidgetItem("gui.done"))
        preview_table.setItem(0, 1, QTableWidgetItem("Done"))
        preview_table.setItem(1, 0, QTableWidgetItem("gui.cancel"))
        preview_table.setItem(1, 1, QTableWidgetItem("Cancel"))
        preview_table.setCurrentCell(0, 0)
        
        preview_input = QLineEdit("Sample Text Input")
        preview_btn = QPushButton("Standard Button")
        preview_accent = QPushButton("Accent Button")
        preview_accent.setObjectName("accent")
        
        preview_layout.addWidget(preview_table)
        preview_layout.addWidget(preview_input)
        preview_layout.addWidget(preview_btn)
        preview_layout.addWidget(preview_accent)
        preview_layout.addStretch()
        
        content_layout.addWidget(self.preview_box, stretch=1)
        self.layout.addLayout(content_layout)
        #save
        btn_save = QPushButton("Save New Theme As...")
        btn_save.setObjectName("accent")
        btn_save.setMinimumHeight(40)
        btn_save.clicked.connect(self.save_theme)
        self.layout.addWidget(btn_save)

    def load_theme_to_editor(self, theme_data):
        self.draft_theme = theme_data.copy()
        self.update_ui()

    def update_ui(self):
        for key, btn in self.color_buttons.items():
            color = self.draft_theme.get(key, "#000000")
            btn.setStyleSheet(f"background-color: {color}; border: 1px solid #777; border-radius: 4px;")
        
        # Apply stylesheet
        self.preview_box.setStyleSheet(generate_stylesheet(self.draft_theme))

    def pick_color(self, key):
        init_color = QColor(self.draft_theme.get(key, "#ffffff"))
        color = QColorDialog.getColor(init_color, self, f"Select color for {THEME_KEYS[key]}")
        if color.isValid():
            self.draft_theme[key] = color.name()
            self.update_ui()

    def save_theme(self):
        name, ok = QInputDialog.getText(self, "Save Theme", "Enter new theme name (e.g. LightMode):")
        if ok and name.strip():
            clean_name = name.strip()
            self.draft_theme['name'] = clean_name
            theme_path = os.path.join(script_path, 'themes', f"{clean_name}.json")
            
            jio('w', theme_path, self.draft_theme)
            
            QMessageBox.information(self, "Theme Saved", f"Theme '{clean_name}' saved successfully!")
            self.parent_app.settings_view.refresh_themes()
            
            # Select and Apply
            idx = self.parent_app.settings_view.theme_combo.findText(clean_name)
            if idx >= 0:
                self.parent_app.settings_view.theme_combo.setCurrentIndex(idx)
                
            self.parent_app.apply_theme(clean_name)
            self.parent_app.show_menu()


class SettingsWidget(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(self.parent_app.show_menu)
        header_layout.addWidget(btn_back)
        self.layout.addLayout(header_layout)

        # Form Layout
        form_layout = QFormLayout()
        
        self.save_path_input = QLineEdit(config.get('Preferences', 'SavePath', fallback='langs'))
        btn_browse_save = QPushButton("Browse...")
        btn_browse_save.clicked.connect(self.browse_save_path)
        save_layout = QHBoxLayout()
        save_layout.addWidget(self.save_path_input)
        save_layout.addWidget(btn_browse_save)
        form_layout.addRow("Files Save Path:", save_layout)

        self.template_path_input = QLineEdit(config.get('Preferences', 'TemplatePath', fallback='templates'))
        btn_browse_template = QPushButton("Browse...")
        btn_browse_template.clicked.connect(self.browse_template_path)
        template_layout = QHBoxLayout()
        template_layout.addWidget(self.template_path_input)
        template_layout.addWidget(btn_browse_template)
        form_layout.addRow("Templates Path:", template_layout)

        # Theme Selector
        self.theme_combo = QComboBox()
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(self.theme_combo)
        
        btn_theme_maker = QPushButton("Open Theme Maker")
        btn_theme_maker.clicked.connect(self.open_theme_maker)
        theme_layout.addWidget(btn_theme_maker)
        form_layout.addRow("Application Theme:", theme_layout)

        self.layout.addLayout(form_layout)
        self.layout.addStretch()

        # Apply Button
        btn_apply = QPushButton("Apply and Save")
        btn_apply.setObjectName("accent")
        btn_apply.clicked.connect(self.apply_settings)
        self.layout.addWidget(btn_apply)
        
        self.refresh_themes()

    def refresh_themes(self):
        self.theme_combo.clear()
        themes_dir = os.path.join(script_path, 'themes')
        for f in glob.glob(os.path.join(themes_dir, "*.json")):
            self.theme_combo.addItem(os.path.basename(f).replace(".json", ""))
            
        current_theme = config.get('Preferences', 'Theme', fallback='DarkSheets')
        idx = self.theme_combo.findText(current_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)

    def browse_save_path(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Save Directory", get_save_path())
        if dir_path: self.save_path_input.setText(dir_path)

    def browse_template_path(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Templates Directory", get_template_path())
        if dir_path: self.template_path_input.setText(dir_path)

    def open_theme_maker(self):
        selected_theme = self.theme_combo.currentText()
        theme_path = os.path.join(script_path, 'themes', f"{selected_theme}.json")
        theme_data = jio('r', theme_path) if os.path.exists(theme_path) else DEFAULT_THEME
        
        self.parent_app.theme_editor_view.load_theme_to_editor(theme_data)
        self.parent_app.stacked_widget.setCurrentWidget(self.parent_app.theme_editor_view)

    def apply_settings(self):
        config.set('Preferences', 'SavePath', self.save_path_input.text())
        config.set('Preferences', 'TemplatePath', self.template_path_input.text())
        
        selected_theme = self.theme_combo.currentText()
        config.set('Preferences', 'Theme', selected_theme)
        
        save_config()
        ensure_directories()
        self.parent_app.apply_theme(selected_theme)
        
        QMessageBox.information(self, "Settings", "Settings applied and saved successfully!")
        self.parent_app.show_menu()


class MainMenuWidget(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Minecraft Language Files")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        btn_settings = QPushButton("Settings")
        btn_settings.clicked.connect(lambda: self.parent_app.stacked_widget.setCurrentWidget(self.parent_app.settings_view))
        header_layout.addWidget(btn_settings)
        
        self.layout.addLayout(header_layout)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: transparent;")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(10)
        self.scroll.setWidget(self.scroll_content)
        
        self.layout.addWidget(self.scroll)

        # Create New Button
        self.btn_new = QPushButton("+ Create New Language File")
        self.btn_new.setObjectName("accent")
        self.btn_new.setMinimumHeight(50)
        self.btn_new.clicked.connect(self.create_new_file)
        self.layout.addWidget(self.btn_new)

    def refresh_file_list(self):
        for i in reversed(range(self.scroll_layout.count())): 
            self.scroll_layout.itemAt(i).widget().setParent(None)

        save_path = get_save_path()
        json_files = glob.glob(os.path.join(save_path, "*.json"))
        
        if not json_files:
            empty_lbl = QLabel("No files found in your save directory. Create one!")
            empty_lbl.setObjectName("subText")
            self.scroll_layout.addWidget(empty_lbl)
        
        for file_path in json_files:
            file_name = os.path.basename(file_path)
            data = jio('r', file_path)
            
            if isinstance(data, dict):
                lang_name = data.get("language.name", "Unknown Language")
                lang_region = data.get("language.region", "Unknown Region")
                description = f"{lang_name} ({lang_region})"

                # Create File
                card = QPushButton()
                card.setObjectName("fileCard")
                card_layout = QVBoxLayout(card)
                
                lbl_title = QLabel(file_name)
                lbl_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
                lbl_title.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
                
                lbl_desc = QLabel(description)
                lbl_desc.setFont(QFont("Segoe UI", 10))
                lbl_desc.setObjectName("subText")
                lbl_desc.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

                card_layout.addWidget(lbl_title)
                card_layout.addWidget(lbl_desc)
                card.setMinimumHeight(80)
                card.clicked.connect(lambda checked, fp=file_path: self.parent_app.open_editor(fp))
                self.scroll_layout.addWidget(card)

    def create_new_file(self):
        template_path = get_template_path()
        templates = glob.glob(os.path.join(template_path, "*.json"))
        
        if not templates:
            QMessageBox.warning(self, "No Templates", "No templates found in your templates folder!")
            return
            
        template_names = [os.path.basename(t) for t in templates]
        selected_template, ok1 = QInputDialog.getItem(self, "Select Template", "Choose a blueprint template to use:", template_names, 0, False)
        if not ok1 or not selected_template: return
        
        name, ok2 = QInputDialog.getText(self, "New Language File", "Enter new file name (e.g. fr_fr.json):")
        if not ok2 or not name.strip(): return
        
        if not name.endswith(".json"):
            name += ".json"
            
        filepath = os.path.join(get_save_path(), name)
        if os.path.exists(filepath):
            QMessageBox.warning(self, "Error", "File already exists!")
            return
            
        template_data = jio('r', os.path.join(template_path, selected_template))
        jio('w', filepath, template_data)
        
        self.parent_app.open_editor(filepath)

class EditorWidget(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.current_file = None
        self.unsaved_changes = False
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()
        self.lbl_filename = QLabel("Editing: ")
        self.lbl_filename.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header_layout.addWidget(self.lbl_filename)
        header_layout.addStretch()

        self.lbl_count = QLabel("Lines: 0")
        self.lbl_count.setObjectName("subText")
        header_layout.addWidget(self.lbl_count)

        self.btn_back = QPushButton("Back to Menu")
        self.btn_back.clicked.connect(self.request_back)
        header_layout.addWidget(self.btn_back)
        self.layout.addLayout(header_layout)

        # Table
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Translation Key", "Translated Value"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 400)
        self.table.itemChanged.connect(self.mark_unsaved)
        self.layout.addWidget(self.table)

        # Action Buttons
        actions_layout = QHBoxLayout()
        
        self.btn_add_row = QPushButton("+ Add Row")
        self.btn_add_row.clicked.connect(self.add_empty_row)
        actions_layout.addWidget(self.btn_add_row)
        
        actions_layout.addStretch()
        
        self.btn_save = QPushButton("Save Changes")
        self.btn_save.setObjectName("accent")
        self.btn_save.setMinimumWidth(150)
        self.btn_save.clicked.connect(self.save_file)
        actions_layout.addWidget(self.btn_save)

        self.layout.addLayout(actions_layout)
    
    def update_line_count(self):
        self.lbl_count.setText(f"Lines: {self.table.rowCount()}")

    def load_file(self, filepath):
        self.current_file = filepath
        filename = os.path.basename(filepath)
        self.lbl_filename.setText(f"Editing: {filename}")
        
        data = jio('r', filepath)
        if not data: data = {}

        self.table.blockSignals(True) 
        self.table.setRowCount(len(data))
        for row, (key, value) in enumerate(data.items()):
            self.table.setItem(row, 0, QTableWidgetItem(str(key)))
            self.table.setItem(row, 1, QTableWidgetItem(str(value)))
        self.table.blockSignals(False)
        self.unsaved_changes = False
        self.update_line_count()

    def add_empty_row(self):
        row = self.table.rowCount()
        self.table.blockSignals(True)
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))
        self.table.blockSignals(False)
        self.table.scrollToBottom()
        self.mark_unsaved()
        self.update_line_count()

    def mark_unsaved(self):
        self.unsaved_changes = True

    def check_unsaved_warning(self):
        if self.unsaved_changes:
            reply = QMessageBox.question(self, 'Unsaved Changes',
                                         "You have unsaved changes. Are you sure you want to exit without saving?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            return reply == QMessageBox.StandardButton.Yes
        return True

    def request_back(self):
        if self.check_unsaved_warning():
            self.parent_app.show_menu()

    def save_file(self):
        if not self.current_file: return
        
        reply = QMessageBox.question(self, 'Confirm Save',
                                     f"Are you sure you want to save changes to {os.path.basename(self.current_file)}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.Yes)
                                     
        if reply == QMessageBox.StandardButton.Yes:
            data = {}
            for row in range(self.table.rowCount()):
                key_item = self.table.item(row, 0)
                val_item = self.table.item(row, 1)
                
                key = key_item.text().strip() if key_item else ""
                val = val_item.text() if val_item else ""
                
                data[key] = val
                    
            jio('w', self.current_file, data)
            self.unsaved_changes = False
            QMessageBox.information(self, "Success", "File saved successfully!")

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        load_config()
        self.setWindowTitle("Minecraft Language Editor | Copyright (C) 2026  Fligma")
        self.setMinimumSize(1000, 700)

        # Setup Stacked Widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.menu_view = MainMenuWidget(self)
        self.editor_view = EditorWidget(self)
        self.settings_view = SettingsWidget(self)
        self.theme_editor_view = ThemeEditorWidget(self)

        self.stacked_widget.addWidget(self.menu_view)
        self.stacked_widget.addWidget(self.editor_view)
        self.stacked_widget.addWidget(self.settings_view)
        self.stacked_widget.addWidget(self.theme_editor_view)

        # Apply theme
        self.apply_theme(config.get('Preferences', 'Theme', fallback='DarkSheets'))

        self.show_menu()

    def apply_theme(self, theme_name):
        theme_path = os.path.join(script_path, 'themes', f"{theme_name}.json")
        if os.path.exists(theme_path):
            theme_data = jio('r', theme_path)
            # safe fallback for broken json keys
            merged_theme = {**DEFAULT_THEME, **theme_data} 
            self.setStyleSheet(generate_stylesheet(merged_theme))
        else:
            self.setStyleSheet(generate_stylesheet(DEFAULT_THEME))

    def show_menu(self):
        self.menu_view.refresh_file_list()
        self.stacked_widget.setCurrentWidget(self.menu_view)

    def open_editor(self, filepath):
        self.editor_view.load_file(filepath)
        self.stacked_widget.setCurrentWidget(self.editor_view)

    def closeEvent(self, event: QCloseEvent):
        if self.stacked_widget.currentWidget() == self.editor_view:
            if not self.editor_view.check_unsaved_warning():
                event.ignore()
                return
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())