# 🧠 Image Colorization and Upscaling Project
This project is a web application that utilizes pre-trained models to colorize and upscale images. The application is built using Flask, a micro web framework, and utilizes OpenCV for image processing. The project's core functionality is to take an input image, apply colorization and upscaling using the downloaded models, and return the result. The application provides a user-friendly interface for uploading images, viewing results, and interacting with the application.

## 🚀 Features
- **Image Colorization**: The application can colorize black and white images using pre-trained models.
- **Image Upscaling**: The application can upscale images to higher resolutions using pre-trained models.
- **User-Friendly Interface**: The application provides a simple and intuitive interface for uploading images, viewing results, and interacting with the application.
- **Model Downloading**: The application downloads pre-trained models automatically if they are not already present locally.

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **Image Processing**: OpenCV
- **Model Downloading**: Requests
- **Dependencies**: numpy, opencv-contrib-python-headless, requests, gunicorn, werkzeug
- **Database**: None

## 📦 Installation
To install the project, follow these steps:
1. Clone the repository using `git clone`.
2. Install the dependencies using `pip install -r requirements.txt`.
3. Run the application using `python app.py`.

## 💻 Usage
To use the application, follow these steps:
1. Open a web browser and navigate to `http://localhost:5000`.
2. Upload an image using the file input or drop zone.
3. Click the convert button to apply colorization and upscaling to the image.
4. View the result and download the converted image.

## 📂 Project Structure
```markdown
.
├── app.py
├── download_models.py
├── static
│   ├── js
│   │   └── script.js
│   └── ...
├── templates
│   └── index.html
├── requirements.txt
└── ...
```



## 💖 Thanks Message
We would like to thank all the contributors and users of the project for their support and feedback. This project is made possible by the open-source community and the pre-trained models used in the application.
