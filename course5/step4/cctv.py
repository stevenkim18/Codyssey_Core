from pathlib import Path
import zipfile
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

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

def run_viewer(images: list[Path]) -> int:

    class ImageViewer(QWidget):
        def __init__(self, imgs: list[Path]):
            super().__init__()
            self.imgs = imgs
            self.idx = 0

            self.label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.label)

            self.setWindowTitle("CCTV Viewer")
            self.resize(1000, 700)
            self._orig_pixmap = None
            self.load_current()

        def load_current(self):
            if not self.imgs:
                self.label.setText("CCTV 폴더에 표시할 이미지가 없습니다.")
                return
            path = self.imgs[self.idx]
            pix = QPixmap(str(path))
            if pix.isNull():
                self.label.setText(f"이미지를 불러올 수 없습니다:\n{path.name}")
                self._orig_pixmap = None
            else:
                self._orig_pixmap = pix
                self.update_scaled_pixmap()
            self.setWindowTitle(f"CCTV Viewer — {path.name} ({self.idx+1}/{len(self.imgs)})")

        def update_scaled_pixmap(self):
            if self._orig_pixmap is None:
                return
            avail = self.label.size()
            if avail.width() > 0 and avail.height() > 0:
                scaled = self._orig_pixmap.scaled(
                    avail,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self.label.setPixmap(scaled)

        def keyPressEvent(self, e):
            if not self.imgs:
                return super().keyPressEvent(e)
            key = e.key()
            # -> D 키
            if key in (Qt.Key.Key_Right, Qt.Key.Key_D):
                self.idx = (self.idx + 1) % len(self.imgs)
                self.load_current()
            # <- A 키
            elif key in (Qt.Key.Key_Left, Qt.Key.Key_A):
                self.idx = (self.idx - 1) % len(self.imgs)
                self.load_current()
            else:
                super().keyPressEvent(e)

            # 로딩 뒤 즉시 스케일 갱신 (윈도 크기 변경 없이도 선명도 유지)
            self.update_scaled_pixmap()

        def resizeEvent(self, e):
            super().resizeEvent(e)
            self.update_scaled_pixmap()

    app = QApplication(sys.argv)
    w = ImageViewer(images)
    w.show()
    return app.exec()


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    target = extract_cctv_zip_if_exists(base)
    images = list_images_in(target)

    if not images:
        print(f"[안내] '{target}' 폴더에 표시할 이미지가 없습니다. (지원 확장자: jpg, jpeg, png, bmp, gif, webp, tif, tiff)")
    sys.exit(run_viewer(images))