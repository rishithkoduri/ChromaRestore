import os
import numpy as np
import cv2
from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
MODEL_FOLDER = 'static/models'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

net = None
pts = None

def load_models():
    global net, pts
    if net is None:
        protoPath = os.path.join(MODEL_FOLDER, 'colorization_deploy_v2.prototxt')
        weightsPath = os.path.join(MODEL_FOLDER, 'colorization_release_v2.caffemodel')
        ptsPath = os.path.join(MODEL_FOLDER, 'pts_in_hull.npy')
        
        net = cv2.dnn.readNetFromCaffe(protoPath, weightsPath)
        pts = np.load(ptsPath)
        class8 = net.getLayerId("class8_ab")
        conv8 = net.getLayerId("conv8_313_rh")
        pts = pts.transpose().reshape(2, 313, 1, 1)
        net.getLayer(class8).blobs = [pts.astype("float32")]
        net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

def process_image(image_path, save_path):
    load_models()
    
    frame = cv2.imread(image_path)
    
    height, width = frame.shape[:2]
    max_dim = 500
    if max(height, width) > max_dim:
        scale = max_dim / max(height, width)
        frame = cv2.resize(frame, None, fx=scale, fy=scale)
    
    scaled = frame.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (frame.shape[1], frame.shape[0]))
    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")

    upscale_factor = 4
    new_width = frame.shape[1] * upscale_factor
    new_height = frame.shape[0] * upscale_factor
    
    final_output = cv2.resize(colorized, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

    cv2.imwrite(save_path, final_output)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = "input_" + file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    output_filename = "restored_" + file.filename
    output_path = os.path.join(RESULT_FOLDER, output_filename)

    try:
        process_image(filepath, output_path)
        return jsonify({
            'result': '/' + output_path, 
            'filename': output_filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(RESULT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)