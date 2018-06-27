import os
import glob
import requests
import json
from gannoy import gannoy_host

extractor_host = 'http://127.0.0.1:8080/'

if __name__ == '__main__':
    for path in glob.glob('images/*.jpg'):
        files = {'image': open(path, 'rb')}
        res = requests.post(extractor_host, files=files)
        js = json.loads(res.content)

        filename = os.path.basename(path).split('.')[0]
        file_id = int(filename.split('_')[0])

        registering_url = '{}/databases/table/features/{}'.format(gannoy_host, file_id)
        requests.put(registering_url,
                data=json.dumps(js),
                headers={'content-type': 'application/json'})
