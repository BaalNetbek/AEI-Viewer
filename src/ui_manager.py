import os
from PyQt6.QtWidgets import QApplication, QDockWidget, QMainWindow, QToolBar, QFileDialog, QListWidget, QListWidgetItem, QAbstractItemView, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QPushButton, QFileDialog
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from image_preview_window import ImagePreviewWindow
from image_loader import ImageLoader

from file_browser import FileBrowser
from PyQt6 import QtGui
from PyQt6.QtCore import *

class UIManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.File_browser_visible = True
        self.Auto_scale = True
        
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("AEI Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create the central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_layout = QHBoxLayout(self.central_widget)

        # Create dock widgets for browser and preview
        self.browser_dock = QDockWidget("File Browser", self)
        self.preview_dock = QDockWidget("Image Preview", self)

        # Create the file browser widget
        self.browser_widget = FileBrowser(self)
        self.browser_dock.setWidget(self.browser_widget)

        # Create the image preview widget and layout
        self.preview_widget = QWidget(self.preview_dock)
        self.preview_layout = QVBoxLayout(self.preview_widget)

        self.image_preview = ImagePreviewWindow(self.preview_widget)
        self.preview_layout.addWidget(self.image_preview)

        # Set the widgets for the dock widgets
        self.preview_dock.setWidget(self.preview_widget)

        # Add dock widgets to main window
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.browser_dock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.preview_dock)

        # Create the toolbar
        self.toolbar = QToolBar("Toolbar", self)
        self.addToolBar(self.toolbar)

        # Set the stretch factors for the dock widgets
        self.central_layout.addWidget(self.browser_dock, stretch=1)
        self.central_layout.addWidget(self.preview_dock, stretch=2)

        # Set the minimum and maximum widths of the dock widgets
        self.browser_dock.setMinimumWidth(100)
        self.browser_dock.setMaximumWidth(300)
        self.preview_dock.setMinimumWidth(400)

        # Create the "Go Up" button
        self.go_up_button = QAction(QIcon("up.png"), "Go Up", self)
        self.go_up_button.triggered.connect(self.browser_widget.go_up_directory)
        self.toolbar.addAction(self.go_up_button)

        # Create the "Reset Image" button
        self.reset_image_button = QAction(QIcon("reset.png"), "Reset Image", self)
        self.reset_image_button.triggered.connect(self.image_preview.fit_to_frame)
        self.toolbar.addAction(self.reset_image_button)

        # Create the "Toggle File Browser" button
        self.toggle_file_browser_button = QAction(QIcon("toggle.png"), "Toggle File Browser", self)
        self.toggle_file_browser_button.triggered.connect(self.toggle_file_browser)
        self.toolbar.addAction(self.toggle_file_browser_button)

        # Create the "Toggle Overlay" button
        self.toggle_overlay_button = QAction(QIcon("overlay.png"), "Toggle Overlay", self)
        self.toggle_overlay_button.triggered.connect(self.image_preview.toggle_overlay)
        self.toolbar.addAction(self.toggle_overlay_button)

        # Create the "Auto Scale" button
        self.auto_scale_button = QAction(QIcon("autoscale.png"), "Auto Scale", self)
        self.auto_scale_button.triggered.connect(self.toggle_auto_scale)
        self.toolbar.addAction(self.auto_scale_button)

        # Create the "New File Browser" button
        self.new_file_browser_button = QAction(QIcon("new.png"), "New File Browser", self)
        self.new_file_browser_button.triggered.connect(self.new_file_browser)
        self.toolbar.addAction(self.new_file_browser_button)

        # Create the "New Preview" button
        self.new_preview_button = QAction(QIcon("new.png"), "New Preview", self)
        self.new_preview_button.triggered.connect(self.new_preview)
        self.toolbar.addAction(self.new_preview_button)
        
    def new_file_browser(self):
        new_browser_dock = QDockWidget("File Browser", self)
        new_browser_widget = FileBrowser()
        new_browser_dock.setWidget(new_browser_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, new_browser_dock)

    def new_preview(self):
        new_preview_dock = QDockWidget("Image Preview", self)
        new_preview_widget = QWidget(new_preview_dock)
        new_preview_layout = QVBoxLayout(new_preview_widget)
        new_image_preview = ImagePreviewWindow(new_preview_widget)
        new_preview_layout.addWidget(new_image_preview)
        new_preview_dock.setWidget(new_preview_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, new_preview_dock)


    def toggle_auto_scale(self):
        self.Auto_scale = not self.Auto_scale

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.Auto_scale is True:
            self.image_preview.fit_to_frame()

    def reset_image(self):
        self.image_preview.fit_to_frame()

    def toggle_file_browser(self):
        if self.file_browser_visible:
            self.file_listwidget.hide()
            self.toggle_file_browser_button.setText("Show File Browser")
        else:
            self.file_listwidget.show()
            self.toggle_file_browser_button.setText("Hide File Browser")
        self.file_browser_visible = not self.file_browser_visible
        
    def change_path(self):
        new_path = self.path_edit.text()
        if os.path.exists(new_path):
            self.current_path = new_path
            self.load_files()
        else:
            print("Invalid path")
      

    def select_image(self, item):
        selected_item = item.text()

        if selected_item == "..":
            self.browser_widget.go_up_directory()
        elif os.path.isdir(selected_item):
            os.chdir(selected_item)
            self.browser_widget.current_path = os.getcwd()
            self.browser_widget.load_files()
        else:
            image_path = os.path.join(self.browser_widget.current_path, selected_item)
            if os.path.exists(image_path):
                self.loadedImage = ImageLoader.load_image(image_path, self.image_preview)
                self.image_preview.display_image(self.loadedImage[0],self.loadedImage[1])
            else:
                print("Image not found:", image_path)
