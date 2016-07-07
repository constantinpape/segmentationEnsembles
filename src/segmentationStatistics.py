import numpy
import vigra

import matplotlob.pyplot as plt

# return several statistics about the segmentation
class SegmentationStatistics(object):

    def __init__(segmentation):
        self.seg = segmentation


