import os
import glob
import requests
import json

gannoy_host = 'http://172.18.0.1:1323/'

if __name__ == '__main__':
    for path in glob.glob('images/*.jpg'):
        filename = os.path.basename(path).split('.')[0]
        file_id = int(filename.split('_')[0])

        deleting_url = '{}databases/table/features/{}'.format(gannoy_host, file_id)
        requests.delete(deleting_url)
