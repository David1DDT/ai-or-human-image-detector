from flask import Flask, request
from predict import predict_image
import io

app = Flask(__name__)


@app.route("/api/predict", methods=["POST"])
def api_predict():
    if "image" not in request.files:
        return {"error": "No image provided"}, 400
    return "This endpoint will handle image predictions."
    file = request.files["image"]

    try:
        image = Image.open(io.BytesIO(file.read()))
    except Exception as e:
        return {"error": "Invalid image file"}, 400

    label, confidence = predict_image(image)

    return {"prediction": label, "confidence": round(confidence, 4)}


if __name__ == "__main__":
    app.run(debug=True)
