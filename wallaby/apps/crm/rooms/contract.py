# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

from invoice import *

class Contract(Invoice):

    def __init__(self, name):
        Invoice.__init__(self, name)

