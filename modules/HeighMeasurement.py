from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
from ultralytics import YOLO

class HeightMeasurement(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.coin_d = [0.0,0.0]
        self.bottle_d =[0.0,0.0]

    def init_ui(self):
        label = QLabel("Height Measurement")
        self.image_label = QLabel(self)
        self.load_image_button = QPushButton("Load Image", self)
        self.detect_objects_button = QPushButton("Measure Bottle Height", self)

        # Connect button clicks to functions
        self.load_image_button.clicked.connect(self.load_image)
        self.detect_objects_button.clicked.connect(self.detect_objects)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_image_button)
        layout.addWidget(self.detect_objects_button)
        self.setLayout(layout)
        self.setWindowTitle("Height Measurement")
        self.show()

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.pgm *.jpeg)", options=options)

        if file_name:
            resized_image = self.resize_image_load(file_name)
            # Convert the resized image to a QPixmap and set it as the pixmap for the QLabel
            pixmap = QPixmap.fromImage(QImage(resized_image.data, resized_image.shape[1], resized_image.shape[0], QImage.Format_BGR888))
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_path = file_name

    def resize_image_load(self, image_path):
        image = cv2.imread(image_path)
        desired_width = 400
        aspect_ratio = image.shape[1] / image.shape[0]
        desired_height = int(desired_width / aspect_ratio)
        resized_image = cv2.resize(image, (desired_width, desired_height))
        return resized_image
    
    def resize_image(self, image):
            # Resize the image to a smaller size
            desired_width = 400
            aspect_ratio = image.shape[1] / image.shape[0]
            desired_height = int(desired_width / aspect_ratio)
            resized_image = cv2.resize(image, (desired_width, desired_height))
            return resized_image
    def detect_objects(self):
        if hasattr(self, 'image_path'):
            # initialize the heights
            self.coin_d = [0.0,0.0]
            self.bottle_d =[0.0,0.0]
            # Load YOLO model
            model = YOLO('./model/best.pt')
            model_generic = YOLO('yolov8n.pt')
            result = model.predict(
                source=self.image_path,
                conf=0.45,
                save=True, 
            )
           # get the dimesnions of the pound
            x,y,w,h = result[0].boxes.xywh.numpy()[0]
            self.coin_d = [w , h]
            #  get the dimensions and detect the bottle
            result_bottle = model_generic.predict(
                source = self.image_path,
                conf = 0.45,
                save = True,
            )
            
            # check the existance of the bottle
            x_bottle , y_bottle , w_bottle , h_bottle = result_bottle[0].boxes.xywh.numpy()[0] 
            self.bottle_d = [w_bottle , h_bottle]
            # get the ratios
            max_coin = max(w ,h)
            ratios = [w_bottle/max_coin , h_bottle/max_coin]
            # get the dimensions of the bottle
            final_dimensions = [ratios[0] * 2.5 , ratios[1] * 2.5]
            
            QMessageBox.information(self,"The Measurement", f"The height of the input object is approximately {final_dimensions[0]} and {final_dimensions[1]} in cm")
            
        else:
            QMessageBox.warning(self, "No Image", "Please load an image before detecting objects.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MoneyCounter(None)
    window.show()
    sys.exit(app.exec_())
    