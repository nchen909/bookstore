# coding=utf-8
"""图片hash相关的工具函数集"""

from .tool import Tools
import base64
from io import BytesIO
import imagehash
import os
import heapq
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from tqdm import tqdm


class HashTool:
    """生成图片hash相关的工具函数集"""
    @staticmethod
    def get_pil(picture):
        """BufferReader转base64转PIL变大小"""
        # image=base64.b64encode(picture)
        image=picture
        image = BytesIO(image)
        image = Image.open(image)
        # return image.thumbnail((100, 60))
        # if image.format =='JPEG':
        #     raise TypeError
        return image.resize((200,120))

    @staticmethod
    def file_pil(picture):
        """输入的文件转base64转PIL转哈希"""
        image = Image.open(picture)
        # image=picture
        return HashTool.get_file_hash(image)

    @staticmethod
    def buffer_pil(picture):
        """BufferReader转base64转PIL转哈希"""
        # image=base64.b64encode(picture)
        image=picture
        # print('image:',image)
        # print("image.decode('utf-8'):",image.decode('utf-8'))
        # image = base64.b64decode(image)
        image = BytesIO(image)
        image = Image.open(image)
        return HashTool.get_file_hash(image)

    @staticmethod
    def get_file_hash(image):
        """获取图片文件的hash值"""
        return imagehash.phash(image)

    @staticmethod
    def get_files_hash(directory) -> [tuple]:
        """获取文件夹下所有图片的hash值
        
        Returns:
            list: 元组(ImageHash,full_path)构成的列表

        """

        file_names = os.listdir(directory)
        l = []
        for file_name in tqdm(file_names, ncols=10):
            full_path = os.path.join(directory, file_name)
            hashv = HashTool.get_file_hash(full_path)
            l.append((hashv, full_path))
        return l

    @staticmethod
    def n_smallest(tuple_list, target_hash, n):
        """从元组的列表中找出hash与目标差值最小的n张图片,元组的第一项应为该图片hash值
        
        Returns:
            list: 找到tuple构成的列表
        """
        return heapq.nsmallest(n, tuple_list, key=lambda t: t[0] - target_hash)


class HashEngine:
    """使用图片hash进行判断的函数集"""

    @staticmethod
    def mean_distance(tuple_list, target_hash):
        """计算target_hash与tuple_list中所有hash的平均hamming距离
        
        Args:
            list: tuple_list (ImageHash,...)元组构成的列表,元组第一个元素必须为ImageHash

        Returns:
            int : target_hash与tuple_list中所有hash的平均hamming距离
        """

        total_dist = 0
        for t in tuple_list:
            dist = t[0] - target_hash
            total_dist += dist
        return total_dist / len(tuple_list)

# # thehash=HashTool.get_file_hash(r'F:\Desktop\世界名画\Snipaste_2019-10-11_19-22-11.png')
# thehash=HashTool.get_file_hash(r'F:\Desktop\hash\1.png')
# print(thehash)
# final=HashTool.n_smallest(HashTool.get_files_hash(r'F:\Desktop\世界名画'),thehash,3)
# # print(final)
# for i in final:
#     print(1-HashEngine.mean_distance([i],thehash)/64)
#     print(i[1])