import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image


# ======================
# CONFIG
# ======================
MODEL_PATH = "ai_vs_real.pth"
IMG_SIZE = 224

if torch.backends.mps.is_available():
    DEVICE = "mps"
elif torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"

CLASSES = ["fake", "real"]

# ======================
# TRANSFORM (must match training!)
# ======================
transform = transforms.Compose(
    [
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
    ]
)

# ======================
# LOAD MODEL
# ======================
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 2)

state = torch.load(MODEL_PATH, map_location=DEVICE)
model.load_state_dict(state)

model.to(DEVICE)
model.eval()

print("✅ Model loaded on", DEVICE)


# ======================
# PREDICT FUNCTION
# ======================
def predict_image(image: Image.Image):
    image = image.convert("RGB")
    image = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        output = model(image)
        probs = torch.softmax(output, dim=1)

    idx = probs.argmax(dim=1).item()
    confidence = probs[0, idx].item()

    return CLASSES[idx], confidence
