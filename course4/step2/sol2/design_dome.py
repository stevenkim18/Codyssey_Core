import math

# 전역 변수
MARS_GRAVITY = 0.38  # 화성 중력 (지구 중력의 0.38배)
MATERIAL_DENSITIES = {
    'glass': 2.4,      # g/cm³
    'aluminum': 2.7,   # g/cm³
    'carbon_steel': 7.85  # g/cm³
}

# 결과 저장용 전역 변수
dome_material = ''
dome_diameter = 0.0
dome_thickness = 0.0
dome_area = 0.0
dome_weight = 0.0

def sphere_area(diameter, material, thickness=1.0):
    """
    반구체 돔의 표면적과 무게를 계산하는 함수
    
    Parameters:
    - diameter: 지름 (m)
    - material: 재질 ('glass', 'aluminum', 'carbon_steel')
    - thickness: 두께 (cm, 기본값 1cm)
    
    Returns:
    - tuple: (표면적(m²), 무게(kg))
    """
    global dome_material, dome_diameter, dome_thickness, dome_area, dome_weight
    
    try:
        # 입력 검증
        if not isinstance(diameter, (int, float)):
            raise TypeError('지름은 숫자여야 합니다.')
        if not isinstance(thickness, (int, float)):
            raise TypeError('두께는 숫자여야 합니다.')
        if not isinstance(material, str):
            raise TypeError('재질은 문자열이어야 합니다.')
        
        # 값 검증
        if diameter <= 0:
            raise ValueError('지름은 0보다 큰 값이어야 합니다.')
        if thickness <= 0:
            raise ValueError('두께는 0보다 큰 값이어야 합니다.')
        
        # 재질 검증
        material_lower = material.lower()
        if material_lower not in MATERIAL_DENSITIES:
            valid_materials = ', '.join(MATERIAL_DENSITIES.keys())
            raise ValueError(f'유효하지 않은 재질입니다. 가능한 재질: {valid_materials}')
        
        # 반구체 표면적 계산: 2πr² (반구의 곡면 + 밑면)
        radius = diameter / 2
        surface_area = 2 * math.pi * (radius ** 2)  # m²
        
        # 부피 계산 (껍질 부피)
        # 큰 반구 부피 - 작은 반구 부피
        thickness_m = thickness / 100  # cm를 m로 변환
        outer_radius = radius
        inner_radius = radius - thickness_m
        
        if inner_radius <= 0:
            inner_radius = 0  # 두께가 반지름보다 클 경우
        
        # 반구 부피 = (2/3) * π * r³
        outer_volume = (2/3) * math.pi * (outer_radius ** 3)
        inner_volume = (2/3) * math.pi * (inner_radius ** 3)
        shell_volume = outer_volume - inner_volume  # m³
        
        # 무게 계산
        density = MATERIAL_DENSITIES[material_lower]  # g/cm³
        density_kg_m3 = density * 1000  # kg/m³로 변환
        
        # 지구에서의 무게
        earth_weight = shell_volume * density_kg_m3  # kg
        
        # 화성에서의 무게 (* 0.38)
        mars_weight = earth_weight * MARS_GRAVITY  # kg
        
        # 전역 변수에 저장
        dome_material = material_lower
        dome_diameter = diameter
        dome_thickness = thickness
        dome_area = surface_area
        dome_weight = mars_weight
        
        return surface_area, mars_weight
        
    except (TypeError, ValueError) as e:
        raise e
    except Exception as e:
        raise ValueError(f'계산 중 오류가 발생했습니다: {e}')


def get_user_input():
    """사용자로부터 입력을 받는 함수"""
    try:
        # 지름 입력
        diameter_input = input('돔의 지름을 입력하세요 (m): ').strip()
        if not diameter_input:
            raise ValueError('지름을 입력해주세요.')
        
        diameter = float(diameter_input)
        if diameter <= 0:
            raise ValueError('지름은 0보다 큰 값이어야 합니다.')
        
        # 재질 입력
        print('재질을 선택하세요:')
        print('1. glass (유리)')
        print('2. aluminum (알루미늄)')
        print('3. carbon_steel (탄소강)')
        
        material_input = input('재질을 입력하세요: ').strip().lower()
        
        # 재질 매핑
        material_map = {
            '1': 'glass',
            'glass': 'glass',
            '유리': 'glass',
            '2': 'aluminum',
            'aluminum': 'aluminum',
            '알루미늄': 'aluminum',
            '3': 'carbon_steel',
            'carbon_steel': 'carbon_steel',
            '탄소강': 'carbon_steel'
        }
        
        if material_input not in material_map:
            raise ValueError('유효하지 않은 재질입니다.')
        
        material = material_map[material_input]
        
        # 두께 입력 (선택사항)
        thickness_input = input('돔의 두께를 입력하세요 (cm, 기본값 1): ').strip()
        if not thickness_input:
            thickness = 1.0
        else:
            thickness = float(thickness_input)
            if thickness <= 0:
                raise ValueError('두께는 0보다 큰 값이어야 합니다.')
        
        return diameter, material, thickness
        
    except ValueError as e:
        raise ValueError(f'입력 오류: {e}')
    except Exception as e:
        raise ValueError(f'입력 처리 중 오류가 발생했습니다: {e}')


def print_results():
    """결과를 지정된 형식으로 출력"""
    # 재질 한글 변환
    material_korean = {
        'glass': '유리',
        'aluminum': '알루미늄',
        'carbon_steel': '탄소강'
    }
    
    korean_material = material_korean.get(dome_material, dome_material)
    
    print(f'\n=== 계산 결과 ===')
    print(f'재질 ⇒ {korean_material}, 지름 ⇒ {dome_diameter} m, 두께 ⇒ {dome_thickness} g/cm³, '
          f'면적 ⇒ {dome_area:.3f} m², 무게 ⇒ {dome_weight:.3f} kg')
    print(f'화성 중력을 적용한 무게입니다. (지구 중력의 {MARS_GRAVITY}배)')


def main():
    """메인 실행 함수"""
    print('=== Mars 반구체 돔 계산 프로그램 ===')
    print('화성 기지용 반구체 돔의 표면적과 무게를 계산합니다.')
    
    while True:
        try:
            print('\n' + '='*50)
            print('1. 돔 계산하기')
            print('2. 프로그램 종료')
            
            choice = input('\n선택하세요 (1-2): ').strip()
            
            if choice == '1':
                try:
                    # 사용자 입력 받기
                    diameter, material, thickness = get_user_input()
                    
                    # 계산 수행
                    print('\n계산 중...')
                    area, weight = sphere_area(diameter, material, thickness)
                    
                    # 결과 출력
                    print_results()
                    
                    # # 추가 정보 출력
                    # print(f'\n상세 정보:')
                    # print(f'- 반구 곡면적: {area:.3f} m²')
                    # print(f'- 사용된 재질 밀도: {MATERIAL_DENSITIES[material]:.1f} g/cm³')
                    # print(f'- 화성 중력 계수: {MARS_GRAVITY}')
                    
                except (ValueError, TypeError) as e:
                    print(f'오류: {e}')
                    print('다시 시도해주세요.')
                except Exception as e:
                    print(f'예상치 못한 오류가 발생했습니다: {e}')
                    
            elif choice == '2':
                print('프로그램을 종료합니다.')
                break
                
            else:
                print('잘못된 선택입니다. 1 또는 2를 입력해주세요.')
                
        except KeyboardInterrupt:
            print('\n\n프로그램이 중단되었습니다.')
            break
        except Exception as e:
            print(f'프로그램 실행 중 오류가 발생했습니다: {e}')


if __name__ == '__main__':
    main()