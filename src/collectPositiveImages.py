from io import BytesIO
from itertools import count
from time import sleep
import requests
from PIL import Image

URL_IMG_GEN = 'https://dog.ceo/api/breed/boxer/images/random'
NUM_IMAGES = 400

count = 0 

while count < NUM_IMAGES:
    urlToConsume = URL_IMG_GEN
    try :
        response = requests.get(urlToConsume)

        if response.ok:
            imgUrl = response.json()['message']
            response = requests.get(imgUrl)

            if response.ok:
                name = imgUrl.split('/')[-1]

                img = Image.open(BytesIO(response.content))        
                img.save("/data/train/boxer" + name, "JPEG")

                print(f'IMAGEM SALVA: {name}\nNUMERO DA IMAGEM SALVA: {count+1}')
                count += 1
                sleep(1)
    
    except:
        sleep(5)