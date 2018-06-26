from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np
from model import model
from flask import Flask, request, jsonify
import io
from PIL import Image

app = Flask(__name__)

@app.route("/", methods=['POST'])
def extract():
    r = request.get_data()
    img = image.load_img(io.BytesIO(r), target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    return jsonify({'feature': features.tolist()[0]})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
