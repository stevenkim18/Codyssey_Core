알겠습니다 👍  
요청해주신 대로 문서 내용을 **절대 변경하지 않고**, 보기 좋게 정리해서 그대로 출력해드릴게요.  

---

# 📄 2025 혁신과정 공통문제

### 문제 설명
mission_computer_main.log 파일을 읽어 로그를 가공 출력하는 프로그램을 작성하세요.

---

### 요구사항
- mission_computer_main.log 파일을 읽어 출력형식 요구사항에 맞는 형식으로 출력한다.  
- 파일 없음, 디코딩 오류 등 예외 처리를 구현한다.

---

### 입력 형식
파일을 읽는 함수는 다음과 같이 고정하여 사용합니다.  
과제에서는 항상 인자 없이 **read_log()**를 호출하세요 (기본 파일명만 사용)

```python
def read_log(path:str='mission_computer_main.log') -> str:
    """로그 원문을 읽어 문자열로 변환한다"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    """예외처리 추가"""
```

---

### 출력 형식
총 4회 **print()** 해야 하며, 아래 순서와 형식 그대로 출력하세요.  
자동 채점도 이 순서를 기준으로 합니다.

- 리스트/딕셔너리는 문자열이 아니라 객체 자체를 print() 하세요  
  (예: `print(pairs)`, `print(sorted_pairs)`, `print(result_dict)`)

1. 전체 로그 원문 출력 (그대로 1회)

```
timestamp, event, message
2023-08-27 10:00:00,INFO,Rocket initialization process started.
2023-08-27 10:02:00,INFO,Power systems online. Batteries at optimal charge.
...
2023-08-27 12:00:00,INFO,Center and mission control systems powered down.
```

2. 원본 리스트 출력 – **[(timestamp, message), ...]** 형식의 튜플 리스트 그대로 print()

```python
[('2023-08-27 10:00:00',' Rocket initialization process started.'),
 ('2023-08-27 10:02:00','Power systems online. Batteries at optimal charge.'),
 ...
 ('2023-08-27 12:00:00','Center and mission control systems powered down.')]
```

- event 컬럼은 무시합니다.  
- 파싱 시 `line.split(',', 2)`처럼 최대 2번만 분리하여 message 내 콤마를 보존하세요.  
- 문자열 표기는 파이썬 기본 표기(작은따옴표)가 출력되도록 리스트/튜플 자체를 print() 합니다.  

3. 시간 역순(내림차순) 정렬 리스트 출력 – 2)의 리스트를 timestamp 기준 내림차순으로 정렬 후 그대로 print()

```python
[('2023-08-27 12:00:00','Center and mission control systems powered down.'),
 ('2023-08-27 11:40:00','Oxygen tank explosion.'),
 ...
 ('2023-08-27 10:00:00','Rocket initialization process started.')]
```

4. Dict로 변환하여 출력 – 정렬 리스트를 **{timestamp:message}** 딕셔너리로 변환하여 그대로 print()

```python
{'2023-08-27 12:00:00':'Center and mission control systems powered down.',
 '2023-08-27 11:40:00':'Oxygen tank explosion.',
 ...
 '2023-08-27 10:00:00':'Rocket initialization process started.'}
```

- 키: timestamp 문자열 / 값: message 문자열  
- 중첩 없음, UTF-8, 정상 JSON 포맷  

---

### 예외 처리
- 파일을 열 수 없는 경우 (없음/권한/경로 등):

```
File open error.
```

- 디코딩 오류 발생 시:

```
Decoding error.
```

- 로그 포맷 오류 발생 시:

```
Invalid log format.
```

- 처리 단계 오류 (리스트 변환/정렬/딕셔너리 변환 중 기타 예외):

```
Processing error.
```

- 예외 처리 제약:
  - 반드시 `print()`로 위 메시지를 출력 후 return으로 종료  
  - **exit()/sys.exit 사용 금지**  
  - try-except는 사용 가능하나 메시지는 반드시 동일 문자열 출력  

#### 예외 처리 우선순위
1. 파일 열기 실패 → File open error.  
2. 디코딩 오류 → Decoding error.  
3. 로그 포맷 오류 → Invalid log format.  
4. 처리 단계 오류 → Processing error.  

---

### 개발 환경 설정
- Python 버전: Python 3 이상  
- IDE/에디터: VSCode, Pycharm 혹은 기타 Text editor  

---

### 구현 방식 및 제약 사항
- 파일명은 반드시 **log_analysis.py** 여야 한다.  
- 반드시 다음과 같은 블럭으로 실행됩니다:

```python
if __name__ == "__main__":
    main()
```

- 표준 라이브러리만 사용 (추가 패키지 설치 금지)  
- 모든 파일 입출력은 예외 처리 필수  
- 딕셔너리 구조는 key-value여야 하며 중첩을 허용하지 않음  
- 정렬 기준 타임스탬프는 `'%Y-%m-%d %H:%M:%S'` 형식을 따름  
- 빈 줄은 무시, 각 행을 `split(',', 2)`로 파싱  
- 코딩 컨벤션: PEP 8 준수  
- 문자열은 single quote 사용 (내부에 ‘가 필요한 경우만 “ 사용)  
- 대입문은 `foo = (0, )` 처럼 = 양쪽에 공백  
- 들여쓰기는 공백 사용  

---

📌 원본 문서 내용은 그대로 유지하면서 보기 쉽게 정리했습니다.  
혹시 이걸 바로 **마크다운 파일(.md)** 로 뽑아드릴까요?