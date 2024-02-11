from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
from PIL import Image
from ultralytics import YOLO

class MoneyCounter(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.money_amount = 0.0

    def init_ui(self):
        label = QLabel("Money Counter")
        self.image_label = QLabel(self)
        self.load_image_button = QPushButton("Load Image", self)
        self.detect_objects_button = QPushButton("Count Coins", self)

        # Connect button clicks to functions
        self.load_image_button.clicked.connect(self.load_image)
        self.detect_objects_button.clicked.connect(self.detect_objects)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_image_button)
        layout.addWidget(self.detect_objects_button)
        self.setLayout(layout)
        self.setWindowTitle("Money Counter")
        self.show()

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.pgm)", options=options)

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
            # initialize the count
            self.money_amount = 0.0
            # Load YOLO model
            model = YOLO('./model/best.pt')

            result = model.predict(
                source=self.image_path,
                conf=0.45,
                save=True, 
            )
            classes = result[0].boxes.cls.numpy()
            
            # display the image of the detected box
            for c in classes:
                if int(c) == 1:
                    self.money_amount += 0.5
                elif int(c) == 0:
                    self.money_amount += 1.0


            image = cv2.imread(self.image_path)
            for b in result[0].boxes.xyxy.numpy():
                    x1, y1, x2, y2 = map(int, b)
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 10)
            image = self.resize_image(image)

            position = (10, 50)  # (x, y) coordinates
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_size = 0.5
            font_thickness = 2
            font_color = (0, 0, 255)  # BGR color format (blue, green, red)

            if self.money_amount > 0.0:
                text = f"The amount of money in the photo is ${self.money_amount} L.E"
            else:
                text = "There is no money in the photo"

            # Write the text on the image
            cv2.putText(image, text, position, font, font_size, font_color, font_thickness)

            # Convert the OpenCV image to a QImage
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w, ch = image_rgb.shape
            bytes_per_line = ch * w
            q_image = QImage(image_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Convert QImage to QPixmap and set it as the pixmap for the QLabel
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
        else:
            QMessageBox.warning(self, "No Image", "Please load an image before detecting objects.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MoneyCounter(None)
    window.show()
    sys.exit(app.exec_())
