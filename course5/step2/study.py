import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt6.QtGui import QFont
from enum import Enum

class ButtonType(Enum):
    DIGIT = 1
    OPERATOR =2
    FUNCTION = 3
    
    @property
    def bg_color(self):
        if self is ButtonType.OPERATOR:
            return "#FF9502"
        elif self is ButtonType.FUNCTION:
            return "#989696"
        else:  # DIGIT
            return "#555555"

    @property
    def bg_pressed(self):
        if self is ButtonType.OPERATOR:
            return "#FCC78D"
        elif self is ButtonType.FUNCTION:
            return "#A9A7A6"
        else:
            return "#767676"

class CalcalutorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.display_text = "0"
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('계산기')
        self.setFixedSize(200, 350)
        
        central = QWidget(self)
        self.setCentralWidget(central)
        
        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(12, 12, 12, 12)  # 바깥 여백
        self.main_layout.setSpacing(6)                      # 위아래 간격
        
        self.expr_label = QLabel("1")     # 수식(작은 글씨 영역)
        self.expr_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.expr_label.setFont(QFont("", 14))   # 14pt 정도, 작게

        self.result_label = QLabel("0")  # 결과(큰 글씨 영역)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.result_label.setFont(QFont("", 32))  # 36pt 정도, 크게

        display_layout = QVBoxLayout()
        display_layout.setContentsMargins(4, 8, 8, 8)  # 디스플레이 영역 안쪽 여백
        display_layout.setSpacing(6)                   # 수식과 결과 라벨 사이 간격
        display_layout.addWidget(self.expr_label)
        display_layout.addWidget(self.result_label)

        self.main_layout.addLayout(display_layout)
        
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(12)
        self.grid.setVerticalSpacing(6)

        self.main_layout.addLayout(self.grid)
        
        buttons_row0 = ["AC", "+/−", "%", "÷"]
        for col, text in enumerate(buttons_row0):
            if col == 3:
                btn = self._create_button(text, ButtonType.OPERATOR)
            else:
                btn = self._create_button(text, ButtonType.FUNCTION)
            self.grid.addWidget(btn, 0, col)  # (행=0, 열=0..3)
        
        buttons_row1 = ["7", "8", "9", "×"]
        for col, text in enumerate(buttons_row1):
            if col == 3:
                btn = self._create_button(text, ButtonType.OPERATOR)
            else:
                btn = self._create_button(text, ButtonType.DIGIT)
            self.grid.addWidget(btn, 1, col)  
            
        buttons_row2 = ["4", "5", "6", "-"]
        for col, text in enumerate(buttons_row2):
            if col == 3:
                btn = self._create_button(text, ButtonType.OPERATOR)
            else:
                btn = self._create_button(text, ButtonType.DIGIT)
            self.grid.addWidget(btn, 2, col)  
            
        buttons_row3 = ["1", "2", "3", "+"]
        for col, text in enumerate(buttons_row3):
            if col == 3:
                btn = self._create_button(text, ButtonType.OPERATOR)
            else:
                btn = self._create_button(text, ButtonType.DIGIT)
            self.grid.addWidget(btn, 3, col)
            
        btn0 = self._create_button("0", ButtonType.DIGIT)
        btn0.setFixedSize(86, 40)   # 두 칸 차지하게 40 + 8(여백) + 40
        self.grid.addWidget(btn0, 4, 0, 1, 2)  # (row=4, col=0, rowSpan=1, colSpan=2)

        btn_dot = self._create_button(".", ButtonType.DIGIT)
        self.grid.addWidget(btn_dot, 4, 2)

        btn_eq = self._create_button("=", ButtonType.OPERATOR)
        self.grid.addWidget(btn_eq, 4, 3)
    
    def _create_button(self, text, button_type=ButtonType.DIGIT, size=40):
        btn = QPushButton(text)
        btn.setFixedSize(size, size)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {button_type.bg_color};
                color: #ffffff;
                font-size: 16px;
                border-radius: {size//2}px;
            }}
            QPushButton:pressed {{
                background-color: {button_type.bg_pressed}
            }}
        """)
        return btn
    

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = CalcalutorApp()
   ex.show()
   sys.exit(app.exec())
        
        