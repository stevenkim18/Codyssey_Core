import random
import json
import time
import platform
import psutil
import threading
import multiprocessing

#1-1
class DummySensor:
    
    #1-2
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        
    #1-3, 1-4
    def set_env(self):
        try:
            self.env_values['mars_base_internal_temperature'] = round(
                random.uniform(18.0, 30.0), 1
            )
            self.env_values['mars_base_external_temperature'] = round(
                random.uniform(0.0, 21.0), 1
            )
            self.env_values['mars_base_internal_humidity'] = round(
                random.uniform(50.0, 60.0), 1
            )
            self.env_values['mars_base_external_illuminance'] = round(
                random.uniform(500.0, 715.0), 0
            )
            self.env_values['mars_base_internal_co2'] = round(
                random.uniform(0.02, 0.1), 3
            )
            self.env_values['mars_base_internal_oxygen'] = round(
                random.uniform(4.0, 7.0), 1
            )
            
        except Exception as e:
            print(f"환경 데이터 설정 중 오류 발생: {e}")
    #1-5
    def get_env(self):
        return self.env_values

# 2-1
class MissionComputer:
    
    #2-2
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        
        #2-3
        self.ds = DummySensor()
    
    #2-4
    def get_sensor_data(self):
        try:
            while True:
                #2-5-1
                self.ds.set_env()  
                sensor_data = self.ds.get_env()
                self.env_values.update(sensor_data)
                
                #2-5-2
                print("=== 화성 기지 정보 ===")
                print(json.dumps(self.env_values, indent=2, ensure_ascii=False))
                print("-" * 50)  # 구분선 추가
                
                #2-5-3
                time.sleep(5)
                
        except Exception as e:
            print(f"센서 데이터 처리 중 오류 발생: {e}")
    
    # 3-1, 3-2, 3-3
    def get_mission_computer_info(self):
        try:
            while True:
                system_info = {
                    'operating_system': platform.system(),
                    'os_version': platform.version(),
                    'cpu_type': platform.processor(),
                    'cpu_cores': psutil.cpu_count(logical=False),  # 물리적 코어 수
                    'cpu_logical_cores': psutil.cpu_count(logical=True),  # 논리적 코어 수
                    'memory_size_gb': round(psutil.virtual_memory().total / (1024**3), 2)  # GB 단위
                }

                # JSON 형식으로 출력
                print("=== 미션 컴퓨터 시스템 정보 ===")
                print(json.dumps(system_info, indent=2, ensure_ascii=False))
                print("-" * 50)
                
                time.sleep(20)

            
        except Exception as e:
            print(f"시스템 정보 수집 중 오류 발생: {e}")
            return None
    # 3-4, 3-5, 3-6
    def get_mission_computer_load(self):
        try:
            
            while True:
                memory = psutil.virtual_memory()
                load_info = {
                    'cpu_usage_percent': psutil.cpu_percent(interval=1),  # 1초 간격으로 CPU 사용량 측정
                    'memory_usage_percent': memory.percent,
                    'memory_used_gb': round(memory.used / (1024**3), 2),
                    'memory_available_gb': round(memory.available / (1024**3), 2)
                }

                # JSON 형식으로 출력
                print("=== 미션 컴퓨터 실시간 부하 정보 ===")
                print(json.dumps(load_info, indent=2, ensure_ascii=False))
                print("-" * 50)

                time.sleep(20)
            
        except Exception as e:
            print(f"부하 정보 수집 중 오류 발생: {e}")
            return None

def run_system_info():
    print(f"[{multiprocessing.current_process().name}] 시스템 정보 모니터링 시작...")
    runComputer1 = MissionComputer()
    runComputer1.get_mission_computer_info()

def run_load_info():
    print(f"[{multiprocessing.current_process().name}] 부하 정보 모니터링 시작...")
    runComputer2 = MissionComputer()
    runComputer2.get_mission_computer_load()

def run_sensor_data():
    print(f"[{multiprocessing.current_process().name}] 센서 데이터 모니터링 시작...")
    runComputer3 = MissionComputer()
    runComputer3.get_sensor_data()
            
def main():
    #1-6
    # ds = DummySensor()
   
    #1-7
    # ds.set_env()
   
    # print(ds.get_env())
   
    #2-6
    runComputer = MissionComputer()
   
     #2-7
#    runComputer.get_sensor_data()
   
    #3-7
    # runComputer.get_mission_computer_info()
    # runComputer.get_mission_computer_load()
   
    try:
        # # 4-1, 4-2, 4-3
        # info_thread = threading.Thread(
        #     target=runComputer.get_mission_computer_info,
        #     name="SystemInfoThread",
        #     daemon=True
        # )

        # load_thread = threading.Thread(
        #     target=runComputer.get_mission_computer_load,
        #     name="LoadInfoThread",
        #     daemon=True
        # )

        # sensor_thread = threading.Thread(
        #     target=runComputer.get_sensor_data,
        #     name="SensorDataThread",
        #     daemon=True
        # )

        # print("🔄 시스템 정보 모니터링 스레드 시작...")
        # info_thread.start()

        # print("🔄 부하 정보 모니터링 스레드 시작...")
        # load_thread.start()

        # print("🔄 센서 데이터 모니터링 스레드 시작...")
        # sensor_thread.start()

        # # 메인 쓰레드가 살려두기 위함.
        # while True:
        #     time.sleep(1)
            
            
        # 4-4, 4-5, 4-6
        process1 = multiprocessing.Process(
            target=run_system_info,
            name="SystemInfoProcess"
        )
        
        # 2. 부하 정보 모니터링 프로세스 (20초마다)
        process2 = multiprocessing.Process(
            target=run_load_info,
            name="LoadInfoProcess"
        )
        
        # 3. 센서 데이터 모니터링 프로세스 (5초마다)
        process3 = multiprocessing.Process(
            target=run_sensor_data,
            name="SensorDataProcess"
        )
        
        print("🚀 시스템 정보 모니터링 프로세스 시작...")
        process1.start()
        
        print("🚀 부하 정보 모니터링 프로세스 시작...")
        process2.start()
        
        print("🚀 센서 데이터 모니터링 프로세스 시작...")
        process3.start()
        
        # 모든 프로세스가 종료될 때까지 대기    
        process1.join()
        process2.join()
        process3.join()
            
    except KeyboardInterrupt:
        print("\n\n🛑 모든 모니터링 시스템이 종료되었습니다.")
        
        # 모든 프로세스 종료
        if process1.is_alive():
            process1.terminate()
            process1.join()
            print("✅ SystemInfoProcess 종료됨")
            
        if process2.is_alive():
            process2.terminate()
            process2.join()
            print("✅ LoadInfoProcess 종료됨")
            
        if process3.is_alive():
            process3.terminate()
            process3.join()
            print("✅ SensorDataProcess 종료됨")
        
        print("프로그램을 종료합니다.")
    except Exception as e:
        print(f"\n❌ 멀티스레드/프로세스 실행 중 오류 발생: {e}")
   
if __name__ == "__main__":
    main() 
    