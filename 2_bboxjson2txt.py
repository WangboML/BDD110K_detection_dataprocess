import os
import json


train_det_json='C:\\Users\\wangbo\\Documents\\EGDownloads\\bdd_dect\\detection_train.json'
# # 对它进行解析

# #1、生成train.txt、val.txt
# #2、生成det_label文件夹：两个子文件夹：train、val；用于保存train和val的目标检测label；每张图片的检测结果以同样的方式命名；

# 所有目标检测的标签信息。它的index表示数字类别
class_names = ['car', 'bus', 'person',
               'bike', 'truck', 'motor', 'train',
               'rider', 'traffic sign', 'traffic light']
#
src = json.load(open(train_det_json))
    # 得到元json文件中所有的元素列表，
    # 每个元素都是
    # {'name': '0000f77c-6257be58.jpg', 'timestamp': 10000, 'category': 'traffic light', 'bbox': [1125.902264

### 生成txt名称文档文档
filenames=[]
# 首先得到所有的图片名称，当然有重复的（有一百多万呢）

for i in range(len(src)):
    anno = src[i]
    filename = anno['name']
    filenames.append(filename)

#所有包含目标的图片名称列表（经过下面之后就只有69863张image了）
filenames = list(set(filenames))



#### 首先生成所有名称的txt文档
txt_file = 'C:\\Users\\wangbo\\Documents\\EGDownloads\\bdd_dect\\train.txt'
with open(txt_file, 'w') as txt_file:
    for filename in filenames:
        txt_file.write(filename + '\n')






H=720
W=1280
# 首先定义每张图片生成的label.txt保存位置：
for filename in filenames:# 针对每张image生成一个一个txt文档
    image_txt=os.path.join('C:\\Users\\wangbo\\Documents\\EGDownloads\\bdd_dect\\train\\',
                           filename.split(".")[0]+".txt")
    with open(image_txt, 'w') as txt_file:
        for i in range(len(src)):
            anno = src[i]
            if anno["name"]==filename:
                category = anno['category']
                bbox = anno['bbox'] #xmin ymin xmax ymax

                # 相对的    中心和宽与高
                x_center=(bbox[0]+bbox[2])/(2*W)
                y_center = (bbox[1] + bbox[3]) / (2 * H)
                width=(bbox[2]-bbox[0])/W
                height = (bbox[3] - bbox[1]) / H
                class_num = class_names.index(category)
                txt_file.write(
                    str(class_num) + ' ' + str(x_center) + ' ' + str(y_center) + ' ' + str(width)
                    + ' ' + str(
                        height) + '\n')
                #对同一个文件得到的label信息为str，bbox也被变成str