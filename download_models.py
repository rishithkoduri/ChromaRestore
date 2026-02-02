import os
import requests

MODEL_FOLDER = 'static/models'
os.makedirs(MODEL_FOLDER, exist_ok=True)

models = {
    "colorization_deploy_v2.prototxt": "https://raw.githubusercontent.com/AbhilipsaJena/Image_colorization-OpenCV/main/colorization_deploy_v2.prototxt",
    "pts_in_hull.npy": "https://raw.githubusercontent.com/AbhilipsaJena/Image_colorization-OpenCV/main/pts_in_hull.npy",
    "colorization_release_v2.caffemodel": "https://www.dropbox.com/s/dx0qvhhp5hbcx7z/colorization_release_v2.caffemodel?dl=1",
    "EDSR_x4.pb": "https://github.com/Saafke/EDSR_Tensorflow/raw/master/models/EDSR_x4.pb"
}

for filename, url in models.items():
    path = os.path.join(MODEL_FOLDER, filename)
    if not os.path.exists(path):
        print(f"Downloading {filename}...")
        response = requests.get(url, stream=True)
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)