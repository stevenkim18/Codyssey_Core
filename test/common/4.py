import math

def sphere_area(diameter: float, material: str, thickness: float = 1.0) -> tuple[float, float]:
     
    # 이미 입력을 받는 곳에서 예외처리를 해서 매개변수로 들어오는 값이 검증이 되지만
    # 기계 채점에서는 따로 함수를 분리해서 검사하는 것 같습니다.
    # 그래서 매개변수에 대한 예외처리를 해주시고 예외 발생하면 ValueError를 던지세요.
    if diameter <= 0:
        raise ValueError
    if material not in ['유리', '알루미늄', '탄소강']:
        raise ValueError
    if thickness <= 0:
        raise ValueError
    
    # ‼️ 계산식은 문제에 있습니다. 문제의 식을 고대로 코드로 작성하세요(매우 쉽습니다)
    # 아래 계산식은 제가 임의로 복기한 것입니다. 정확하지 않을 수 있습니다.
    # 그냥 참고하는 용도로만 봐주세요!
    
    densities = {
        '유리': 2.4,      # g/cm³
        '알루미늄': 2.7,  # g/cm³
        '탄소강': 7.85     # g/cm³
    }

    area_m2 = math.pi * (diameter * diameter)
    area_cm2 = area_m2 * 10000  # m² to cm²
    
    # 질량 영어로 
    mass = densities[material] * area_cm2 * thickness  # g
    
    # 화성에서의 무게
    weight_on_mars = mass * 0.38  # g
    
    # 요구사항에서 2개의 float 값을 리턴하라고 제시합니다.
    return (area_m2, weight_on_mars)

def main():
    
    try:
        # 입력1. 지름 입력 숫자(float)으로 받고 0보다 작을 때 예외처리
        diameter = float(input("구의 지름을 입력하세요 (cm): "))
        
        if diameter <= 0:
            raise ValueError
        
        # 입력2. 재질 입력 (유리/알루미늄/탄소강) 중 하나로 받고 아닐 때 예외처리
        material = input("재질을 입력하세요(유리/알루미뉼/탄소강)").strip()
        
        if material not in ['유리', '알루미늄', '탄소강']:
            raise ValueError
        
        # 입력3. 두께 입력 숫자(float)으로 받고 빈 문자열 일때는 1.0으로 처리. (0보다 작을 때도 예외처리)
        thickness_input = input("두께를 입력하세요 (기본값 1.0 cm, 생략 가능): ").strip()
        thickness = float(thickness_input) if thickness_input else 1.0
        
        if thickness <= 0:
            raise ValueError
        
        area, weight = sphere_area(diameter, material, thickness)
        
        # 지름, 두께는 :g로 출력 -> 10.0 -> 10으로 출력
        # 면적 무게는 .3f로 출력
        # 모두 문제에 나옵니다(조금 어지럽게 나오기는 해요)
        print(f"재질 ⇒ {material}, 지름 ⇒ {diameter:g}, 두께 ⇒ {thickness:g}, 면적 ⇒ {area:.3f}, 무게 ⇒ {weight:.3f} kg")
    
    # ValueError와 그 외 에러(Exception)으로 처리하라고 나옵니다.
    # 에러 처리 문구도 문제를 참고해주세요.   
    except ValueError:
        print("Invlid input.")
    except Exception:
        print("error")

if __name__ == '__main__':
    main()