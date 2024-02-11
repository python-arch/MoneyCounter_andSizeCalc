from modules.MoneyCounter import MoneyCounter
from modules.HeighMeasurement import HeightMeasurement
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import sys

if __name__ == '__main__':
    print("-"*20)
    print("1- Money Counter")
    print("2- Height Measurement")
    program_number = int(input("Enter the number of the program:"))
    
    app = QApplication(sys.argv)

    if program_number == 1 :
       main_window=  MoneyCounter()
    elif program_number == 2:
       main_window =  HeightMeasurement()  
    main_window.show()
    sys.exit(app.exec_())