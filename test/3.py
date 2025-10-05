
# 문제에 해당 함수 포맷이 나옵니다.
# 4번 문제는 따로 함수를 검사하는 것으로 보아, 이 함수도 따로 검사를 하는 것 같습니다.
# 그래서 반드시 순서대로 예외처리를 해주세요
# 1. FileNotFoundError - 파일 없음
# 2. UnicodeDecodeError - 인코딩 문제
# 3. Exception - 그외 기타
def read_log(path:str='mission_computer_main.log') -> str:
    """로그 원문을 읽어 문자열로 변환한다"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise
    except UnicodeDecodeError:
        raise
    except Exception:
        raise
    
def log_to_tuple(log):
    raw_data = log.strip()
    
    logs = raw_data.split('\n')
    
    #1. 헤더 검사
    if logs[0] != 'timestamp,event,message':
        raise ValueError
    
    pairs = []
    
    for line in logs[1:]:
        if line.strip():
            parts = line.split(',', 2)
            # 2. 3개 있는지 검사
            if len(parts) != 3:
                raise ValueError
            
            # 3. 타임스탬프 검사
            # 타임 스탬프는 datetime을 사용해도 되나 모든 포맷이 19글자입니다.
            # 따라서 19글자인지 아닌지만 확인해주어도 저도 통과되었습니다.
            # 불안하신 분들은 datetime 모듈을 사용해서 타임스탬프를 검사해주세요.
            if len(parts[0]) != 19:
                raise ValueError
            
            pairs.append((parts[0], parts[2]))
            
    return pairs

def sort_log(tuples):
    return sorted(tuples, key=lambda x: x[0])

def log_to_dict(tuples):
    result = {}
    
    for timestamp, message in tuples:
        result[timestamp] = message
    
    return result
            
def main():
    
    try:
        log = read_log()

        # 1. 첫번째 출력
        print(log)

        tuples = log_to_tuple(log)

        # 2. 두번째 출력
        print(tuples)

        sorted_tuples = sort_log(tuples)

        # 3. 세번째 출력
        print(sorted_tuples)

        dict_log = log_to_dict(sorted_tuples)

        # 4. 네번째 출력
        print(dict_log)
    
    # 에러도 아래와 같은 순서대로 처리해주세요.
    # 문제에 나와있습니다.
    except FileNotFoundError:
        print("File open error.")
        return
    except UnicodeDecodeError:
        print("Decoding error.")
        return
    except ValueError:
        print("Invalid log format.")
        return
    except Exception:
        print("Processing error.")
        return

if __name__ == '__main__':
    main()