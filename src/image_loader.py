# image_loader.py

import os
from PIL import Image, ImageDraw
from io import BytesIO
from PyQt6.QtGui import QImage
from AEPi import AEI
from AEPi import exceptions


class ImageLoader:
    @staticmethod
    def load_image(image_path, image_preview):
        error = False
        if os.path.exists(image_path):
            overlay = None
            qim = None
            if image_path.lower().endswith('.aei'):
                try:
                    aei = AEI.read(image_path)
                    with aei:
                        format = aei.format 
                        # Save the whole AEI image to RAM as a PNG
                        buffer = BytesIO()
                        aei._image.save(buffer, format="PNG")
                        buffer.seek(0)

                        # Load the PNG image from RAM
                        image = Image.open(buffer)

                        # Create a separate image for the overlay
                        bboxes = Image.new('RGBA', image.size, (0, 0, 0, 0))  # Transparent background
                        
                        # Draw bounding boxes of the textures on the overlay
                        try:
                            draw = ImageDraw.Draw(bboxes)
                            for i, texture in enumerate(aei.textures):
                                id = i+1
                                x, y, w, h = texture.x, texture.y, texture.width, texture.height
                                draw.rectangle((x, y, x+w, y+h), outline="red")
                                draw.text((x, y), str(id), fill="red")  # Write the texture ID
                            overlay_valid = True
                        except:
                            overlay_valid = False
                    if overlay_valid:    
                        overlay = QImage(bboxes.tobytes("raw","RGBA"), bboxes.width, bboxes.height, bboxes.width * 4, QImage.Format.Format_RGBA8888)
                    qim = QImage(image.tobytes("raw","RGBA"), image.width, image.height, image.width * 4, QImage.Format.Format_RGBA8888)
                except ValueError as ex:
                    print(ex)
                    format = "ERR"
                    error = True
                except exceptions.AEPiException as ex:
                    print(ex)
                    format = "ERR"
                    error = True
                except:
                    print("AEI reading error")
                    format = "ERR"
                    error = True

            else:
                format = "PNG"
                qim = QImage(image_path)
            
            if error == True:
                qim = QImage(os.path.join(os.path.dirname(__file__),"readerr.png"))
                
            return (qim, overlay, format)
        else:
            return None
