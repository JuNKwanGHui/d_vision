import cv2
import numpy as np

f = open("/Users/choehyeonseog/Desktop/Yolov5_DeepSort_Pytorch/boundingbox.txt","r")
line = f.readline()
#print(len(line))
#car_scale = [[]for _ in range(1000)]
car_scale = np.array([[]for _ in range(1000)])
car_scale_2 = [[]for _ in range(1000)]
car_label = []
car_dict = {}
i = 0

while True:
    line = f.readline()
    if not line: break
    
    line_split = line.split()
    
    #자동차 스케일 확인후 car_scale_v변수에 저장
    car_scale_v = int(line_split[4]) * int(line_split[5])
    frame = int(line_split[0])
    car_label_v = int(line_split[1])
    #car_scale.
    car_scale[i] = np.append(car_scale[i], car_label_v)
    car_scale[i] = np.append(car_scale[i], frame)
    car_scale[i] = np.append(car_scale[i], car_scale_v)
    i += 1
    #print(i)
    
    car_label.append(car_label_v)

    #라벨값을 확인하여 딕셔너리에 저장

    #car_dict = {line_split[1]:car_scale} 
    
    

    line_split[1]
    

    

    #print(line_split)

#print(car_scale)

# print(len(car_scale))
# for i in range(len(set(car_label))):
#     print(i)
#     for j in range(len(car_scale)):
#         if car_scale[j] == i:
#             car_scale_2[car_label].append(car_scale[j][2])

car_scale_2 = [[]*len(car_scale) for _ in range(len(car_scale))]

for i in range(len(car_scale)):
    if car_scale[i]:
        for j in range(1, len(set(car_label))):
            if j == car_scale[i][0]:
                car_scale_2[j-1].append(car_scale[i][2])
        
print(car_scale_2)


car_label_arr = []
car_scale_arr = []

#print(car_label)
#print(car_scale)

# for i in range(len(set(car_label))):
#     #globals()["car_dict{}".format(i)] = i
#     car_label_arr.append(i + 1)

# for i in range(len(car_label)):
#     for j in car_label_arr:
#         if car_label[i] == j:
#             #차량 크를 디렉터리에 넣어줌
#             car_dict[j] = car_scale[i]
#             if car_scale[i-1] <= car_scale[i]:
#                 print(car_scale[i-1], car_dict[j])
#                 print('stop={0} , 급정지!!'.format(i))
            #print('detection={0}'.format(i), car_dict)

# for i in range(len(car_label)):
#     print(i)
    #if car_label[i] == 2:
        #print(car_label[i])
        #print(car_scale[i-1], car_scale[i])
        #if car_scale[i-1] * 1.2 <= car_scale[i]:
            #print('stop={0} , 급정지!!'.format(i))


# for i in range(len(car_label_arr)):
#     for j in range(len(car_label)):
#         if car_label[j] == i:
#             car_dict[j] = car_scale[i]
#             # car_scale_arr.append(car_scale[i])
#             # car_dict = {car_label[j] :car_scale_arr}
#             print(car_dict)

#print(car_dict)





#print(car_dict)
    

#print(car_dict)
#print(car_dict)

#for i in range(len(car_scale)):

f.close()
