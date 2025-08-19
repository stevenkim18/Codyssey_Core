import numpy as np

MARS_BASE_INVENTORY_LIST = "Mars_Base_Inventory_List.csv"
MARS_BASE_INVENTORY_DANGER = "Mars_Base_Inventory_danger.csv"

def is_float(s: str) -> bool:
    """문자열이 실수인지 확인"""
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_csv_file(filename):
    """CSV 파일을 읽어서 문자열로 반환"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f'오류: {filename} 파일을 찾을 수 없습니다.')
        return None
    except Exception as e:
        print(f'파일 읽기 오류: {e}')
        return None
    
def parse_csv_content_to_list(content):
    """csv 데이터를 딕셔너리로 된 리스트로 변환"""
    lines = content.strip().split("\n")
    headers = [h.strip() for h in lines[0].split(',')]
    
    data_list = []
    for line in lines[1:]:
        row_dict = {}
        fields = [field.strip() for field in line.split(',')]
        for i, field in enumerate(fields):
            if is_float(field):
                field = float(field)
            row_dict[headers[i]] = field
        data_list.append(row_dict)
    
    return data_list

def sort_by_flammability(data_list):
    """Flammability 내림차순으로 정렬"""
    return sorted(data_list, key=lambda x: x['Flammability'], reverse=True)
    
def filter_high_flammability(data_list):
    """인화성 지수가 0.7 이상인 항목만 필터링"""
    return [item for item in data_list if item['Flammability'] >= 0.7]

def dict_list_to_csv(data_list, filename):
    headers = list(data_list[0].keys())
    
    with open(filename, 'w', encoding='utf-8') as file:
        # 헤더 쓰기
        file.write(','.join(headers) + '\n')
        
        # 데이터 쓰기
        for item in data_list:
            row = []
            for header in headers:
                value = item[header]
                row.append(str(value))
            file.write(','.join(row) + '\n')
        
    print(f'성공적으로 {filename} 파일에 저장되었습니다.')
    print(f'총 {len(data_list)}개의 항목이 저장되었습니다.')

def main():
    # 1-1 파일 읽기 및 출력
    content = read_csv_file(MARS_BASE_INVENTORY_LIST)
    
    print("===========csv 파일 읽고 출력===========")
    print(content)
    
    # 1-2 콤마로 구분하여 리스트 객체로 변환
    data_list = parse_csv_content_to_list(content)
    
    # 1-3 인화성 지수가 내림 차순으로 정렬
    sorted_list = sort_by_flammability(data_list)
    
    # 1-4 
    filtered_list = filter_high_flammability(sorted_list)
    print("===========flammability 0.7 이상 항목 출력===========")
    for row in filtered_list:
        print(row)
    
    # 1-5 필터링된 결과 csv 파일로 저장
    dict_list_to_csv(filtered_list, MARS_BASE_INVENTORY_DANGER)
    
    
if __name__ == "__main__":
    main()