import sys
import os
import queue
import csv
import time as time_module
import sounddevice as sd
import soundfile as sf
from datetime import datetime
from typing import List, Optional
from faster_whisper import WhisperModel

SAMPLE_RATE = 44100
CHANNELS = 1
RECORD_DIR = "records"
os.makedirs(RECORD_DIR, exist_ok=True)

def _fmt(sec: float) -> str:
    s = int(max(0, sec or 0))
    h, r = divmod(s, 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def record_audio() -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = os.path.join(RECORD_DIR, f"{ts}.wav")

    q: "queue.Queue[bytes]" = queue.Queue()

    def cb(indata, frames, t, status):
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    print("녹음 시작! 중지하려면 Ctrl+C")
    start = time_module.time()

    with sf.SoundFile(out_path, mode="w", samplerate=SAMPLE_RATE, channels=CHANNELS) as f:
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=cb) as stream:
            dev = stream.device[0] if isinstance(stream.device, (list, tuple)) else stream.device
            try:
                mic = sd.query_devices(dev).get("name", "Unknown")
            except Exception:
                mic = "Unknown"
            print(f"인식된 마이크: {mic}")
            try:
                while True:
                    f.write(q.get())
            except KeyboardInterrupt:
                print("\n녹음을 중지합니다...")

    mins, secs = divmod(int(time_module.time() - start), 60)
    print(f"\n저장 완료: {out_path}")
    print(f"총 녹음 시간: {mins}분 {secs}초")
    return out_path

def list_recordings() -> List[str]:
    EXTS = (".wav", ".mp3", ".m4a", ".flac", ".ogg", ".webm")
    files = [os.path.join(RECORD_DIR, n) for n in os.listdir(RECORD_DIR) if n.lower().endswith(EXTS)]
    files.sort(key=os.path.getmtime, reverse=True)
    return files


def choose_file(files: List[str]) -> Optional[str]:
    if not files:
        print("녹음된 파일이 없습니다. 먼저 녹음을 해주세요.")
        return None
    print("\n변환할 파일을 선택하세요:")
    for i, p in enumerate(files, 1):
        mtime = datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M")
        size_mb = os.path.getsize(p) / 1_000_000
        print(f"[{i}] {os.path.basename(p)}  ({mtime}, {size_mb:.1f} MB)")
    print("[0] 취소")
    while True:
        s = input("번호 입력: ").strip()
        if s.isdigit():
            n = int(s)
            if n == 0:
                return None
            if 1 <= n <= len(files):
                return files[n - 1]
        print("잘못된 입력입니다. 다시 입력하세요.")

def transcribe_to_csv(audio_path: str, language_hint: Optional[str] = "ko") -> str:
    base, _ = os.path.splitext(audio_path)
    csv_path = base + ".csv"

    print(f"\n음성 인식 시작: {os.path.basename(audio_path)}")
    model = WhisperModel("base", device="auto", compute_type="int8")

    # write as we go (memory-friendly)
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["time", "text"])  # header
        segments, _info = model.transcribe(audio_path, language=language_hint)
        for seg in segments:
            w.writerow([_fmt(seg.start), (seg.text or "").strip()])

    print(f"저장 완료: {csv_path}")
    return csv_path

def main():
    try:
        print("\n무엇을 하시겠어요?")
        print("1) 새로 녹음하기")
        print("2) 녹음된 파일을 텍스트로 변환하기 (SST)")
        print("0) 종료")
        c = input("번호 입력: ").strip()
        if c == "1":
            record_audio()
        elif c == "2":
            files = list_recordings()
            picked = choose_file(files)
            if picked:
                transcribe_to_csv(picked, language_hint="ko")
        else:
            print("종료합니다.")
    except KeyboardInterrupt:
        print("\n사용자 취소(Ctrl+C). 종료합니다.")

if __name__ == "__main__":
    main()