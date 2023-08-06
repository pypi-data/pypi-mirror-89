import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pylib_kittenai')))

import pytest

# 以上为测试用例初始化，在板子上跑不需要加

import time
from kittenai import *
from kittenmedia import *

media = KittenMedia()
media.start()

baiduAi = BaiduAI()

while True:
  au = media.waitAudio()
  if au:
    result = baiduAi.speech2text(au)
    print("识别结果:", result)
