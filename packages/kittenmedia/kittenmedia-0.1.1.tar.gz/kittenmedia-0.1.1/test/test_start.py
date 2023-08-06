import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
# 以上为测试用例初始化，在板子上跑不需要加
import time
from kittenmedia import *

s = KittenMedia()
s.start()

a = input()

# s.pop()
# img = s.waitImage()
# print("got image", img)
# s.stop()