import sys
import os
import queue
import time as time_module
import sounddevice as sd
import soundfile as sf
from datetime import datetime

SAMPLE_RATE = 44100
CHANNELS = 1

# "records" 폴더 없으면 생성
os.makedirs("records", exist_ok=True)

# 파일명: "년월일-시간분초".wav  예) 20250828-164512.wav
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
OUT_PATH = os.path.join("records", f"{timestamp}.wav")

q = queue.Queue()

def callback(indata, frames, callback_time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

print("녹음 시작! 중지하려면 Ctrl+C")

start_time = time_module.time()

with sf.SoundFile(OUT_PATH, mode='w', samplerate=SAMPLE_RATE, channels=CHANNELS) as file:
    # 스트림을 변수에 바인딩해서 실제 사용 장치 정보를 확인
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback) as stream:
        # 실제로 사용 중인 입력 장치 인덱스/이름 조회
        in_dev = stream.device
        if isinstance(in_dev, (list, tuple)):
            in_dev = in_dev[0]  # 입력 장치 인덱스만 추출
        dev_info = sd.query_devices(in_dev)
        mic_name = dev_info["name"]
        print(f"인식된 마이크: {mic_name}")

        try:
            while True:
                file.write(q.get())
        except KeyboardInterrupt:
            pass

elapsed = int(time_module.time() - start_time)
mins, secs = divmod(elapsed, 60)
print(f"\n저장 완료: {OUT_PATH}")
print(f"총 녹음 시간: {mins}분 {secs}초")