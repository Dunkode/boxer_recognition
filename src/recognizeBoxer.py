import cv2 as cv
import argparse
from os import path

ap = argparse.ArgumentParser()

ap.add_argument("-p", "--predictor-xml", required=True, help="Arquivo que contenha os pesos sinápticos da face de um Boxer.")
ap.add_argument("-i", "--image", help="Caminho do arquivo da imagem a ser analisada.")
ap.add_argument("-v" , "--video", help="Caminho do vídeo a ser analisado.")

args = vars(ap.parse_args())

verifyArgsMessage = ""

if not path.exists(args["predictor_xml"]):
    verifyArgsMessage = "predictor-xml"

elif args["image"] is not None and not path.exists(args["image"]):
    verifyArgsMessage = "image"
    
elif args["video"] is not None and not path.exists(args["video"]):
    verifyArgsMessage = "video"


if verifyArgsMessage != "":
    print(f"O argumento inserido em {verifyArgsMessage} não foi encontrado!")
    quit()

boxerCascade = cv.CascadeClassifier(args["predictor_xml"])

if args["image"] is not None:
    try:
        nameFileOutput = args["image"].strip("/")[-1]
        img = cv.imread(args["image"])
        
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        boxers = boxerCascade.detectMultiScale(gray, 1.25, 5)

        for i,(x,y,w,h) in enumerate(boxers):
            cv.putText(img, f"Boxer #{i+1}", (x, y-10), cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
            cv.rectangle(img, (x,y), (x+w,y+h),(255, 0, 0), 2)

        cv.imshow("Boxers reconnhecidos - Esc para fechar", img)
        cv.waitKey(0)
        cv.imwrite(nameFileOutput + ".jpg", img)
        cv.destroyAllWindows()

        print("Imagem salva com sucesso!")
    except:
        print("Ocorreu um erro ao fazer a leitura da imagem.")

if args["video"] is not None:
        nameFileOutput = args["video"].strip("/")[-1]

        video = cv.VideoCapture(args["video"])

        size = (int(video.get(3)), int(video.get(4)))

        videoWriter = cv.VideoWriter(nameFileOutput + '.avi', 
                         cv.VideoWriter_fourcc(*'MJPG'),
                         10, size)

        while True:
            ret, frame = video.read()
            
            if ret:
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                boxers = boxerCascade.detectMultiScale(gray, 1.30, 5)

                for i,(x,y,w,h) in enumerate(boxers):
                    cv.putText(frame, f"Boxer #{i+1}", (x, y-10), cv.FONT_HERSHEY_PLAIN, 0.7, (255, 0, 0), 2)
                    cv.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)

                videoWriter.write(frame)

                cv.imshow("Boxers reconnhecidos - Esc para fechar", frame)

                key = cv.waitKey(60)
                if key == "27":
                    break
            else:
                break
        
        video.release()
        videoWriter.release()
        cv.destroyAllWindows()
        
        print("Vídeo salvo com sucesso!")