import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPixmap, QImage, QTransform
from PyQt6.QtCore import Qt

class ImagePreviewWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene(self)

        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.graphics_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        self.zoom_factor = 1.0
        self.draw_overlay = True
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.graphics_view)

    def zoom(self, delta):
        if delta > 0:
            if self.zoom_factor < 5.0:
                self.zoom_factor *= 2
        elif delta < 0:
            if self.zoom_factor > 0.1:
                self.zoom_factor /= 2
        self.update_image()

    def update_image(self):
        if self.pixmap:
            self.graphics_scene.clear()
            self.graphics_scene.addPixmap(self.pixmap.scaled(self.pixmap.width() * self.zoom_factor, self.pixmap.height() * self.zoom_factor))
            
    def redraw(self):
        self.graphics_scene.clear()
        self.graphics_scene.addPixmap(self.pixmap.scaled(int(self.image_width * self.scale_factor), int(self.image_height * self.scale_factor)))
        if self.overlay_pixmap and self.draw_overlay:
            self.graphics_scene.addPixmap(self.overlay_pixmap.scaled(int(self.image_width * self.scale_factor), int(self.image_height * self.scale_factor)))
    
    def scale_121(self):
        self.graphics_scene.clear()
        self.graphics_scene.addPixmap(self.pixmap)
        if self.overlay_pixmap and self.draw_overlay:
            self.graphics_scene.addPixmap(self.overlay_pixmap)    

    def fit_to_frame(self):
        if hasattr(self, "pixmap"):
            if self.pixmap is not None:
                self.frame_width = self.width()
                self.frame_height = self.height()
                
                self.image_width = self.pixmap.width()
                self.image_height = self.pixmap.height()

                scale_x = self.frame_width / self.image_width
                scale_y = self.frame_height / self.image_height
                self.scale_factor = min(scale_x, scale_y)

                self.graphics_scene.clear()
                self.graphics_scene.addPixmap(self.pixmap.scaled(int(self.image_width * self.scale_factor), int(self.image_height * self.scale_factor)))
                if self.overlay_pixmap and self.draw_overlay:
                    self.graphics_scene.addPixmap(self.overlay_pixmap.scaled(int(self.image_width * self.scale_factor), int(self.image_height * self.scale_factor)))
                
    def toggle_overlay(self):
        self.draw_overlay = not self.draw_overlay
        self.redraw()


    def display_image(self, image, overlay=None):
        self.pixmap = QPixmap(image)
        self.overlay_pixmap = QPixmap(overlay)
        self.zoom_factor = 1.0
        self.fit_to_frame()
