import numpy as np


def crop_and_backalign(data, sample):

    shape_old = (1250,1250,125)

    data_backalign = np.zeros(shape_old, dtype = data.dtype)

    if sample == "A":

        shift  = (-90,15)

        zslice = 80

    elif sample == "B":

        shift  = (-200,50)

        zslice = 16

    else:

        return data



    if shift[0] < 0 and shift[1] < 0:

        data_backalign[:,:,:zslice] = data[:shape_old[0],:shape_old[1],:zslice]

        data_backalign[:,:,zslice:] = data[abs(shift[0]):,:abs(shift[1]),zslice:]

    elif shift[0] < 0 and shift[1] > 0:

        data_backalign[:,:,:zslice] = data[:shape_old[0],shift[1]:,:zslice]

        data_backalign[:,:,zslice:] = data[abs(shift[0]):,:shape_old[1],zslice:]

    elif shift[0] > 0 and shift[1] < 0:

        data_backalign[:,:,:zslice] = data[shift[0]:,:shape_old[1],:zslice]

        data_backalign[:,:,zslice:] = data[:shape_old[0],abs(shift[1]):,zslice:]

    elif shift[0] > 0 and shift[1] > 0:

        data_backalign[:,:,:zslice] = data[shift[0]:,shift[1]:,:zslice]

        data_backalign[:,:,zslice:] = data[:shape_old[0],:shape_old[1],zslice:]

    else:

        raise RuntimeError("Unvalid Shift")

    return data_backalign
