#-*- coding: utf-8 -*-
__author__ = 'admin'

import os
import inspect

#获取绝对路径
def get_absolute_dir(dir):
    if not os.path.isabs(dir):
        this_file = inspect.getfile(inspect.currentframe())
        cur_dir = os.path.abspath(os.path.dirname(this_file))
        return os.path.abspath(cur_dir + os.path.sep + dir)
    else:
        return dir