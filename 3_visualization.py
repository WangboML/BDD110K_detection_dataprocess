import os
import cv2
import numpy as np




img_files=[]
label_files=[]

list_path='C:\\Users\\wangbo\\Documents\\EGDownloads\\bdd_dect\\train.txt'

#list.path中保存的是名字，我们使用的时候需要将文件位置也包含在内才能去寻找
# 得到所有图片和和对用的label的位置列表：两者一一对应
for image_path in open(list_path, 'r'):
   # 有时候image_path的默认地址可能与真实所在的地址不一样(修改前缀)
    image_path = os.path.join("C:\\Users\\wangbo\\Documents\\EGDownloads\\bdd100k_images\\bdd100k\\images\\100k\\train",image_path.rstrip()).rstrip()
    label_path = image_path.replace('\\bdd100k_images\\bdd100k\\images\\100k\\train\\', '\\bdd_dect\\train\\').replace('.png', '.txt').replace('.jpg', '.txt').strip()
    if os.path.isfile(label_path):
        img_files.append(image_path)
        label_files.append(label_path)


for index in range(len(img_files)):
    img_path = img_files[index % len(img_files)].rstrip()
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    if img is None:
        raise Exception("Read image error: {}".format(img_path))
    h, w, _ = img.shape
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 得到第index个图片对应的label文件地址；并且读取为多行五列的数组；shape是（n，5）
    label_path = label_files[index % len(img_files)].rstrip()

    if os.path.exists(label_path):
        labels = np.loadtxt(label_path).reshape(-1, 5)
    else:
        #logging.info("label does not exist: {}".format(label_path))
        labels = np.zeros((1, 5), np.float32)
    image = img
    #h, w = image.shape[:2]
    for l in labels:
        if l.sum() == 0:
            continue
        x1 = int((l[1] - l[3]/2 ) * w)
        y1 = int((l[2] - l[4]/2 ) * h)
        x2 = int((l[1] + l[3]/2 ) * w)
        y2 = int((l[2] + l[4]/2 ) * h)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite("step{}.jpg".format(index), image)
