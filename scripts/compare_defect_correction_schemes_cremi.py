import os
import sys
import vigra
#from volumina_viewer import volumina_n_layer
from crop_and_realign_cremi import crop_and_backalign

sys.path.append('..')
from segmentation_ensembles import compare_segs_same_overseg, render_edges

def crop_and_realign_segmentation(sample, corrected_seg = False):
    if corrected_seg:
        seg_path = '/home/constantin/Work/neurodata_hdd/cremi/sample%s+/ws/sample%s+_wsdt_cantorV1_manually_corrected.h5' % (sample, sample)
    else:
        seg_path = '/home/constantin/Work/neurodata_hdd/cremi/sample%s+/ws/sample%s+_wsdt_cantorV1_manually_realigned.h5' % (sample, sample)
    seg = vigra.readHDF5(seg_path, 'data')

    if sample in ('A','B'):
        seg = crop_and_backalign(seg, sample)

    if not os.path.exists('../data'):
        os.mkdir('../data')
    save_path = '../data/sample%s_segmentation_realgined_%s.h5' % (sample, str(corrected_seg))
    vigra.writeHDF5(seg, save_path, 'data', compression = 'gzip')


def make_edgediff(sample, corrected_seg = False):
    seg_path = '../data/sample%s_segmentation_realgined_%s.h5' % (sample, str(corrected_seg))
    manual_corr_path = '/home/constantin/Work/home_hdd/results/cremi/competition_submissions/post-miccai/it1_train_all/sample_%s_test_lmcresult.h5' % sample
    auto_corr_path = '/home/constantin/Work/home_hdd/results/cremi/competition_submissions/post-miccai/it2_automatic_defect_correction/sample_%s+_lmc.h5' % sample

    seg = vigra.readHDF5(seg_path, 'data')
    manual_corr = vigra.readHDF5(manual_corr_path, 'volumes/labels/neuron_ids').transpose( (2,1,0) )
    auto_corr = vigra.readHDF5(auto_corr_path, 'volumes/labels/neuron_ids').transpose( (2,1,0) )

    edge_diff, rag = compare_segs_same_overseg(manual_corr, auto_corr, seg)
    assert edge_diff.shape[0] == rag.edgeNum

    print "Starting to render edges"
    print type(edge_diff)
    edge_vol = render_edges(rag, edge_diff)
    vigra.writeHDF5(edge_vol, '../data/edgediff_vol_sample%s_%s.h5' % (sample, str(corrected_seg)), 'data', compression = 'gzip')

def preprocessing():
    for sample in ('A','B','C'):
        for corrected in (False,True):
            #crop_and_realign_segmentation(sample, corrected)
            make_edgediff(sample, corrected)

if __name__ == '__main__':
    preprocessing()
