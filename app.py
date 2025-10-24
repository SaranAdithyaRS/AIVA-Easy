from flask import Flask, request, jsonify
import base64
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# OCR.space config
OCR_API_KEY = os.getenv("OCR_SPACE_API_KEY", "K89861181488957")
OCR_URL = "https://api.ocr.space/parse/image"

@app.route("/ocr", methods=["POST"])
def ocr_process():
    data = request.json
    image_b64 = data.get("frame", "")

    if not image_b64:
        return jsonify({"response": "No image provided"}), 400

    # Remove possible data URI header
    if "," in image_b64:
        image_b64 = image_b64.split(",")[1]

    try:
        payload = {
            "apikey": OCR_API_KEY,
            "language": "eng",
            "base64Image": f"data:image/jpeg;base64,{image_b64}"
        }

        response = requests.post(OCR_URL, data=payload)
        result = response.json()

        parsed_text = ""
        if "ParsedResults" in result:
            parsed_text = "\n".join(
                [res.get("ParsedText", "") for res in result["ParsedResults"]]
            )

        return jsonify({
            "success": True,
            "text": parsed_text.strip(),
            "raw": result
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/health")
def health():
    return jsonify({"status": "OCR.space server running"})

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 OCR Server (OCR.space) Running on Port 6000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=6000)
