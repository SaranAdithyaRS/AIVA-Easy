from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from flask_cors import CORS
import easyocr

app = Flask(__name__)
CORS(app)

# Initialize EasyOCR once (English only for lightweight setup)
reader = easyocr.Reader(['en'], gpu=False)

@app.route('/ocr', methods=['POST'])
def ocr_process():
    data = request.json
    image_b64 = data.get('frame', '')

    # Clean Base64 string
    if ',' in image_b64:
        image_b64 = image_b64.split(',')[1]

    # Decode base64 -> OpenCV image
    try:
        img_bytes = base64.b64decode(image_b64)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception:
        return jsonify({"response": "Invalid image encoding"})

    if frame is None:
        return jsonify({"response": "Invalid image"})

    # Run OCR
    try:
        results = reader.readtext(frame)
        text = " ".join([res[1] for res in results]) if results else "No text detected"
    except Exception as e:
        text = f"OCR failed: {str(e)}"

    return jsonify({"response": text})

@app.route('/health')
def health():
    return jsonify({"status": "EasyOCR server running"})

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 OCR Server (EasyOCR) Running on Port 6000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=6000)
