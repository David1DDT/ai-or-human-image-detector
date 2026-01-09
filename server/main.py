from flask import Flask, request
from predict import predict_image
import io
from PIL import Image
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api/predict", methods=["POST"])
def api_predict():
    if "image" not in request.files:
        return {"error": "No image provided"}, 400
    file = request.files["image"]

    try:
        image = Image.open(io.BytesIO(file.read()))
    except Exception as e:
        return {"error": "Invalid image file"}, 400

    label, confidence = predict_image(image)
    print(f"Predicted: {label} ({confidence:.4f})")
    return {"prediction": label, "confidence": round(confidence, 4)}


if __name__ == "__main__":
    app.run(debug=True)
