import numpy as np 

MARS_BASE_MAIN_PARTS_001 = "mars_base_main_parts-001.csv"
MARS_BASE_MAIN_PARTS_002 = "mars_base_main_parts-002.csv"
MARS_BASE_MAIN_PARTS_003 = "mars_base_main_parts-003.csv"
PARTS_TO_WORK_ON = "parts_to_work_on.csv"

def read_csv_file(filename):
    """ CSV 파일을 읽어서 NumPy 배열로 반환하는 간단한 함수 """
    try:
        return np.genfromtxt(filename, delimiter=",", encoding="utf-8-sig", names=True, dtype=None)
    except FileNotFoundError:
        print(f"오류: '{filename}' 파일을 찾을 수 없습니다.")
        raise
    

def main():
    try:
        # 1
        arr1 = read_csv_file(MARS_BASE_MAIN_PARTS_001)
        arr2 = read_csv_file(MARS_BASE_MAIN_PARTS_002)
        arr3 = read_csv_file(MARS_BASE_MAIN_PARTS_003)
        # print(arr1, arr2, arr3)

        # 2
        part_names = arr1['parts']
        strengths = np.vstack([
            arr1['strength'],
            arr2['strength'],
            arr3['strength']
        ]).T  # shape: (n_parts, 3)

        parts = np.column_stack((part_names, strengths.astype(int)))
        
        # 3
        row_means = strengths.mean(axis=1).astype(float)
        parts_with_mean = np.column_stack((part_names, row_means))
        
        # 4-1
        filtered = parts_with_mean[row_means < 50]

        # 4-2
        np.savetxt(
            PARTS_TO_WORK_ON,
            filtered,
            delimiter=",",
            fmt="%s",
            header="parts,mean_strength",
            comments=""
        )

        # 보너스 1
        parts2 = np.genfromtxt(
            PARTS_TO_WORK_ON,
            delimiter=",",
            encoding="utf-8-sig",
            names=True,
            dtype=None
        )
        
        # 보너스 2
        parts3 = np.array([parts2[name] for name in parts2.dtype.names]).T
        print(parts3)

    except Exception as e:
        print(f"에러 발생: {e}")
    
if __name__ == "__main__":
    main()