import vigra
import numpy as np

#from volumina_viewer import volumina_n_layer

#class SegmentationEnsemble(object):
#
#    def __init__(segmentation_paths, raw_path):
#        self.segmentation_paths = segmentation_paths
#        self.raw_path = raw_path
#
#
#    def make_rags()


# TODO
# need methods to find corresponding segments
# need methods to find splits

# compare segmentations without having the same underlying oversegmentation
def segmentation_ensemble(segA, segB):
    #ragA = vigra.graphs.regionAdjacencyGraph(vigra.gridGr)
