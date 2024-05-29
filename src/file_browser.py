from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QAbstractItemView
from PyQt6.QtGui import QIcon, QAction
from PyQt6 import QtGui 
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt

import os

class FileBrowser(QWidget):
    def __init__(self,ui_manager):
        super().__init__()
        self.ui_manager = ui_manager
        self.current_path = os.getcwd()

        self.init_ui()

    def init_ui(self):
    
        
        self.layout = QVBoxLayout(self)

        self.path_bar = QVBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setText(self.current_path)
        self.path_edit.returnPressed.connect(self.change_path)
        self.path_bar.addWidget(self.path_edit)
        self.path_button = QPushButton("Browse")
        self.path_button.clicked.connect(self.browse_path)
        self.path_bar.addWidget(self.path_button)
        self.layout.addLayout(self.path_bar)

        self.file_listwidget = QListWidget(self)
        self.file_listwidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.layout.addWidget(self.file_listwidget)

        self.file_listwidget.itemDoubleClicked.connect(self.ui_manager.select_image)
    
        self.load_files()

    def load_files(self):
        self.file_listwidget.clear()

        current_path = self.current_path
        self.setWindowTitle("AEI Viewer - " + current_path)

        files = []
        directories = []

        for item in os.listdir(current_path):
            if os.path.isdir(item):
                directories.append(item)
            elif item.lower().endswith('.aei'):
                files.append(('AEI', item))
            elif item.lower().endswith('.png'):
                files.append(('PNG', item))

        directories.sort()

        item = QListWidgetItem("..")
        self.file_listwidget.addItem(item)

        for directory in directories:
            item = QListWidgetItem(directory)
            self.file_listwidget.addItem(item)

        for filetype, filename in files:
            item = QListWidgetItem(filename)
            if filetype == 'AEI':
                item.setForeground(QtGui.QBrush(QtGui.QColor('red')))
            elif filetype == 'PNG':
                item.setForeground(QtGui.QBrush(QtGui.QColor('blue')))
            self.file_listwidget.addItem(item)

    def change_path(self):
        new_path = self.path_edit.text()
        if os.path.exists(new_path):
            os.chdir(new_path)
            self.current_path = os.getcwd()
            self.path_edit.setText(self.current_path)
            self.load_files()
        else:
            print("Invalid path")

    def browse_path(self):
        new_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if new_path:
            os.chdir(new_path)
            self.current_path = os.getcwd()
            self.path_edit.setText(self.current_path)
            self.load_files()

    def select_image(self, item):
        selected_item = item.text()

        if selected_item == "..":
            self.go_up_directory()
        elif os.path.isdir(selected_item):
            os.chdir(selected_item)
            self.current_path = os.getcwd()
            self.load_files()
        else:
            image_path = os.path.join(self.current_path, selected_item)

    def go_up_directory(self):
        os.chdir("..")
        self.current_path = os.getcwd()
        self.path_edit.setText(self.current_path)
        self.load_files()  # Load files after going up a directory
        

