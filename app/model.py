import torch
from torchvision import models, transforms
from PIL import Image
import requests
from io import BytesIO

# Load of the pre-trained model
model = models.resnet50(pretrained=True)
model.eval()

# Preprocessing of the image:
# Resize the image to slightly larger number image
# Center-crop to ensure that the resized doesn't distort the image and we allow it to be the fixed size (224, 224) which is the dimension configuration
# for the image datasets of resnet
# Transform it to a tensor (because of pytorch transforms)
# and then standardize to match the mean and the standard deviation normalization

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Function to load image from a URL or path
def load_image(image_source:str) -> Image:
    if image_source.startswith("http://") or image_source.startswith("https://"):
        response = requests.get(image_source)
        #print(response)
        return Image.open(BytesIO(response.content)).convert("RGB")

    else:
        return Image.open(image_source).convert("RGB")

# Classification function
def classify_images(image_source: str) -> str:
    image = load_image(image_source)
    input_tensor = preprocess(image).unsqueeze(0)

    # perform inference
    with torch.no_grad():
        output = model(input_tensor)

    # predicted class
    _, predicted_idx = output.max(1)
    return predicted_idx.item()