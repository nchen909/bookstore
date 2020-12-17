import os

import numpy as np
from PIL import Image
from tqdm import tqdm

class Tools:
    """提供一般性的常用函数
    """
    @staticmethod
    def create_save_dir(path):
        if(not os.path.exists(path)):
            os.makedirs(path)

    @staticmethod
    def removeDir(dirPath):
        if not os.path.isdir(dirPath):
            return
        files = os.listdir(dirPath)
        for file in files:
            filePath = os.path.join(dirPath,file)
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif os.path.isdir(filePath):
                    Tools.removeDir(filePath)
        os.rmdir(dirPath)
        
    @staticmethod
    def delete_file_if_exist(filepath): 
        if os.path.isfile(filepath):
            os.remove(filepath)
