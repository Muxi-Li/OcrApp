from paddleocr import PaddleOCR, draw_ocr
class OcrQt:
    def __init__(self) -> None:
        self.img_path = "D:\\programfiles\\VsProject\\OcrApp\\guiocr\\imgs\\11.jpg"
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    
    def set_task(self,path):
        self.img_path = path

    def start(self):
        self.result = self.ocr.ocr(self.img_path, cls=True)
        # self.show()
    
    def show_result(self):
        result = self.result
        for line in result:
            print(line)