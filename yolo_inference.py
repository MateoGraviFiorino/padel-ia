from ultralytics import YOLO

# Load model
model = YOLO('models/yolo8_best.pt')

result = model.predict('input_files/sinner1.mp4', conf=0.2, save=True)
#print(result)
#print("boxes: ")
#for boxes in result[0].boxes:
#    print(boxes)