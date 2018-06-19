import numpy as np
import matplotlib.pyplot as plt
from gabriel import Gabriel

class Empty_Space(object):
    def __init__(self, data):
        self.gabriel = Gabriel(data)
        self.data = data
