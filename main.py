import sys
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QVBoxLayout,
                             QPushButton, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem)
from PyQt5.QtGui import QColor, QPen, QBrush, QPainter, QPixmap
from PyQt5.QtCore import Qt, QTimer, QRectF

class BinaryClockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.background_image = None
        self.dark_mode = False
        self.on_color = QColor(46, 204, 113)
        self.off_color = QColor(231, 76, 60)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Binäre Uhr')
        self.setGeometry(100, 100, 400, 300)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Menü-Button
        self.menu_button = QPushButton('...', self)
        self.menu_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.5);
                border: none;
                color: white;
                font-weight: bold;
                font-size: 20px;
                padding: 5px 10px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.7);
            }
        """)
        self.menu_button.clicked.connect(self.show_menu)
        main_layout.addWidget(self.menu_button, alignment=Qt.AlignTop | Qt.AlignRight)

        clock_layout = QGridLayout()
        main_layout.addLayout(clock_layout)

        self.circles = {
            'h1': self.create_circles(2),
            'h2': self.create_circles(4),
            'm1': self.create_circles(3),
            'm2': self.create_circles(4),
            's1': self.create_circles(3),
            's2': self.create_circles(4)
        }

        for i, (key, circles) in enumerate(self.circles.items()):
            for j, circle in enumerate(circles):
                clock_layout.addWidget(circle, 3 - j, i)

        self.h_label = QLabel('H')
        self.m_label = QLabel('M')
        self.s_label = QLabel('S')
        clock_layout.addWidget(self.h_label, 4, 0, 1, 2, Qt.AlignCenter)
        clock_layout.addWidget(self.m_label, 4, 2, 1, 2, Qt.AlignCenter)
        clock_layout.addWidget(self.s_label, 4, 4, 1, 2, Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

        self.update_style()
        self.show()

    def create_circles(self, count):
        circles = []
        for _ in range(count):
            view = QGraphicsView()
            scene = QGraphicsScene()
            view.setScene(scene)
            view.setRenderHint(QPainter.Antialiasing)
            view.setFixedSize(60, 60)
            view.setStyleSheet("background: transparent; border: none;")
            circle = QGraphicsEllipseItem(QRectF(5, 5, 50, 50))
            circle.setPen(QPen(Qt.NoPen))
            scene.addItem(circle)
            circles.append(view)
        return circles

    def show_menu(self):
        from PyQt5.QtWidgets import QMenu
        menu = QMenu(self)
        bg_action = menu.addAction('Hintergrundbild wählen')
        bg_action.triggered.connect(self.choose_background)
        dark_action = menu.addAction('Dark Mode')
        dark_action.setCheckable(True)
        dark_action.setChecked(self.dark_mode)
        dark_action.triggered.connect(self.toggle_dark_mode)
        menu.exec_(self.menu_button.mapToGlobal(self.menu_button.rect().bottomRight()))

    def update_clock(self):
        current_time = time.localtime()
        hours = f"{current_time.tm_hour:02d}"
        minutes = f"{current_time.tm_min:02d}"
        seconds = f"{current_time.tm_sec:02d}"

        self.update_circles('h1', int(hours[0]))
        self.update_circles('h2', int(hours[1]))
        self.update_circles('m1', int(minutes[0]))
        self.update_circles('m2', int(minutes[1]))
        self.update_circles('s1', int(seconds[0]))
        self.update_circles('s2', int(seconds[1]))

    def update_circles(self, key, value):
        binary = format(value, f'0{len(self.circles[key])}b')
        for i, bit in enumerate(binary[::-1]):
            circle = self.circles[key][i].scene().items()[0]
            color = self.on_color if bit == '1' else self.off_color
            circle.setBrush(QBrush(color))

    def choose_background(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Hintergrundbild wählen", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.background_image = QPixmap(file_name)
            self.update()

    def toggle_dark_mode(self, checked):
        self.dark_mode = checked
        if self.dark_mode:
            self.on_color = QColor(46, 204, 113)
            self.off_color = QColor(192, 57, 43)
        else:
            self.on_color = QColor(39, 174, 96)
            self.off_color = QColor(231, 76, 60)
        self.update_style()
        self.update_clock()

    def update_style(self):
        style = "background-color: #333333; color: white;" if self.dark_mode else "background-color: #f0f0f0; color: black;"
        self.setStyleSheet(style)
        label_style = "color: white;" if self.dark_mode else "color: black;"
        self.h_label.setStyleSheet(label_style)
        self.m_label.setStyleSheet(label_style)
        self.s_label.setStyleSheet(label_style)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.background_image:
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), self.background_image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = BinaryClockWidget()
    sys.exit(app.exec_())
