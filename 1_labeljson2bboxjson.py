import argparse
import json


def parse_args():
    """Use argparse to get command line arguments."""
    # label_path: 原始label文件存储位置
    # det_path : 生成的bbox的信息文件存储位置
    # 下面只是对训练集进行解析，测试机可以得到同样的结果。
    parser = argparse.ArgumentParser()
    parser.add_argument('--label_path', type=str,default='C:\\Users\\wangbo\\Documents\\EGDownloads\\bdd100k_labels_release\\bdd100k\\labels\\bdd100k_labels_images_train.json')
    parser.add_argument('--det_path', type=str,default='C:\\Users\\wangbo\\Documents\\EGDownloads\\bdd_dect\\detection_train.json ')
    args = parser.parse_args()

    return args




def label2det(frames):
    # dataframs为一个列表，每个元素是一个字典，用于表示一张image的所有label；
    # 有“name”属性：这张图片名称
    # 有“label”属性：对应的是一个列表，每个元素是一个字典；

    boxes = list()
    for frame in frames:
        for label in frame['labels']:
            if 'box2d' not in label:
                continue
            xy = label['box2d']
            if xy['x1'] >= xy['x2'] or xy['y1'] >= xy['y2']:
                continue
            box = {'name': frame['name'],
                   'timestamp': frame['timestamp'],
                   'category': label['category'],
                   'bbox': [xy['x1'], xy['y1'], xy['x2'], xy['y2']],
                   'score': 1}
            boxes.append(box)
    return boxes


def convert_labels(label_path, det_path):
    # 第一步：解析原始json文件
    frames = json.load(open(label_path, 'r'))
    # 第二步：得到所有的bbox信息
    det = label2det(frames)
    # 第三步：存储所有的bbox信息为json文件
    json.dump(det, open(det_path, 'w'), indent=4, separators=(',', ': '))


def main():
    args = parse_args()
    convert_labels(args.label_path, args.det_path)


if __name__ == '__main__':
    main()