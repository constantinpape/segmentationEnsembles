import numpy as np
import vigra


def render_edges(rag, edges):

    vol = np.zeros(rag.shape, dtype = np.uint32)

    for edge in rag.edgeIter():
        coordinates = rag.edgeCoordinates(edge)
        vol[np.ceil(coordinates)] = edges[edge.id]
        vol[np.floor(coordinates)] = edges[edge.id]

    return vol




def compare_segs_same_overseg(segA, segB, overseg):
    # oversegmentation rag
    rag = vigra.graphs.regionAdjacencyGraph(vigra.graphs.gridGraph(overseg.shape[0:3]),
            overseg.astype(np.uint32))

    # project segmentations to overseg
    node_projA = rag.projectBaseGraphGt( segA.astype(np.uint32) )
    node_projB = rag.projectBaseGraphGt( segB.astype(np.uint32) )

    uv_ids = np.sort( rag.uvIds(), axis = 1 )

    edgesA = node_projA[ uv_ids[:,0] ] != node_projA[ uv_ids[:,1] ]
    edgesB = node_projB[ uv_ids[:,0] ] != node_projB[ uv_ids[:,1] ]

    diff_edges = edgesA != edgesB

    return diff_edges, rag


def compare_segs_diff_overseg():
    pass


if __name__ == '__main__':

    overseg_p = ""
    segA_p = ""
    segB_p = ""

    overseg = vigra.readHDF5(overseg_p, "data")

    segA = vigra.readHDF5(segA_p, "data")
    segB = vigra.readHDF5(segB_p, "data")

    edges, rag = compare_segs_same_overseg(segA, segB, overseg)

    save_p = ""
    vigra.writeHDF5( render_edges(rag, edges), save_p, "data", compression = 'gzip' )
