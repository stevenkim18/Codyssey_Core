import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt6.QtGui import QFont
from enum import Enum

from decimal import Decimal, DivisionByZero, InvalidOperation

DIV = "÷"
MUL = "×"
class Calculator:
    def __init__(self):
        self.reset()

    def _to_decimal(self, s: str) -> Decimal:
        try:
            return Decimal(s)
        except (InvalidOperation, ValueError):
            return Decimal(0)

    def _fmt(self, d: Decimal) -> str:
        # 소수 끝 0 제거 / 정수면 소수점 제거
        s = format(d, 'f')
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
        return s if s else '0'

    def _apply(self, a: Decimal, op: str, b: Decimal) -> Decimal:
        if op == '+':
            return a + b
        if op == '-':
            return a - b
        if op == '×':
            return a * b
        if op == '÷':
            if b == 0:
                raise DivisionByZero
            return a / b
        return b  # op가 없으면 그냥 현재값

    def reset(self):
        self.acc = Decimal(0)      # 누적값
        self.current = '0'         # 입력 중 문자열
        self.op = None             # 보류 중 연산자('+', '-', '×', '÷')
        self.last_operand = None   # (선택) = 반복 시 사용 가능
        self.error = False

    def input_digit(self, d: str):
        if self.error:
            self.reset()
        if self.current == '0':
            self.current = d
        else:
            self.current += d

    def input_dot(self):
        if self.error:
            self.reset()
        if '.' not in self.current:
            if self.current == '':
                self.current = '0.'
            else:
                self.current += '.'

    def negative_positive(self):
        if self.error:
            self.reset()
        if self.current.startswith('-'):
            self.current = self.current[1:] or '0'
        else:
            if self.current != '0':
                self.current = '-' + self.current

    def percent(self):
        if self.error:
            self.reset()
        x = self._to_decimal(self.current)
        self.current = self._fmt(x / Decimal(100))

    # 공용: 연산자 버튼 처리
    def _commit_op(self, op_symbol: str):
        if self.error:
            self.reset()
        cur_val = self._to_decimal(self.current)

        if self.op is None:
            # 처음 연산자 누름: acc에 현재 입력 반영
            self.acc = cur_val
        else:
            # 이전 보류 연산 수행(중간 계산)
            try:
                self.acc = self._apply(self.acc, self.op, cur_val)
            except DivisionByZero:
                self.error = True
                self.current = 'Error'
                self.op = None
                return

        self.op = op_symbol
        self.current = '0'  # 새 피연산자 입력을 위해 초기화
        self.last_operand = None

    def add(self):      self._commit_op('+')
    def subtract(self): self._commit_op('-')
    def multiply(self): self._commit_op(MUL)
    def divide(self):   self._commit_op(DIV)

    def equal(self):
        if self.error:
            self.reset()
            return

        if self.op is None:
            # 보류 연산이 없으면 현재값 그대로
            return

        cur_val = self._to_decimal(self.current)
        try:
            result = self._apply(self.acc, self.op, cur_val)
        except DivisionByZero:
            self.error = True
            self.current = 'Error'
            self.op = None
            return

        self.acc = result
        self.current = self._fmt(result)
        self.op = None
        self.last_operand = cur_val  # (선택) 이후 반복 '=' 처리 가능

    # UI에서 표시용
    def display_text(self) -> str:
        return self.current if not self.error else 'Error'

    def expression_text(self) -> str:
        # "acc op" 형태로 간단 표시
        if self.op:
            return f"{self._fmt(self.acc)} {self.op}"
        return ""
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
        self.calc = Calculator()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('계산기')
        self.setFixedSize(200, 350)
        
        central = QWidget(self)
        self.setCentralWidget(central)
        
        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(12, 12, 12, 12)  # 바깥 여백
        self.main_layout.setSpacing(6)                      # 위아래 간격
        
        self.expr_label = QLabel("")     # 수식(작은 글씨 영역)
        self.expr_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.expr_label.setFont(QFont("", 14))   # 14pt 정도, 작게
        self.expr_label.setStyleSheet("color: #A6A7A5;") 

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
            btn.clicked.connect(lambda _, t=text: self._handle_button(t))
            self.grid.addWidget(btn, 0, col)  # (행=0, 열=0..3)
        
        buttons_row1 = ["7", "8", "9", "×"]
        for col, text in enumerate(buttons_row1):
            if col == 3:
                btn = self._create_button(text, ButtonType.OPERATOR)
            else:
                btn = self._create_button(text, ButtonType.DIGIT)
            btn.clicked.connect(lambda _, t=text: self._handle_button(t))
            self.grid.addWidget(btn, 1, col)  
            
        buttons_row2 = ["4", "5", "6", "-"]
        for col, text in enumerate(buttons_row2):
            if col == 3:
                btn = self._create_button(text, ButtonType.OPERATOR)
            else:
                btn = self._create_button(text, ButtonType.DIGIT)
            btn.clicked.connect(lambda _, t=text: self._handle_button(t))
            self.grid.addWidget(btn, 2, col)  
            
        buttons_row3 = ["1", "2", "3", "+"]
        for col, text in enumerate(buttons_row3):
            if col == 3:
                btn = self._create_button(text, ButtonType.OPERATOR)
            else:
                btn = self._create_button(text, ButtonType.DIGIT)
            btn.clicked.connect(lambda _, t=text: self._handle_button(t))
            self.grid.addWidget(btn, 3, col)
            
        btn0 = self._create_button("0", ButtonType.DIGIT)
        btn0.setFixedSize(86, 40)   # 두 칸 차지하게 40 + 8(여백) + 40
        btn0.clicked.connect(lambda _, t="0": self._handle_button(t))
        self.grid.addWidget(btn0, 4, 0, 1, 2)  # (row=4, col=0, rowSpan=1, colSpan=2)

        btn_dot = self._create_button(".", ButtonType.DIGIT)
        btn_dot.clicked.connect(lambda _, t=".": self._handle_button(t))
        self.grid.addWidget(btn_dot, 4, 2)

        btn_eq = self._create_button("=", ButtonType.OPERATOR)
        btn_eq.clicked.connect(lambda _, t="=": self._handle_button(t))
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
    
    def _handle_button(self, t: str):
        if t.isdigit():
            self.calc.input_digit(t)
        elif t == ".":
            self.calc.input_dot()
        elif t == "AC":
            self.calc.reset()
        elif t == "+/−":
            self.calc.negative_positive()
        elif t == "%":
            self.calc.percent()
        elif t in ("+", "-", MUL, DIV):
            {
                "+": self.calc.add,
                "-": self.calc.subtract,
                MUL: self.calc.multiply,
                DIV: self.calc.divide,
            }[t]()
        elif t == "=":
            self.calc.equal()

        self._refresh_display()

    def _refresh_display(self):
        self.result_label.setText(self.calc.display_text())
        self.expr_label.setText(self.calc.expression_text())
    

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = CalcalutorApp()
   ex.show()
   sys.exit(app.exec())
        