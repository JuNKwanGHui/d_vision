import cv2
import math
import numpy as np

fileCnt = 1
car_index = np.loadtxt("/Users/choehyeonseog/Desktop/Yolov5_DeepSort_Pytorch/boundingbox4.txt", dtype=int)
vid = "/Users/choehyeonseog/Desktop/Yolov5_DeepSort_Pytorch/test_vid.mp4"
cap = cv2.VideoCapture(vid)

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

def car_vec(car_index):
    car_vector = np.array([])
    car_label = np.array([])
    for i in range(len(car_index)):
        car_label = np.append(car_label, car_index[i][1])
    car_label_unique = np.unique(car_label)

    for j in range(len(car_label_unique)):
            car_arr1 = np.array([])
            car_arr2 = np.array([])
            for i in range(len(car_index)):
                if car_index[i][1] == j:
                    #bbox의 중앙 좌표 구하기
                    midx = car_index[i][2] + car_index[i][4]//2
                    midy = car_index[i][3] + car_index[i][5]//2
                    '''
                    두 좌표 사이의 값이 특정 값 이하면 무시하기 => 방향이 일정하다. => 내가 가는 방향이랑 같다. 같은속력으로
                    아니면 내가 정지하고 있을때 정지하고 있는 차량이다.
                    '''

                    if i > 10:
                        #10프레임 이전 중앙 좌표값
                        pre_midx = car_index[i-10][2] + car_index[i-10][4]//2
                        pre_midy = car_index[i-10][3] + car_index[i-10][5]//2
                        #좌표값 거리 가 작으면 무시
                        dist = distance(pre_midx, pre_midy, midx, midy)
                        #print(dist)
                        if dist < 300:
                            continue
                        #방향값 계산 라디안값
                        angle = get_direction(pre_midx, pre_midy, midx, midy)
                        car_arr1 = np.append(car_arr1, angle)
                        #car_arr2 = np.append(car_arr2, car_index[i][0])
                        #print(car_arr1)
            
            #car_vector는 방향값 좌표 저장한 list 차량마다 '/'로 구분
            car_vector = np.append(car_vector, car_arr1)
            #car_frame = np.append(car_frame, car_arr2)
            car_vector = np.append(car_vector, '/')
                    #여기 안에서 백터값 계산

    return car_vector

def car_vec_com(car_index):
    car_vector1 = car_vec(car_index)
    car_vi_vi = car_vector1
    #car_frame_f = car_frame
    car_vector_forcar = []
    #car_frame_forcar = []
    event_frame = []
    for i in range(len(car_vi_vi)):
        '''
        car_vi 배열에 들어있는 값에서 '/'가 나올때까지 car_scale_forcar에 append
        '/'가 나오면 car_scale_forcar에 들어있는 만큼 + '/' 까지 해서 car_vi 배열 앞에서 부터 삭제
        for문으로 car_vi의 길이만큼 반복
        '''
        if car_vi_vi[i] == '/':
            #################
            #여기에 이제 빨간불 비교연산
            #################

            # 방향값 차마다 자름
            print(car_vector_forcar)
            car_vector_forcar = []
            car_vector1 = np.delete(car_vector1, 0)
            
            #car_frame_forcar = []
            #car_frame = np.delete(car_frame, 0)
        else:

            car_vector_forcar = np.append(car_vector_forcar,round(float(car_vi_vi[i]),3))
            car_vector1 = np.delete(car_vector1, 0)
            #car_frame_forcar = np.append(car_frame_forcar, car_frame_f[i])
            #car_frame = np.delete(car_frame, 0)
    

    return event_frame

#print(car_vector)

def main():
    #event_frame = []
    event_frame = car_vec_com(car_index)
    #print(event_frame)
    #car_scale_com(car_index)
    if cap.isOpened():
        while True:
            ret, img = cap.read()
            if ret:
                cv2.imshow(vid, img)
                cv2.waitKey(33)
            else:
                break
        else:
            print('cannot open the file')
 
    cap.release()
    cv2.destroyAllWindows()
    return event_frame


if __name__ == "__main__":
    main()