import numpy as np
import vigra


def compare_segs_same_overseg():

    # oversegmentation rag
    rag = vigra.graphs.regionAdjacencyGraph(vigra.graphs.gridGraph(overseg.shape[0:3]),
            overseg.astype(np.uint32))

    # project segmentations to overseg
    node_projA, _ = rag.projectBaseGraphGt( segA.astype(np.uint32) )
    node_projB, _ = rag.projectBaseGraphGt( segB.astype(np.uint32) )

    uv_ids = rag.uvIds()

    edgesA = node_projA[ uv_ids[:,0] ] != node_projA[ uv_ids[:,1] ]
    edgesB = node_projB[ uv_ids[:,0] ] != node_projB[ uv_ids[:,1] ]

    diff_edges = edgesA != edgesB

    print "Number of different edges:", np.sum(diff_edges)

    return diff_edges, rag


def render_edges(rag, edges):

    vol = np.zeros(rag.shape, dtype = np.uint32)

    for edge in rag.edgeIter():

        if edges[edge.id]:
            coordinates = rag.edgeCoordinates(edge)

            coords_up = np.ceil( coordinates ).astype(np.uint32)
            coords_up = tuple( [ coords_up[:,i] for i in (0,1,2) ] )

            coords_dn = np.floor( coordinates ).astype(np.uint32)
            coords_dn = tuple( [ coords_dn[:,i] for i in (0,1,2) ] )

            vol[coords_up] = 1
            vol[coords_dn] = 1

    return vol


def compare_segs_same_overseg(segA, segB, overseg):
    # oversegmentation rag
    rag = vigra.graphs.regionAdjacencyGraph(vigra.graphs.gridGraph(overseg.shape[0:3]),
            overseg.astype(np.uint32))

    # project segmentations to overseg
    node_projA, _ = rag.projectBaseGraphGt( segA.astype(np.uint32) )
    node_projB, _ = rag.projectBaseGraphGt( segB.astype(np.uint32) )

    uv_ids = rag.uvIds()

    edgesA = node_projA[ uv_ids[:,0] ] != node_projA[ uv_ids[:,1] ]
    edgesB = node_projB[ uv_ids[:,0] ] != node_projB[ uv_ids[:,1] ]

    diff_edges = edgesA != edgesB

    return diff_edges, rag


def compare_segs_diff_overseg():
    pass


if __name__ == '__main__':

    for sample in ("A", "B", "C"):

        print sample

        overseg_p = "/home/constantin/Work/neurodata_hdd/cremi/sample_%s/train_block/ws/cremi_sample%s_wsdt_cantorV1.h5" % (sample, sample)

        segA_p_1 = "/home/constantin/Work/home_hdd/results/cremi/validation_it5/sample_A_train_id_0_traintest_0.h5"
        segA_p_2 = "/home/constantin/Work/home_hdd/results/cremi/validation_it5/sample_A_train_id_0_traintest_1.h5"

        segB_p_1 = "/home/constantin/Work/home_hdd/results/cremi/validation_it6/sample_%s_train_id_0_traintest_0.h5" % (sample)
        segB_p_2 = "/home/constantin/Work/home_hdd/results/cremi/validation_it6/sample_%s_train_id_0_traintest_1.h5" % (sample)

        overseg = vigra.readHDF5(overseg_p, "data").astype(np.uint32)

        segA = np.concatenate( [vigra.readHDF5(segA_p_2, "data"), vigra.readHDF5(segA_p_1, "data")], axis = 2)
        segB = np.concatenate( [vigra.readHDF5(segB_p_2, "data"), vigra.readHDF5(segB_p_1, "data")], axis = 2)

        edges, rag = compare_segs_same_overseg(segA, segB, overseg)

        print "edge vol computed - going to render"

        import os

        save_folder = "/home/constantin/Work/home_hdd/results/cremi/cantorV1_mcvslmc"
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        save_p = os.path.join(save_folder,"mcvslmc_edges_%s.h5"%(sample))
        edge_vol = render_edges(rag, edges)

        vigra.writeHDF5( edge_vol , save_p, "data", compression = 'gzip' )
