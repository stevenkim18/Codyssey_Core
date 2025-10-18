## 문제
### 단순 연결 리스트와 원형 연결 리스트를 구하는 문제

#### 연결 리스트(Linked List) 요구사항
클래스 이름: linkedList

1. 임의 위치 삽입
```python
insert(self, index: int, value: Any) -> None
```
- 0 <= index <= len이 아니면 Index Error

2. 삭제
```python
delete(self index: int) -> object
```
- 삭제를 하고 삭제한 노드 리턴
- 에러 처리 Index Error

3. 전체 출력
```python
to_list(self) -> list
```
- 맨 앞에서 뒤까지 리스트를 리턴

4. 전체 길이
```python
__len__(self) ->
```
- 노드 수

예시 출력
```
0
[A, C, B]
C
[A, B]
2
```

#### 원형 연결 리스트(Circular Linked List)
클래스 이름: Circular List
1. 커서 기반 삽입
```python
insert(self, value: Any) -> None
```
- 비어 있으면 단일 노드
- 이미 있으면 커서 뒤에 삽입 후, 커서를 새 노드로 이동

2. 가장 먼저 찾은 것 삭제
```python
delete(self, value: Any) -> bool
```
- 커서 위치 기준으로 첫번째로 찾는 노드 삭제
- 삭제 후에 커서는 이전 노드로

3. 다음 노드로 이동
```python
get_next(self) -> object | None
```
- 비어 있으면 None
- 커서 다음 노드로 이동 후 리턴

4. 검색
```python
search(self, value: Any) -> bool
```
- 있으면 true, 없으면 false

예시 출력
```
None
True
False
[A, B, C, A, B]
True
[C, A, C, A]
False
```

파일명: linked_lists.py

