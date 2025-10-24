from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from flask_cors import CORS
from paddleocr import PaddleOCR

app = Flask(__name__)
CORS(app)

# Initialize PaddleOCR once
ocr = PaddleOCR(use_angle_cls=True, lang='en')

@app.route('/ocr', methods=['POST'])
def ocr_process():
    data = request.json
    image_b64 = data.get('frame', '')

    if ',' in image_b64:
        image_b64 = image_b64.split(',')[1]

    img_bytes = base64.b64decode(image_b64)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"response": "Invalid image"})

    result = ocr.ocr(frame)
    text = " ".join([line[1][0] for line in result[0]]) if result and result[0] else "No text detected"
    return jsonify({"response": text})

@app.route('/health')
def health():
    return jsonify({"status": "OCR server running"})

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 OCR Server (PaddleOCR) Running on Port 6000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=6000)
