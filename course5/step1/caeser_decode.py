# caesar_decode.py

def _shift_char(ch: str, shift: int) -> str:
    """단일 문자에 대해 Caesar 디코드(왼쪽으로 shift) 적용."""
    if 'a' <= ch <= 'z':
        base = ord('a')
        return chr((ord(ch) - base - shift) % 26 + base)
    if 'A' <= ch <= 'Z':
        base = ord('A')
        return chr((ord(ch) - base - shift) % 26 + base)
    return ch  

def caesar_cipher_decode(target_text: str) -> list[tuple[int, str]]:
    """
    target_text에 대해 0~25까지 모든 자리수(shift)를 적용해
    (shift, 해독문) 리스트를 반환.
    """
    results: list[tuple[int, str]] = []
    for shift in range(26):
        decoded = ''.join(_shift_char(ch, shift) for ch in target_text)
        results.append((shift, decoded))
    return results

def main():
    try:
        with open('password 2.txt', 'r', encoding='utf-8') as f:
            cipher_text = f.read().strip()
    except FileNotFoundError:
        print('password.txt 파일을 찾을 수 없습니다.')
        return

    if not cipher_text:
        print('password.txt 내용이 비어 있습니다.')
        return

    print(f'대상 문자열: {cipher_text!r}\n')

    results = caesar_cipher_decode(cipher_text)
    for shift, decoded in results:
        print(f'[{shift:2}] {decoded}')

    sel = input('\n정답으로 보이는 "자리수(0~25)"를 입력하세요. 건너뛰려면 엔터: ').strip()
    if not sel:
        print('저장을 건너뜁니다.')
        return

    try:
        k = int(sel)
    except ValueError:
        print('숫자(0~25)로 입력해 주세요.')
        return

    if not (0 <= k <= 25):
        print('자리수는 0~25 범위여야 합니다.')
        return

    final_text = results[k][1]
    with open('result.txt', 'w', encoding='utf-8') as f:
        f.write(final_text)

    print(f'result.txt에 저장 완료! (자리수 shift={k})')

if __name__ == '__main__':
    main()