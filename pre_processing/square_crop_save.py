# coding: utf-8

# In[1]:


# 파일 이름 중복 위험 주의
## 덮어씌울 땐 상관없지만, 그렇지 않다면 file_num 번호를 바꿔주세요.
file_num = 1


# In[2]:


import cv2
import pandas as pd
import os
import sys


def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path) 

def onMouse(event, x, y, flags, param):
    global isDragging, x0, y0, x1, y1, image
    if event == cv2.EVENT_LBUTTONDOWN:
        isDragging = True
        x0 = x
        y0 = y
        
    elif event == cv2.EVENT_MOUSEMOVE:
        if isDragging:
            image_draw = image.copy()
            cv2.rectangle(image_draw, (x0, y0), (x, y), blue, 2)
            cv2.imshow('image', image_draw)
            
    elif event == cv2.EVENT_LBUTTONUP:
        if isDragging:
            isDragging = False
            x1 = x
            y1 = y
            
            w = x1 - x0
            h = y1 - y0
            if w > 0 and h > 0:
                image_draw = image.copy()
                cv2.rectangle(image_draw, (x0, y0), (x1, y1), red, 2)
                cv2.imshow('image', image_draw)
                roi = image[y0:y1, x0:x1]
                cv2.imwrite(crop_path+'/'+file_name, roi) # 컬러이미지 crop 후 저장합니다.
                
            else:
                cv2.imshow('image', image)
                print('drag should start from left-top side')


# In[3]:


# Points 들을 저장할 리스트와 Crop이 실행 되었는지 저장할 Boolean 변수를 선언합니다.
isDragging = False
x0, y0, w, h = -1, -1, -1, -1
blue, red = (255, 0, 0), (0, 0, 255)
tmp = []

df = pd.DataFrame(columns=['x1', 
                           'y1', 
                           'x2', 
                           'y2', 
                           'folder_name', 
                           'file_name', 
                           'brand', 
                           'car', 
                           'year', 
                           'time', 
                           'H', 
                           'V'
                          ])
print("새로운 df",file_num," 생성")

csv_path = './csv/'

## csv 파일 이름이 겹치지 않게 조심하세요.
csv_name = '/k-car_ys'+str(file_num)+'.csv'
make_dir(csv_path)


# In[4]:


# main

# 필요한 폴더가 없을 경우 자동으로 생성합니다.
origin_dir = os.path.join('./before/')
cropped_dir = os.path.join('./after/color/')
cropped_g_dir = os.path.join('./after/gray/')

make_dir(cropped_dir)
make_dir(cropped_g_dir)
    
# before dir.
folder_list = os.listdir(origin_dir)

# 폴더 이름
for folder_name in folder_list:
    print(folder_list)
    file_path = os.path.join(origin_dir,folder_name) 
    
    crop_path = os.path.join(cropped_dir,folder_name) # 컬러 사진
    crop_g_path = os.path.join(cropped_g_dir,folder_name) # 회색조 변환 사진 -> 미정
    
    make_dir(crop_path)
    make_dir(crop_g_path)
    
    # 현재 폴더 안 이미지의 list
    file_list = os.listdir(origin_dir + '/' + folder_name)
    print("폴더 번호 ", folder_name, " : " , len(file_list), "개\n")
    
    # 모든 파일 .jpg로 확장자를 변경
    for x in file_list:
        tmp = os.path.splitext(x)
        src = os.path.join(file_path,x)
        dst = file_path+ '/' + tmp[0]+'.jpg'
        os.rename(src, dst)
        
    # 확장자 변경 후 list
    file_list = os.listdir(origin_dir + '/' + folder_name)
    
    
    # 파일 이름 리스트
    for file_name in file_list:
        # 파일 이름 구분
        for x in file_list:
            tmp = x[:-4].split('_')
        
        # 이미지를 load 합니다.
        image = cv2.imread(file_path+'/'+file_name)
        
        # 원본 이미지를 clone 하여 복사해 둡니다.
        clone = image.copy()
        
        # 새 윈도우 창을 만들고 그 윈도우 창에 click_and_crop 함수를 세팅해 줍니다.
        cv2.namedWindow("image")
        cv2.setMouseCallback('image', onMouse)

        while True:
            # 이미지를 출력하고 key 입력을 기다립니다.
            cv2.imshow("image", image)
            key = cv2.waitKey(0) & 0xFF
            
            # 만약 r이 입력되면, crop 할 영열을 리셋합니다.
            if key == ord("r"):
                image = clone.copy()
                
             # 만약 c가 입력되면 작업 좌표를 확인합니다.
            elif key == ord("c"):
                print("(",x0,y0,"),","(",x1,y1,")")
   

            # 만약 q가 입력되면 작업을 끝냅니다.
            elif key == ord("q"):
                df.to_csv(csv_path + csv_name, index = False)
                cv2.destroyAllWindows()
                sys.exit("You pressed 'q' key")

            # 만약 spacebar가 입력되면 다음으로 넘어갑니다.
            elif key == ord(" "):
                data = {
                'x1' : [x0], 
                'y1' : [y0],
                'x2' : [x1],
                'y2' : [y1],
                'folder_name' : [folder_name],
                'file_name' : [file_name],
                'brand' : [tmp[0]],
                'car' : [tmp[1]],
                'year' : [tmp[2]],
                'in_out(time)' : [tmp[3]],
                'H' : [tmp[4]],
                'V' : [tmp[5]]
                } 
                
                df = df.append(pd.DataFrame(data))      # 데이터프레임에 행 추가
                df.to_csv(csv_path + csv_name, index = False) # 다운됐을 때 비상용
                print(df,'\n')
                break
                
df.to_csv(csv_path + csv_name, index = False) # file path, file name        
