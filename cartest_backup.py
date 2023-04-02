import cv2
import numpy as np
#파일을 불러와 2차원배열로 저장
car_index = np.loadtxt("/Users/choehyeonseog/Desktop/Yolov5_DeepSort_Pytorch/boundingbox.txt", dtype=int)
#numpy 배열 모두 표시
np.set_printoptions(threshold=np.inf)

def car_scale(car_index):
    car_label = np.array([])
    #car_label에 디텍딩된 모든 라벨값 저장
    for i in range(len(car_index)):
        car_label = np.append(car_label, car_index[i][1])

    #라벨값 중복 제거
    car_label_unique = np.unique(car_label)

    car_vi = np.array([[]])
    car_frame = np.array([[]])
    car_mid = []
    '''
    중복제거된 라벨값만큼 j가 돈다.
    i가 돌면서 파일에서 읽어온값에서 스케일 값을 계산한다.
    car_arr1에 j번째 차량크기를 car_vi배열을 저장한다 (디텍팅x = 0)
    다음차량으로 올때는 car_arr1배열을 초기화하고 다시 for문을 돈다
    차량끼리 구분 기호는 '/' 이다
    '''
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
                #관심영역 박스 (900, 650, 250, 150) = (x, y, w, h)
                if 1150 >= midx >= 900 and 800 >= midy >= 650:
                    car_scale = car_index[i][4] * car_index[i][5]
                    car_arr1 = np.append(car_arr1, car_scale)
                    car_arr2 = np.append(car_arr2, car_index[i][0])
                else:
                    pass
        car_vi = np.append(car_vi, car_arr1)
        car_frame = np.append(car_frame, car_arr2)
        car_vi = np.append(car_vi, '/')
        car_frame = np.append(car_frame, '/')

    return car_vi, car_label_unique, car_frame

def car_scale_com(car_index):
    
    car_vi, car_label_unique, car_frame = car_scale(car_index)
    car_vi_vi = car_vi
    car_frame_f = car_frame
    car_scale_forcar = []
    car_frame_forcar = []
    for i in range(len(car_vi_vi)):
        '''
        car_vi 배열에 들어있는 값에서 '/'가 나올때까지 car_scale_forcar에 append
        '/'가 나오면 car_scale_forcar에 들어있는 만큼 + '/' 까지 해서 car_vi 배열 앞에서 부터 삭제
        for문으로 car_vi의 길이만큼 반복
        '''
        if car_vi_vi[i] == '/':
            for j in range(len(car_scale_forcar)):
                if  j > len(car_scale_forcar):
                    pass
                elif car_scale_forcar[j] == 0:
                    pass
                #프레임 단위차량 크기 비교연산
                elif float(car_scale_forcar[j]) >= float(car_scale_forcar[j-1]) * 1.1:
                    print(car_frame_forcar[j])
                    print("급정지")
            
            car_scale_forcar = []
            car_vi = np.delete(car_vi, 0)
            car_frame_forcar = []
            car_frame = np.delete(car_frame, 0)
        else:
            car_scale_forcar = np.append(car_scale_forcar,car_vi_vi[i])
            car_vi = np.delete(car_vi, 0)
            car_frame_forcar = np.append(car_frame_forcar, car_frame_f[i])
            car_frame = np.delete(car_frame, 0)


def main():
    car_scale_com(car_index)

if __name__ == "__main__":
    main()