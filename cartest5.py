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
    car_scale[frame].append(car_scale_v)
    car_scale[frame].append(frame)
    car_scale[frame].append(car_label_v)
    car_label.append(car_label_v)

car_scale_2 = [[] for _ in range(len(car_label))]

for i in range(len(car_scale)):
    if car_scale[i]:
        for j in range(1, len(set(car_label))+1):
            if j == car_scale[i][2]:
                car_scale_2[j-1].append(car_scale[i][0])
        
print(car_scale_2)
