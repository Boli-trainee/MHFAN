import torch
from torch.utils.data import Dataset
import os
import random
# from image import *
import h5py
import cv2
from PIL import Image
import numpy as np
import numbers
from torchvision import datasets, transforms
import  sys
# 加入路径使得模块能被导入
sys.path.append("D:\libo\FIDTM-master")

def load_data_fidt(img_path, args, train=True):
    # gt_path = img_path.replace('.jpg', '.h5').replace('images', 'gt_fidt_map')
    # img_path = '.' + img_path
    img = Image.open(img_path).convert('RGB')

    # while True:
    #     try:
    #         gt_file = h5py.File(gt_path)
    #         k = np.asarray(gt_file['kpoint'])
    #         fidt_map = np.asarray(gt_file['fidt_map'])
    #         break
    #     except OSError:
    #         print("path is wrong, can not load ", img_path)
    #         cv2.waitKey(1000)  # Wait a bit

    img = img.copy()
    # fidt_map = fidt_map.copy()
    # k = k.copy()
    return img
    # return img, fidt_map, k

class listDataset(Dataset):
    def __init__(self, root, shape=None, shuffle=True, transform=None, train=False, seen=0, batch_size=1,
                 num_workers=4, args=None):
        if train:
            random.shuffle(root)

        self.nSamples = len(root)
        self.lines = root
        self.transform = transform
        self.train = train
        self.shape = shape
        self.seen = seen
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.args = args

    def __len__(self):
        return self.nSamples

    def __getitem__(self, index):
        assert index <= len(self), 'index range error'

        if self.args['preload_data'] == True:
            fname = self.lines[index]['fname']
            img = self.lines[index]['img']
            # kpoint = self.lines[index]['kpoint']
            # fidt_map = self.lines[index]['fidt_map']

        else:
            img_path = self.lines[index]
            fname = os.path.basename(img_path)
            img = load_data_fidt(img_path, self.args, self.train)
            # img, fidt_map, kpoint = load_data_fidt(img_path, self.args, self.train)

        '''data augmention'''
        if self.train == True:
            if random.random() > 0.5:
                fidt_map = np.fliplr(fidt_map)
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
                kpoint = np.fliplr(kpoint)

        # fidt_map = fidt_map.copy()
        # kpoint = kpoint.copy()
        img = img.copy()

        if self.transform is not None:
            img = self.transform(img)

        '''crop size'''
        if self.train == True:
            fidt_map = torch.from_numpy(fidt_map).cuda()

            width = self.args['crop_size']
            height = self.args['crop_size']
            # print(img.shape)
            crop_size_x = random.randint(0, img.shape[1] - width)
            crop_size_y = random.randint(0, img.shape[2] - height)
            img = img[:, crop_size_x: crop_size_x + width, crop_size_y:crop_size_y + height]
            kpoint = kpoint[crop_size_x: crop_size_x + width, crop_size_y:crop_size_y + height]
            fidt_map = fidt_map[crop_size_x: crop_size_x + width, crop_size_y:crop_size_y + height]
            fidt_map = torch.from_numpy(fidt_map).cuda()

            # width = self.args['crop_size']
            # height = self.args['crop_size']
            # # print(img.shape)
            # crop_size_x = random.randint(0, img.shape[1] - width)
            # crop_size_y = random.randint(0, img.shape[2] - height)
            # img = img[:, crop_size_x: crop_size_x + width, crop_size_y:crop_size_y + height]
            # kpoint = kpoint[crop_size_x: crop_size_x + width, crop_size_y:crop_size_y + height]
            # fidt_map = fidt_map[crop_size_x: crop_size_x + width, crop_size_y:crop_size_y + height]

        return fname, img
        # return fname, img, fidt_map, kpoint

