import cv2 as cv
import argparse
from os import path, system


ap = argparse.ArgumentParser()
ap.add_argument("-v" , "--video", required=True, help="Caminho do vídeo a ser analisado.")
ap.add_argument("-q" , "--qtd-max-frames", required=True, help="Quantidade de frames para salvar.")
args = vars(ap.parse_args())

NUM_MAX_FRAMES = int(args["qtd_max_frames"])
    
if args["video"] is not None and not path.exists(args["video"]):
    
    print(f"O vídeo selecionadao não foi encontrado!")

else:
    frameNumber = 1
    
    video = cv.VideoCapture(args["video"])

    while frameNumber <= NUM_MAX_FRAMES:
        ret, frame = video.read()

        if ret:
            fileName = f"data/negative/neg_image_{frameNumber}.jpg"
            cv.imwrite(fileName, frame)

            with open("data/negatives.txt", "a") as f:
                f.write(fileName + "\n")
                print(f"IMAGEM {fileName} SALVA COM SUCESSO!")
                frameNumber += 1
        else:
            system('cls')
            break
        
print("Imagens negativas geradas com sucesso!")
video.release()
cv.destroyAllWindows()
