from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np
from model import model
from flask import Flask, request, jsonify
import io
from PIL import Image
import glob
import base64
import requests
import json
import os

app = Flask(__name__)
gannoy_host = 'http://gannoy:1323'

def get_feature(f):
    img = image.load_img(f, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return model.predict(x)


@app.route("/", methods=['GET', 'POST'])
def extract():
    if request.method == 'GET':
        return """
<html>
<body>
<h1>DeepFeature Extracter</h1>
<form method="POST" enctype="multipart/form-data">
<input type="file" name="image">
<button type="submit">extract feature</button>
</form>
<h1>Setup To Search Similar Image</h1>
<form method="POST" action="/setup">
<button type="submit">setup</button>
</form>
<h1>Search Similar Images Using Gannoy</h1>
<form method="POST" enctype="multipart/form-data" action="/search">
<input type="file" name="image">
<button type="submit">search</button>
<p>NOTE: Use it after setup.</p>
</form>
</body>
</html>
"""
    elif request.method == 'POST':
        r = request.files['image']
        features = get_feature(r)
        return jsonify({'features': features.tolist()[0]})

@app.route("/search", methods=['POST'])
def search():
    r = request.files['image']
    query = base64.b64encode(r.read()).decode('utf-8')

    searching_url = '{}/search?database=table&key={}'.format(gannoy_host, int(r.filename.split('_')[0]))
    res = requests.get(searching_url)
    first_path = resolve(json.loads(res.content)[0])
    second_path = resolve(json.loads(res.content)[1])
    third_path = resolve(json.loads(res.content)[2])
    fourth_path = resolve(json.loads(res.content)[3])
    first = base64.b64encode(open(first_path, 'rb').read()).decode('utf-8')
    second = base64.b64encode(open(second_path, 'rb').read()).decode('utf-8')

    third = base64.b64encode(open(third_path, 'rb').read()).decode('utf-8')
    fourth = base64.b64encode(open(fourth_path, 'rb').read()).decode('utf-8')

    s =  """
<html>
<body>
<h1>query</h1>
<img src="data:image/jpeg;base64,{}" width=200>
<h1>first</h1>
<img src="data:image/jpeg;base64,{}" width=200>
<h1>second</h1>
<img src="data:image/jpeg;base64,{}" width=200>
<h1>third</h1>
<img src="data:image/jpeg;base64,{}" width=200>
</body>
</html>
"""
    return s.format(query, first, second, third)

@app.route("/setup", methods=['POST'])
def setup():
    for path in glob.glob('images/*.jpg'):
        features = get_feature(open(path, 'rb'))
        js = {'features': features.tolist()[0]}

        filename = os.path.basename(path).split('.')[0]
        file_id = int(filename.split('_')[0])

        registering_url = '{}/databases/table/features/{}'.format(gannoy_host, file_id)
        requests.put(registering_url,
                data=json.dumps(js),
                headers={'content-type': 'application/json'})
    return 'setup done';



def resolve(id):
    for l in glob.glob('images/*.jpg'):
        prefix = '{}_'.format(id)
        if os.path.basename(l).startswith(prefix):
            return l

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
