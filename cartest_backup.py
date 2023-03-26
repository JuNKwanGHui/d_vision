import cv2
import numpy as np
#파일을 불러와 2차원배열로 저장
car_index = np.loadtxt("/Users/choehyeonseog/Desktop/Yolov5_DeepSort_Pytorch/boundingbox.txt", dtype=int)
#print(car_index)
np.set_printoptions(threshold=np.inf)

def car_scale(car_index):
    car_label = np.array([])
    #car_label에 디텍딩된 모든 라벨값 저장
    for i in range(len(car_index)):
        car_label = np.append(car_label, car_index[i][1])

    #라벨값 중복 제거
    car_label_unique = np.unique(car_label)

    car_vi = np.array([[]])
    '''
    중복제거된 라벨값만큼 j가 돈다.
    i가 돌면서 파일에서 읽어온값에서 스케일 값을 계산한다.
    car_arr1에 j번째 차량크기를 car_vi배열을 저장한다 (디텍팅x = 0)
    다음차량으로 올때는 car_arr1배열을 초기화하고 다시 for문을 돈다
    차량끼리 구분 기호는 '/' 이다
    '''
    for j in range(1, len(car_label_unique)):
        car_arr1 = np.array([])
        for i in range(len(car_index)):
            if car_index[i][1] == j:
                car_scale = car_index[i][4] * car_index[i][5]
                car_arr1 = np.append(car_arr1, car_scale)
            else:
                car_arr1 = np.append(car_arr1, 0)
        car_vi = np.append(car_vi, car_arr1)
        car_vi = np.append(car_vi, '/')

    #non_car_vi = np.nonzero(car_vi)
    #print(car_vi)
    return car_vi , car_label_unique

def car_scale_com(car_index):
    
    car_vi, car_label_unique = car_scale(car_index)
    car_vi_vi = car_vi
    car_scale_forcar = []
    for i in range(len(car_vi_vi)):
        if car_vi_vi[i] == '/':
            print(car_scale_forcar)
            #여기에 이제 비교연산
            car_scale_forcar = []
            car_vi = np.delete(car_vi, 0)
        else:
            car_scale_forcar = np.append(car_scale_forcar,car_vi_vi[i])
            car_vi = np.delete(car_vi, 0)


    #print(car_vi)

def main():
    car_scale_com(car_index)

if __name__ == "__main__":
    main()