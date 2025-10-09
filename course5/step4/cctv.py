from pathlib import Path
import zipfile
import sys
import cv2

def extract_cctv_zip_if_exists(base_dir: Path) -> Path:
    zip_path = base_dir / "cctv.zip"
    target_dir = base_dir / "CCTV"
    target_dir.mkdir(exist_ok=True)

    if not zip_path.exists():
        # ZIP이 없어도 뷰어는 동작하도록 조용히 통과
        return target_dir

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(target_dir)
        print(f"[완료] '{zip_path.name}' 을(를) '{target_dir}' 에 압축 해제했습니다.")
    except zipfile.BadZipFile:
        print(f"[오류] 올바른 ZIP 파일이 아닙니다: {zip_path}")
        sys.exit(2)

    return target_dir

def list_images_in(dir_path: Path) -> list[Path]:
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tif", ".tiff"}
    return sorted([p for p in dir_path.iterdir() if p.suffix.lower() in exts])

def detect_person_in_image(image_path: Path) -> tuple[bool, any]:
    # 이미지 읽기
    img = cv2.imread(str(image_path))
    if img is None:
        return False, None

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    h, w = img.shape[:2]

    # 여러 스케일로 검사
    found = False
    for scale_factor in [1.0, 1.5, 2.0, 0.7, 0.5]:
        scaled_img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor)

        # 사람 감지 - 매우 완화된 파라미터
        boxes, weights = hog.detectMultiScale(
            scaled_img,
            winStride=(2, 2),      # 매우 촘촘하게 검색
            padding=(16, 16),      # 패딩 증가
            scale=1.02,            # 매우 세밀한 스케일
            hitThreshold=-1.0      # 임계값을 음수로 설정하여 최대 민감도
        )

        if len(boxes) > 0:
            found = True
            break

    return found, img

def viewer_mode(images: list[Path]):
    """이미지 뷰어 모드: 방향키로 이미지 탐색"""
    if not images:
        print("[안내] CCTV 폴더에 이미지가 없습니다.")
        return

    print(f"\n=== 이미지 뷰어 모드 ===")
    print(f"총 {len(images)}장의 이미지")
    print("← 또는 A: 이전 이미지")
    print("→ 또는 D: 다음 이미지")
    print("ESC 또는 Q: 종료\n")

    idx = 0
    while True:
        image_path = images[idx]
        img = cv2.imread(str(image_path))

        if img is not None:
            # 창 제목에 현재 이미지 정보 표시
            window_title = f"CCTV Viewer - {image_path.name} ({idx + 1}/{len(images)})"
            cv2.imshow(window_title, img)
            print(f"[{idx + 1}/{len(images)}] {image_path.name}")

        key = cv2.waitKey(0) & 0xFF

        # 오른쪽 방향키 또는 D (키코드: 3, 83, 또는 'd')
        if key == ord('d') or key == ord('D') or key == 3 or key == 83:
            idx = (idx + 1) % len(images)
        # 왼쪽 방향키 또는 A (키코드: 2, 82, 또는 'a')
        elif key == ord('a') or key == ord('A') or key == 2 or key == 82:
            idx = (idx - 1) % len(images)
        # ESC 또는 Q
        elif key == 27 or key == ord('q') or key == ord('Q'):
            break

        cv2.destroyAllWindows()

    cv2.destroyAllWindows()
    print("\n[종료] 뷰어 모드를 종료합니다.")

def person_detection_mode(images: list[Path]):
    """사람 감지 모드: 사람이 있는 이미지만 표시"""
    if not images:
        print("[안내] CCTV 폴더에 이미지가 없습니다.")
        return

    print(f"\n=== 사람 감지 모드 ===")
    print(f"총 {len(images)}장의 이미지를 검색합니다...")
    print("엔터키: 다음 검색 진행\n")

    idx = 0
    while idx < len(images):
        image_path = images[idx]
        print(f"[{idx + 1}/{len(images)}] {image_path.name} 검색 중...")

        found, img = detect_person_in_image(image_path)
        if found:
            print(f"✓ 사람을 발견했습니다! {image_path.name}")

            # 이미지를 화면에 표시
            if img is not None:
                cv2.imshow('CCTV - 사람 감지', img)
                print("엔터키를 눌러 다음 검색을 진행하세요...\n")

                # 엔터키 입력 대기
                while True:
                    key = cv2.waitKey(0)
                    if key == 13 or key == ord('\n') or key == ord('\r'):  # 엔터키
                        cv2.destroyAllWindows()
                        break

        idx += 1

    print("\n[완료] 모든 이미지 검색이 완료되었습니다.")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    target = extract_cctv_zip_if_exists(base)
    images = list_images_in(target)

    if not images:
        print(f"[안내] '{target}' 폴더에 표시할 이미지가 없습니다. (지원 확장자: jpg, jpeg, png, bmp, gif, webp, tif, tiff)")
        sys.exit(0)

    # 모드 선택
    print("\n" + "="*50)
    print("CCTV 이미지 분석 프로그램")
    print("="*50)
    print("\n모드를 선택하세요:")
    print("1. 이미지 뷰어 모드 (방향키로 이미지 탐색)")
    print("2. 사람 감지 모드 (사람이 있는 이미지만 표시)")
    print("="*50)

    try:
        choice = input("\n선택 (1 또는 2): ").strip()

        if choice == "1":
            viewer_mode(images)
        elif choice == "2":
            person_detection_mode(images)
        else:
            print("[오류] 1 또는 2를 입력해주세요.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n[종료] 프로그램을 종료합니다.")
        sys.exit(0)
