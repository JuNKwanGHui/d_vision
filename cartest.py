import cv2

f = open("/Users/choehyeonseog/Desktop/Yolov5_DeepSort_Pytorch/boundingbox.txt","r")
car_scale = [[] for _ in range(1000)]
car_label = []

while True:
    line = f.readline()
    if not line: break
    
    line_split = line.split()
    
    #자동차 스케일 확인후 car_scale_v변수에 저장
    car_scale_v = int(line_split[4]) * int(line_split[5])
    car_label_v = int(line_split[1])
    frame = int(line_split[0])
    #car_scale.
    car_scale.append(car_scale_v)
    car_scale.append(frame)
    car_scale.append(car_label_v)
    car_label.append(car_label_v)

car_scale_2 = [[] for _ in range(len(car_scale))]

for i in range(len(car_scale)):
    if car_scale[i]:
        for j in range(1, len(set(car_label))):
            if j == car_scale[i][0]:
                car_scale_2[j-1].append(car_scale[i][2])
        
print(car_scale_2)

# for i in range(len(car_label)):
#     print(i)
#     if car_label[i] == 2:
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
