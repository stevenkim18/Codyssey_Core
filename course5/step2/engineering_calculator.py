import sys
import math
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt6.QtGui import QFont
from enum import Enum
from decimal import Decimal, DivisionByZero, InvalidOperation
from calculator import Calculator

class EngineeringCalculator(Calculator):
    def __init__(self):
        super().__init__()
    
    def sin_func(self):
        if self.error:
            self.reset()
        try:
            x = float(self.current)
            # 도를 라디안으로 변환
            result = math.sin(math.radians(x))
            self.current = self._fmt(Decimal(str(result)))
        except (ValueError, InvalidOperation):
            self.error = True
            self.current = 'Error'
    
    def cos_func(self):
        if self.error:
            self.reset()
        try:
            x = float(self.current)
            # 도를 라디안으로 변환
            result = math.cos(math.radians(x))
            self.current = self._fmt(Decimal(str(result)))
        except (ValueError, InvalidOperation):
            self.error = True
            self.current = 'Error'
    
    def tan_func(self):
        if self.error:
            self.reset()
        try:
            x = float(self.current)
            # 도를 라디안으로 변환
            result = math.tan(math.radians(x))
            self.current = self._fmt(Decimal(str(result)))
        except (ValueError, InvalidOperation):
            self.error = True
            self.current = 'Error'
    
    def sinh_func(self):
        if self.error:
            self.reset()
        try:
            x = float(self.current)
            result = math.sinh(x)
            self.current = self._fmt(Decimal(str(result)))
        except (ValueError, InvalidOperation):
            self.error = True
            self.current = 'Error'
    
    def cosh_func(self):
        if self.error:
            self.reset()
        try:
            x = float(self.current)
            result = math.cosh(x)
            self.current = self._fmt(Decimal(str(result)))
        except (ValueError, InvalidOperation):
            self.error = True
            self.current = 'Error'
    
    def tanh_func(self):
        if self.error:
            self.reset()
        try:
            x = float(self.current)
            result = math.tanh(x)
            self.current = self._fmt(Decimal(str(result)))
        except (ValueError, InvalidOperation):
            self.error = True
            self.current = 'Error'
    
    def pi_func(self):
        if self.error:
            self.reset()
        self.current = self._fmt(Decimal(str(math.pi)))
    
    def square_func(self):
        if self.error:
            self.reset()
        try:
            x = self._to_decimal(self.current)
            result = x * x
            self.current = self._fmt(result)
        except (InvalidOperation):
            self.error = True
            self.current = 'Error'
    
    def cube_func(self):
        if self.error:
            self.reset()
        try:
            x = self._to_decimal(self.current)
            result = x * x * x
            self.current = self._fmt(result)
        except (InvalidOperation):
            self.error = True
            self.current = 'Error'

class ButtonType(Enum):
    DIGIT = 1
    OPERATOR = 2
    FUNCTION = 3
    SCIENTIFIC = 4
    
    @property
    def bg_color(self):
        if self is ButtonType.OPERATOR:
            return "#FF9502"
        elif self is ButtonType.FUNCTION:
            return "#505050"
        elif self is ButtonType.SCIENTIFIC:
            return "#505050"
        else:  # DIGIT
            return "#333333"

    @property
    def bg_pressed(self):
        if self is ButtonType.OPERATOR:
            return "#FCC78D"
        elif self is ButtonType.FUNCTION:
            return "#707070"
        elif self is ButtonType.SCIENTIFIC:
            return "#707070"
        else:
            return "#555555"

class EngineeringCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.display_text = "0"
        self.calc = EngineeringCalculator()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('공학용 계산기')
        self.setFixedSize(500, 320)
        
        central = QWidget(self)
        self.setCentralWidget(central)
        
        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.setSpacing(6)
        
        # 디스플레이 영역
        self.result_label = QLabel("0")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.result_label.setFont(QFont("", 24))
        self.result_label.setStyleSheet("color: white; background-color: #1C1C1C; padding: 10px; border-radius: 5px;")
        self.result_label.setMinimumHeight(60)
        
        self.main_layout.addWidget(self.result_label)
        
        # 버튼 그리드
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(6)
        self.grid.setVerticalSpacing(6)
        
        self.main_layout.addLayout(self.grid)
        
        # 버튼 정의 (6행 x 10열)
        buttons = [
            # Row 0
            [("(", ButtonType.FUNCTION), (")", ButtonType.FUNCTION), ("mc", ButtonType.FUNCTION), ("m+", ButtonType.FUNCTION), ("m-", ButtonType.FUNCTION), ("mr", ButtonType.FUNCTION), ("AC", ButtonType.FUNCTION), ("+/−", ButtonType.FUNCTION), ("%", ButtonType.FUNCTION), ("÷", ButtonType.OPERATOR)],
            # Row 1  
            [("2ⁿᵈ", ButtonType.SCIENTIFIC), ("x²", ButtonType.SCIENTIFIC), ("x³", ButtonType.SCIENTIFIC), ("xʸ", ButtonType.SCIENTIFIC), ("eˣ", ButtonType.SCIENTIFIC), ("10ˣ", ButtonType.SCIENTIFIC), ("7", ButtonType.DIGIT), ("8", ButtonType.DIGIT), ("9", ButtonType.DIGIT), ("×", ButtonType.OPERATOR)],
            # Row 2
            [("¹/ₓ", ButtonType.SCIENTIFIC), ("²√x", ButtonType.SCIENTIFIC), ("³√x", ButtonType.SCIENTIFIC), ("ʸ√x", ButtonType.SCIENTIFIC), ("ln", ButtonType.SCIENTIFIC), ("log₁₀", ButtonType.SCIENTIFIC), ("4", ButtonType.DIGIT), ("5", ButtonType.DIGIT), ("6", ButtonType.DIGIT), ("-", ButtonType.OPERATOR)],
            # Row 3
            [("x!", ButtonType.SCIENTIFIC), ("sin", ButtonType.SCIENTIFIC), ("cos", ButtonType.SCIENTIFIC), ("tan", ButtonType.SCIENTIFIC), ("e", ButtonType.SCIENTIFIC), ("EE", ButtonType.SCIENTIFIC), ("1", ButtonType.DIGIT), ("2", ButtonType.DIGIT), ("3", ButtonType.DIGIT), ("+", ButtonType.OPERATOR)],
            # Row 4
            [("sinh", ButtonType.SCIENTIFIC), ("cosh", ButtonType.SCIENTIFIC), ("tanh", ButtonType.SCIENTIFIC), ("π", ButtonType.SCIENTIFIC), ("Rad", ButtonType.SCIENTIFIC), ("Rand", ButtonType.SCIENTIFIC), ("0", ButtonType.DIGIT), (".", ButtonType.DIGIT), ("=", ButtonType.OPERATOR)]
        ]
        
        # 버튼 생성 및 배치
        for row, button_row in enumerate(buttons):
            for col, (text, btn_type) in enumerate(button_row):
                if text:  # 빈 버튼이 아닌 경우
                    if row == 4 and col == 6 and text == "0":  # 마지막 행의 "0" 버튼은 두 칸 차지
                        btn = self._create_button(text, btn_type, width=86)
                        btn.clicked.connect(lambda _, t=text: self._handle_button(t))
                        self.grid.addWidget(btn, row, col, 1, 2)
                    elif row == 4 and col > 6:
                        btn = self._create_button(text, btn_type)
                        btn.clicked.connect(lambda _, t=text: self._handle_button(t))
                        self.grid.addWidget(btn, row, col+1)
                    else:
                        btn = self._create_button(text, btn_type)
                        btn.clicked.connect(lambda _, t=text: self._handle_button(t))
                        self.grid.addWidget(btn, row, col)
    
    def _create_button(self, text, button_type=ButtonType.DIGIT, width=40, height=35):
        btn = QPushButton(text)
        btn.setFixedSize(width, height)
        
        font_size = "12px" if len(text) > 2 else "14px"
        
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {button_type.bg_color};
                color: #ffffff;
                font-size: {font_size};
                border-radius: {height//2}px;
                font-weight: normal;
            }}
            QPushButton:pressed {{
                background-color: {button_type.bg_pressed};
            }}
        """)
        return btn
    
    def _handle_button(self, text: str):
        # 기본 계산기 기능
        if text.isdigit():
            self.calc.input_digit(text)
        elif text == ".":
            self.calc.input_dot()
        elif text == "AC":
            self.calc.reset()
        elif text == "+/−":
            self.calc.negative_positive()
        elif text == "%":
            self.calc.percent()
        elif text in ("+", "-", "×", "÷"):
            {
                "+": self.calc.add,
                "-": self.calc.subtract,
                "×": self.calc.multiply,
                "÷": self.calc.divide,
            }[text]()
        elif text == "=":
            self.calc.equal()
        # 공학용 계산기 기능
        elif text == "sin":
            self.calc.sin_func()
        elif text == "cos":
            self.calc.cos_func()
        elif text == "tan":
            self.calc.tan_func()
        elif text == "sinh":
            self.calc.sinh_func()
        elif text == "cosh":
            self.calc.cosh_func()
        elif text == "tanh":
            self.calc.tanh_func()
        elif text == "π":
            self.calc.pi_func()
        elif text == "x²":
            self.calc.square_func()
        elif text == "x³":
            self.calc.cube_func()
        else:
            # 아직 구현되지 않은 기능들
            print(f"Button '{text}' clicked")
        
        self._refresh_display()
    
    def _refresh_display(self):
        self.result_label.setText(self.calc.display_text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow {
            background-color: #1C1C1C;
        }
        QWidget {
            background-color: #1C1C1C;
        }
    """)
    ex = EngineeringCalculatorApp()
    ex.show()
    sys.exit(app.exec())