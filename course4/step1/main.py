from datetime import datetime
import json

LOG_FILE_NAME = "mission_computer_main.log"
JSON_FILE_NAME = "mission_computer_main.json"
DANGEROUS_LOG_FILE_NAME = "dangerous_logs.log"

# MARK: 테스트
def print_test_text():
    """
    환경 테스트를 위한 함수
    """
    print("Hello Mars")
    
def read_log_file(filename):
    """
    로그 파일을 읽어서 전체 내용을 반환
    """
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            print('=== 로그 파일 전체 내용 ===')
            print(content)
            return content
    except FileNotFoundError:
        print(f'오류: {filename} 파일을 찾을 수 없습니다.')
        raise
    except UnicodeDecodeError:
        print(f'오류: {filename} 파일 디코딩에 실패했습니다.')
        raise
    except Exception as e:
        print(f'오류: 파일 읽기 중 예상치 못한 오류가 발생했습니다: {e}')
        raise
    
def parse_log_to_list(content):
    """
    로그 내용을 파싱하여 리스트로 변환
    """
    log_list = []
    lines = content.strip().split('\n')
    
    # 헤더 라인 건너뛰기
    for line in lines[1:]:
        if line.strip():
            parts = line.split(',', 2)
            if len(parts) >= 3:
                timestamp = parts[0].strip()
                event = parts[1].strip()
                message = parts[2].strip()
                
                log_entry = {
                    'timestamp': timestamp,
                    'event': event,
                    'message': message
                }
                log_list.append(log_entry)
    
    print('\n=== 파싱된 로그 리스트 ===')
    for entry in log_list:
        print(entry)
    
    return log_list

def sort_log_by_time_desc(log_list):
    """
    로그 리스트를 시간 역순으로 정렬
    """
    try:
        sorted_list = sorted(log_list, 
                             key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S'), 
                             reverse=True)
        
        print('\n=== 시간 역순 정렬된 로그 ===')
        for entry in sorted_list:
            print(entry)
        
        return sorted_list
    except ValueError as e:
        print(f'오류: 시간 형식 파싱 중 오류 발생: {e}')
        raise
    
def sort_log_by_time_desc(log_list):
    """
    로그 리스트를 시간 역순으로 정렬
    """
    try:
        sorted_list = sorted(log_list, 
                           key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S'), 
                           reverse=True)
        
        print('\n=== 시간 역순 정렬된 로그 ===')
        for entry in sorted_list:
            print(entry)
        
        return sorted_list
    except ValueError as e:
        print(f'오류: 시간 형식 파싱 중 오류 발생: {e}')
        raise

def save_to_json(data, filename):
    """
    딕셔너리 데이터를 JSON 파일로 저장
    
    Args:
        data (dict): 저장할 데이터
        filename (str): 저장할 파일명
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f'\n=== JSON 파일 저장 완료: {filename} ===')
    except Exception as e:
        print(f'오류: JSON 파일 저장 중 오류 발생: {e}')
        raise

# MARK: 보너스 함수
def filter_dangerous_logs(log_list):
    """
    위험 키워드가 포함된 로그만 필터링
    """
    dangerous_keywords = ['폭발', '누출', '고온', 'oxygen', 'explosion', 'unstable']
    dangerous_logs = []
    
    for entry in log_list:
        message_lower = entry['message'].lower()
        if any(keyword.lower() in message_lower for keyword in dangerous_keywords):
            dangerous_logs.append(entry)
    
    print(f'\n=== 위험 키워드 필터링 결과: {len(dangerous_logs)}개 발견 ===')
    for entry in dangerous_logs:
        print(entry)
    
    return dangerous_logs


def save_dangerous_logs(dangerous_logs, filename):
    """
    위험 로그를 별도 파일로 저장
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('위험 키워드가 포함된 로그\n')
            file.write('=' * 50 + '\n\n')
            for entry in dangerous_logs:
                file.write(f"시간: {entry['timestamp']}\n")
                file.write(f"이벤트: {entry['event']}\n")
                file.write(f"메시지: {entry['message']}\n")
                file.write('-' * 30 + '\n')
        print(f'위험 로그가 {filename}에 저장되었습니다.')
    except Exception as e:
        print(f'오류: 위험 로그 저장 중 오류 발생: {e}')

def search_logs(json_filename, search_term):
    """
    JSON 파일에서 특정 문자열을 포함한 로그 검색
    """
    try:
        with open(json_filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        matching_logs = []
        for entry in data:
            if search_term.lower() in entry['message'].lower():
                matching_logs.append(entry)
        
        print(f'\n=== "{search_term}" 검색 결과: {len(matching_logs)}개 발견 ===')
        for entry in matching_logs:
            print(f"[{entry['timestamp']}] {entry['event']}: {entry['message']}")
            
    except FileNotFoundError:
        print(f'오류: {json_filename} 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'오류: 검색 중 오류 발생: {e}')


# MARK: Main
def main():
    
    print_test_text()
    
    try:
        # 2-2, 2-3 로그 파일 출력, 예외처리
        content = read_log_file(LOG_FILE_NAME)
        
        # 2-4, 2-5 리스트 객체, 출력
        log_list = parse_log_to_list(content)
        
        # 2-6 시간 역순
        sort_log_list = sort_log_by_time_desc(log_list)
        
        # 2-7 이미 리스트 안에 딕셔너리로 저장
        
        # 2-8 json파일로 저장
        save_to_json(sort_log_list, JSON_FILE_NAME)
        
        # 보너스 위함한 키워드 추출
        dangerous_logs = filter_dangerous_logs(log_list)
        if dangerous_logs:
            save_dangerous_logs(dangerous_logs, DANGEROUS_LOG_FILE_NAME)
        else:
            print('위험 키워드가 포함된 로그가 없습니다.')
            
        # 보너스 검색
        search_keyword = input("search: ")
        
        search_logs(JSON_FILE_NAME, search_keyword)

    except Exception as e:
        print(f'프로그램 실행 중 오류 발생: {e}')

if __name__ == "__main__":
    main()