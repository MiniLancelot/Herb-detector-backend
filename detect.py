import pathlib
import cv2
from PIL import Image
import torch
import base64
import numpy as np
from io import BytesIO

class Detect:
    def __init__(self):
        temp = pathlib.PosixPath
        pathlib.PosixPath = pathlib.WindowsPath
        torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
        pathlib.PosixPath = temp

    def detect(self, image):
        # Read image
        image = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
        converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        converted = Image.fromarray(converted)

        results = self.model(converted, size=640)
        labels = results.names
        plant_labels_detected = {"plants": {}}

        for *box, conf, cls in results.xyxy[0]:
            label = f"{labels[int(cls)]}: {conf:.2f}"

            cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 0, 0), 2)
            width = box[2] - box[0]
            font_scale = get_optimal_font_scale(label, width)
            # changing scale
            # cv2.putText(image, label, (int(box[0]), int(box[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
            cv2.putText(image, label, (int(box[0]), int(box[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                        (0, 0, 255), 2)
            # Count the number of fruit detected
            plant_labels_detected["plants"][labels[int(cls)]] = plant_labels_detected["plants"].get(labels[int(cls)],
                                                                                                    0) + 1

        # pic = cv2.imwrite(f'img/{image_path}_detected.jpg', image)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(image)
        byte_arr = BytesIO()
        pil_img.save(byte_arr, format='JPEG')
        encoded_image = base64.b64encode(byte_arr.getvalue()).decode('utf-8')

        plant_labels_detected["image"] = encoded_image
        # return image
        return plant_labels_detected

def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 60, 1)):
        textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale/10, thickness=1)
        new_width = textSize[0][0]
        if (new_width <= width):
            return scale/10
    return 0.1





