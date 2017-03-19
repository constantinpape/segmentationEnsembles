import numpy as np
import vigra

from compareSegmentations import render_edges


def compareBySimpleProjection(segA, oversegA, segB):#, oversegB):

    ragA = vigra.graphs.regionAdjacencyGraph( vigra.graphs.gridGraph(oversegA.shape), oversegA )
    #ragB = vigra.graphs.regionBdjacencyGraph( vigra.graphs.gridGraph(oversegB.shape), oversegB )

    resA, _ = ragA.projectBaseGraphGt( segA )
    resB, _ = ragA.projectBaseGraphGt( segB ) # projected !!

    uvIds = ragA.uvIds()

    edgesA = resA[uvIds[:,0]] != resA[uvIds[:,1]]
    edgesB = resB[uvIds[:,0]] != resB[uvIds[:,1]]

    diff_edges = edgesA != edgesB

    return diff_edges, ragA



if __name__ == '__main__':

    segA = vigra.readHDF5('/home/constantin/Work/home_hdd/results/cremi/competition_submissions/it1/', 'data')
    segB = vigra.readHDF5('/home/constantin/Work/multicut_pipeline/software/multicut_exp/rebuttal/snemi/round3/snemi_final_seglmc_myel_myelmerged.h5', 'data')

    oversegA = vigra.readHDF5('/home/constantin/Work/neurodata_hdd/snemi3d_data/watersheds/snemiTheUltimateMapWsdtSpecialTest_myel.h5', 'data')
    oversegB = vigra.readHDF5('/home/constantin/Work/neurodata_hdd/snemi3d_data/watersheds/snemiTheMapWsdtTestV2_myel.h5', 'data')

    print 'Calculating edge diffs'
    diff_edges, ragA = compareBySimpleProjection(segA, oversegA, segB)

    print 'Rendering edge diffs'
    edge_vol = render_edges(ragA, diff_edges)

    from volumina_viewer import volumina_n_layer
    raw = vigra.readHDF5('/home/constantin/Work/neurodata_hdd/snemi3d_data/raw/test-input.h5','data')
    volumina_n_layer([raw,oversegA,oversegB,segA,segB,edge_vol],['raw','overseg_LMC_new','overseg_LMC_best','seg_LMC_new','seg_LMC_best','edge_diff'])
