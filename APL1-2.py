# DYKBPupVuJtZ1hxrMq79cGfTByIO7Db2NQmQmbDU
# https://api.nasa.gov/planetary/apod? api_key = DYKBPupVuJtZ1hxrMq79cGfTByIO7Db2NQmQmbDU
import urllib.request
import json
import requests
from pprint import pprint

ml = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&page=2&api_key=DYKBPupVuJtZ1hxrMq79cGfTByIO7Db2NQmQmbDU'


f = requests.get(ml).json()
pprint(f)
for i in f['photos']: print('id', i['id'])
param_id = int(input('id = '))
for o in f['photos']:
    if o['id'] == param_id:
        print(o['img_src'])
        foto = o['img_src']
        img = urllib.request.urlopen(foto).read()
        name = f'{param_id}_foto.jpg'
        with open(name, 'wb') as a:
            a.write(img)
            a.close
