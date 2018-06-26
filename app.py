from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np
from model import model
from flask import Flask

app = Flask(__name__)
model = VGG16(weights='imagenet', include_top=False, pooling='avg')

@app.route("/", methods=['POST'])
def extract():
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    return str(feature.shape)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
