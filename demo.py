import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QFrame, QSplitter
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QImage
from PyQt5.QtCore import Qt
from ultralytics import YOLO

class ImageFrame(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(1)
        self.title = title
        self.pixmap = None
        self.setStyleSheet("background-color: white;")

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(10, 20, self.title)
        if self.pixmap:
            painter.drawPixmap(self.rect().adjusted(10, 30, -10, -10), self.pixmap)
        else:
            painter.drawText(self.rect().adjusted(10, 30, -10, -10), Qt.AlignCenter, "")  # 图像显示区域

    def setPixmap(self, pixmap):
        self.pixmap = pixmap.scaled(self.size().width() - 20, self.size().height() - 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.update()

class RoadCrackDetectionSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image_path = None

    def initUI(self):
        self.setWindowTitle('道路裂缝检测系统')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #E6F3FF;")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 标题
        title_label = QLabel('道路裂缝检测系统')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black; border: 2px solid blue; padding: 5px; background-color: white;")
        title_label.setFixedHeight(40)  # 设置固定高度
        main_layout.addWidget(title_label)

        # 按钮布局
        button_layout = QHBoxLayout()
        self.open_button = QPushButton('打开待检测图像')
        self.detect_button = QPushButton('检测')
        button_style = "font-size: 16px; padding: 5px; background-color: #4CAF50; color: white; border: none; border-radius: 5px;"
        self.open_button.setStyleSheet(button_style)
        self.detect_button.setStyleSheet(button_style)
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.detect_button)
        main_layout.addLayout(button_layout)

        # 图像显示区域布局
        image_layout = QHBoxLayout()
        self.input_image_frame = ImageFrame('待检测图像')
        self.result_image_frame = ImageFrame('检测结果')
        image_layout.addWidget(self.input_image_frame)
        image_layout.addWidget(self.result_image_frame)
        main_layout.addLayout(image_layout)

        # 设置布局比例
        main_layout.setStretch(0, 1)  # 标题
        main_layout.setStretch(1, 1)  # 按钮
        main_layout.setStretch(2, 6)  # 图像区域

        self.setLayout(main_layout)

        # 连接按钮到函数
        self.open_button.clicked.connect(self.open_image)
        self.detect_button.clicked.connect(self.detect_cracks)

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图像", "", "图像文件 (*.png *.jpg *.bmp)")
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            self.input_image_frame.setPixmap(pixmap)

    def detect_cracks(self):
        if self.image_path:
            onnx_model = YOLO("/Volumes/2T/Code/QT/best.onnx")
            results = onnx_model(self.image_path)
            img = results[0].plot()
            height, width, channel = img.shape
            bytes_per_line = 3 * width
            q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.result_image_frame.setPixmap(pixmap)
        else:
            self.result_image_frame.setPixmap(QPixmap())
            self.result_image_frame.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.input_image_frame.setPixmap(pixmap)
            self.result_image_frame.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RoadCrackDetectionSystem()
    ex.show()
    sys.exit(app.exec_())