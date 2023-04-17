import cv2
import numpy as np
import math

def get_direction(pre_x, pre_y, x, y):
     '''
     p1과 p2사이의 방향값을 반환하는 함수
     p1과 p2는 (x, y) 좌표값을 가지는 튜플입니다
     '''
     dx = x - pre_x
     dy = y - pre_y
     angle = math.atan2(dy,dx)
     return angle

def distance(pre_x, pre_y, x, y):
    '''
    두점사이의 거리구하는 함수
    '''
    return ((x - pre_x) ** 2 + (y - pre_y) ** 2) ** 0.5

car_index = np.loadtxt("/Users/choehyeonseog/Desktop/Yolov5_DeepSort_Pytorch/boundingbox.txt", dtype=int)

inPath = "/Users/choehyeonseog/Desktop/test.mp4"

car_vector = np.array([])
car_label = np.array([])
car_frame = np.array([[]])

pts = np.array([[950, 730], [1050, 730], [1519, 1074], [491, 1074]], np.int32)

wid, hei = 1920, 1080

vc = cv2.VideoCapture(inPath)
if not vc.isOpened():
    print("can't open File")
    exit()

fps = vc.get(cv2.CAP_PROP_FPS)
width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))

car_label = np.array([])
#car_label에 디텍딩된 모든 라벨값 저장
for i in range(len(car_index)):
    car_label = np.append(car_label, car_index[i][1])

#라벨값 중복 제거
car_label_unique = np.unique(car_label)

for j in range(1, len(car_label_unique)):
    car_arr1 = np.array([])
    car_arr2 = np.array([])
    for i in range(len(car_index)):
                if car_index[i][1] == j:
                    '''
                    차량의 중앙 값을 계산해서 관심영역 지정
                    '''
                    midx = car_index[i][2] + car_index[i][4]//2
                    midy = car_index[i][3] + car_index[i][5]//2

                    mid = [float(midx), float(midy)]
                    mid = tuple(mid)

                    is_inside = cv2.pointPolygonTest(pts, (mid), False)

                    if is_inside > 0:
                         #print(mid)
                         print('roi안에 들어온 차량의 인덱스,프레임 : {},{}'.format(car_index[i][1], car_index[i][0]))

                         if i > 30:
                        #10프레임 이전 중앙 좌표값
                            pre_midx = car_index[i-30][2] + car_index[i-30][4]//2
                            pre_midy = car_index[i-30][3] + car_index[i-30][5]//2
                            #좌표값 거리 가 작으면 무시
                            dist = distance(pre_midx, pre_midy, midx, midy)
                            #print(dist)
                            if dist < 300:
                                continue
                            #방향값 계산 라디안값
                            angle = get_direction(pre_midx, pre_midy, midx, midy)
                            print(angle)
                            if angle >= -0.52 and angle <= 0.52:
                                print('칼치기')
                            # 두 번째 범위
                            elif angle >= -3.14 and angle < -2.57:
                                print('칼치기')
                            # 세 번째 범위
                            elif angle > 2.57 and angle <= 3.14:
                                print('칼치기')
                            
                            

                            car_arr1 = np.append(car_arr1, angle)
                            car_arr2 = np.append(car_arr2, car_index[i][0])

                    
    car_vector = np.append(car_vector, car_arr1)
    car_frame = np.append(car_frame, car_arr2)
    car_vector = np.append(car_vector, '/')
    car_frame = np.append(car_frame, '/')
#outPath = folderPath + "stop" + str(fileCnt) + ".mp4"
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#vw = cv2.VideoWriter(outPath, fourcc, fps, (width, height))

if vc.isOpened():
    while True:
        ret, img = vc.read()
        if ret:
            resized_img = cv2.resize(img, (wid, hei))
            cv2.polylines(resized_img, [pts], True, (0,255,255), 3)
            cv2.imshow('resized_img', resized_img)
            # mask = np.zeros_like(img)
            # cv2.fillPoly(mask, [pts], (255, 255, 255))

            
            cv2.waitKey(33)
        else:
            break
else:
    print('cannot open the file')
 