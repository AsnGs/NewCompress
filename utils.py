import os
import re
import csv
import sys
import copy
from tqdm import tqdm

from config import *

# 将连续的 nodeOffset+2 后归成连续组
def group_nodeOffset_plus2(n):
    if not n: return []
    nums = [i + 2 for i in n]
    groups = ''
    start = nums[0]
    end = nums[0]
    for num in nums[1:]:
        if num == end + 1:end = num
        else:
            # groups.append((start, end))
            groups = groups + str(start) + '-' + str(end)
            start = num
            end = num
    groups = groups + str(start) + '-' + str(end)
    return groups

