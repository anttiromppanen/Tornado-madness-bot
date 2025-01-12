from ultralytics import YOLO

model = YOLO("./data/model/best.pt")

result = model(["./data/img/test-img-continue.png"], conf=0.5, save=True)

boxes = result[0].boxes.xyxy.tolist()
classes = result[0].boxes.cls.tolist()
names = result[0].names
confidences = result[0].boxes.conf.tolist()

print(boxes)
print(classes)
print(names)
print(confidences)
