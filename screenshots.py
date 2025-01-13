import pyautogui

class Screenshots:
    @staticmethod
    def take_and_process_screenshot(model):
        screenshot = pyautogui.screenshot()
        result = model([screenshot], conf=0.5)

        boxes = result[0].boxes.xyxy.tolist()
        classes = result[0].boxes.cls.tolist()
        names = result[0].names

        pixel_color_top_left_corner = screenshot.getpixel((10, 10))

        return boxes, classes, names, pixel_color_top_left_corner
    
    @staticmethod
    def process_screenshot(screenshot, model):
        result = model([screenshot], conf=0.5)

        boxes = result[0].boxes.xyxy.tolist()
        classes = result[0].boxes.cls.tolist()
        names = result[0].names
        confidences = result[0].boxes.conf.tolist()

        return boxes, classes, names, confidences