import cv2
import cartest3

inPath = "/Users/choehyeonseog/Desktop/test.mp4" # 파일명 포함한 입력파일 경로
outPath = ""
folderPath = "/Users/choehyeonseog/Desktop/" # 저장할 폴더경로
fileCnt = 1
event_f = 0
frameCnt = 0
event_frame = cartest3.main()

# 리스트의 각 요소를 float로 변환
event_frame = [float(frame) for frame in event_frame]
# 리스트를 정렬
event_frame.sort()
print(event_frame)

vc = cv2.VideoCapture(inPath)
if not vc.isOpened():
    print("can't open File")
    exit()

fps = vc.get(cv2.CAP_PROP_FPS)
width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))

outPath = folderPath + "stop" + str(fileCnt) + ".mp4"
print("outputPath", outPath)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
vw = cv2.VideoWriter(outPath, fourcc, fps, (width, height))


while True:
    try:
        ret, frame = vc.read()
        if ret: 
            frameCnt += 1
            if frameCnt == event_frame[event_f]:
                #vw = cv2.VideoWriter(outPath, fourcc, fps, (width, height)) 
                fileCnt += 1
                event_f += 1
                outPath = folderPath + "stop" + str(fileCnt) + ".mp4"
                print("outputPath", outPath)
                for i in range(30):
                    ret, frame = vc.read()
                    vw.write(frame)
                print("--")

                vw = cv2.VideoWriter(outPath, fourcc, fps, (width, height))
                
                #vw.write(frame)
            else:
                pass
        else:
            break
    except:
        break

    

vw.release()