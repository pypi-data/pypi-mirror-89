##############################################################################
# Imports
##############################################################################

import numpy as np

cimport cython
cimport numpy as np

##############################################################################
# External Declarations
##############################################################################

cdef extern from "matfit.c":
    int matfitw(const long n_atoms, const float *xa, const float *xb,
                float *r, float *v, float *rmse,
                const int dofit, const float *w)

cdef extern from "fitutil.c":
    int fit_frame(const long n_atoms, const float *in_frame,
                  const float *r, const float *v, float *out_frame)

    int fast_pib(const long n_atoms, const float *in_coords,
                 const float *box, float *out_coords)

##############################################################################
# Public Functions
##############################################################################

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef fitted_traj(traj, ref, w=None):
    """
    Fast fitting function. Fits every snapshot in traj
    to structure ref and returns the transformed coordinates

    An optional array of weights may be provided.
    """

    cdef int dofit
    cdef long f
    cdef long n_frames = traj.shape[0]
    cdef long n_atoms = traj.shape[1]

    cdef float rms = 0.0
    cdef float[:] wloc
    cdef float[:] v
    cdef float[:, :] r
    cdef float[:, :] in_frame
    cdef float[:, :] ref_frame
    cdef float[:, :, :] out_traj

    dofit = 1

    if w is None:
        wloc = np.asarray(np.ones([n_atoms]), order='C', dtype=np.float32)
    else:
        wloc = np.asarray(w[:, 0], order='C', dtype=np.float32)

    ref_frame = np.asarray(ref, order='C', dtype=np.float32)

    v = np.asarray(np.zeros([3]), order='C', dtype=np.float32)
    r = np.asarray(np.zeros([3, 3]), order='C', dtype=np.float32)
    out_traj = np.asarray(np.zeros([n_frames, n_atoms, 3]), order='C', dtype=np.float32)

    for f in range(n_frames):
        in_frame = np.asarray(traj[f, :, :], order='C', dtype=np.float32)

        matfitw(n_atoms, &ref_frame[0,0], &in_frame[0,0], &r[0,0], &v[0], &rms, dofit, &wloc[0])
        fit_frame(n_atoms, &in_frame[0,0], &r[0,0], &v[0], &out_traj[f, 0, 0])

    return np.array(out_traj, dtype=np.float32)

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef fitted(in_, ref, w=None):
    """
    Fits in_ to structure ref and returns the
    the resulting coordinates

    An optional array of weights may be provided
    """

    cdef int dofit
    cdef long n_atoms = in_.shape[0]

    cdef float rms = 0.0
    cdef float[:] wloc
    cdef float[:] v
    cdef float[:, :] r
    cdef float[:, :] in_frame
    cdef float[:, :] ref_frame
    cdef float[:, :] out_frame

    dofit = 1

    if w is None:
        wloc = np.asarray(np.ones([n_atoms]), order='C', dtype=np.float32)
    else:
        wloc = np.asarray(w[:, 0], order='C', dtype=np.float32)

    in_frame = np.asarray(in_, order='C', dtype=np.float32)
    ref_frame = np.asarray(ref, order='C', dtype=np.float32)

    v = np.asarray(np.zeros([3]), order='C', dtype=np.float32)
    r = np.asarray(np.zeros([3, 3]), order='C', dtype=np.float32)
    out_frame = np.asarray(np.zeros([n_atoms, 3]), order='C', dtype=np.float32)

    matfitw(n_atoms, &ref_frame[0,0], &in_frame[0,0], &r[0,0], &v[0], &rms, dofit, &wloc[0])
    fit_frame(n_atoms, &in_frame[0,0], &r[0,0], &v[0], &out_frame[0,0])

    return np.array(out_frame, dtype=np.float32)



@cython.boundscheck(False)
@cython.wraparound(False)
cpdef rv(in_, ref, w=None):
    """
    Fits in_ to structure ref and returns the
    the rotation matrix and shift vector.

    An optional array of weights may be provided
    """

    cdef int dofit
    cdef long n_atoms = in_.shape[0]

    cdef float rms = 0.0
    cdef float[:] wloc
    cdef float[:] v
    cdef float[:, :] r
    cdef float[:, :] in_frame
    cdef float[:, :] ref_frame

    dofit = 1

    if w is None:
        wloc = np.asarray(np.ones([n_atoms]), order='C', dtype=np.float32)
    else:
        wloc = np.asarray(w[:, 0], order='C', dtype=np.float32)

    in_frame = np.asarray(in_, order='C', dtype=np.float32)
    ref_frame = np.asarray(ref, order='C', dtype=np.float32)

    v = np.asarray(np.zeros([3]), order='C', dtype=np.float32)
    r = np.asarray(np.zeros([3, 3]), order='C', dtype=np.float32)

    matfitw(n_atoms, &ref_frame[0,0], &in_frame[0,0], &r[0,0], &v[0], &rms, dofit, &wloc[0])

    return np.array(r.T, dtype=np.float32), np.array(v.T, dtype=np.float32)



@cython.boundscheck(False)
@cython.wraparound(False)
cpdef rmsd_traj(traj, ref, w=None):
    """
    Fits every snapshot in traj to structure ref and returns the
    the rmsd.

    An optional array of weights may be provided
    """

    cdef int dofit
    cdef long f
    cdef long n_frames = traj.shape[0]
    cdef long n_atoms = traj.shape[1]

    cdef float rms = 0.0
    cdef float[:] wloc
    cdef float[:] v
    cdef float[:] out_rms
    cdef float[:, :] r
    cdef float[:, :] in_frame
    cdef float[:, :] ref_frame

    dofit = 0

    if w is None:
        wloc = np.asarray(np.ones([n_atoms]), order='C', dtype=np.float32)
    else:
        wloc = np.asarray(w[:, 0], order='C', dtype=np.float32)

    ref_frame = np.asarray(ref, order='C', dtype=np.float32)

    v = np.asarray(np.zeros([3]), order='C', dtype=np.float32)
    r = np.asarray(np.zeros([3, 3]), order='C', dtype=np.float32)
    out_rms = np.asarray(np.zeros([n_frames]), order='C', dtype=np.float32)

    for f in range(n_frames):
        in_frame = np.asarray(traj[f, :, :], order='C', dtype=np.float32)

        matfitw(n_atoms, &ref_frame[0,0], &in_frame[0,0], &r[0,0], &v[0], &rms, dofit, &wloc[0])
        out_rms[f] = rms

    return np.array(out_rms, dtype=np.float32)



@cython.boundscheck(False)
@cython.wraparound(False)
cpdef rmsd(in_, ref, w=None):
    """
    Calculates the (optionally mass-weighted) rmsd between in_ and ref

    An optional array of weights may be provided
    """

    cdef int dofit
    cdef long n_atoms = in_.shape[0]

    cdef float rms = 0.0
    cdef float[:] wloc
    cdef float[:] v
    cdef float[:, :] r
    cdef float[:, :] in_frame
    cdef float[:, :] ref_frame

    dofit = 0

    if w is None:
        wloc = np.asarray(np.ones([n_atoms]), order='C', dtype=np.float32)
    else:
        wloc = np.asarray(w[:, 0], order='C', dtype=np.float32)

    ref_frame = np.asarray(ref, order='C', dtype=np.float32)
    in_frame = np.asarray(in_, order='C', dtype=np.float32)

    v = np.asarray(np.zeros([3]), order='C', dtype=np.float32)
    r = np.asarray(np.zeros([3, 3]), order='C', dtype=np.float32)

    matfitw(n_atoms, &ref_frame[0,0], &in_frame[0,0], &r[0,0], &v[0], &rms, dofit, &wloc[0])

    return rms



@cython.boundscheck(False)
@cython.wraparound(False)
cpdef fitted_mean(traj, ref, w=None):
    """
    Fits every snapshot in traj to structure ref and returns the
    the mean coordinates

    An optional array of weights may be provided
    """

    cdef int dofit
    cdef long f
    cdef long n_frames = traj.shape[0]
    cdef long n_atoms = traj.shape[1]

    cdef float rms = 0.0
    cdef float[:] wloc
    cdef float[:] v
    cdef float[:, :] r
    cdef float[:, :] in_frame
    cdef float[:, :] ref_frame
    cdef float[:, :] out_frame

    dofit = 1

    if w is None:
        wloc = np.asarray(np.ones([n_atoms]), order='C', dtype=np.float32)
    else:
        wloc = np.asarray(w[:, 0], order='C', dtype=np.float32)

    ref_frame = np.asarray(ref, order='C', dtype=np.float32)

    v = np.asarray(np.zeros([3]), order='C', dtype=np.float32)
    r = np.asarray(np.zeros([3, 3]), order='C', dtype=np.float32)
    out_frame = np.asarray(np.zeros([n_atoms, 3]), order='C', dtype=np.float32)

    for f in range(n_frames):
        in_frame = np.asarray(traj[f, :, :], order='C', dtype=np.float32)

        matfitw(n_atoms, &ref_frame[0,0], &in_frame[0,0], &r[0,0], &v[0], &rms, dofit, &wloc[0])
        fit_frame(n_atoms, &in_frame[0,0], &r[0,0], &v[0], &out_frame[0,0])

    out_frame = np.divide(out_frame, n_frames)
    return np.array(out_frame, dtype=np.float32)



@cython.boundscheck(False)
@cython.wraparound(False)
cpdef pib(coords, box):
    """
    Fast version of "pack into box" in utils.py
    Wraps coordinates into the primary unit cell
    """

    cdef long f
    cdef long n_frames = coords.shape[0]
    cdef long n_atoms = coords.shape[1]

    cdef float[:, :] in_coords
    cdef float[:, :] in_box
    cdef float[:, :, :] out_coords

    out_coords = np.asarray(np.zeros([n_frames, n_atoms, 3]), order='C', dtype=np.float32)

    for f in range(n_frames):
        in_coords = np.asarray(coords[f, :, :], order='C', dtype=np.float32)
        in_box = np.asarray(box[f, :, :], order='C', dtype=np.float32)

        fast_pib(n_atoms, &in_coords[0,0], &in_box[0,0], &out_coords[f,0,0])

    return np.array(out_coords, dtype=np.float32)

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
def make_dx(float [:,:] x, float [:] dd, long [:, :] ij):
    """
    REFINE utility function: Calculate the coordinate shift vector DX.

    Arguments:
        x: [N,3] numpy array of current coordinates.
        dd: [K] numpy array of bond length gradients
        ij: [K, 2] numpy array indexing atom pairs for each bond in dd
    Returns:
        [N, 3] numpy array of shifts (will be further processed in calling
        python function)
    """
    
    cdef Py_ssize_t n = x.shape[0]
    cdef Py_ssize_t nk = ij.shape[0]
    cdef Py_ssize_t i, j, k, l
    
    DX = np.zeros((n, 3), dtype = np.float32)
    cdef float [:, :] DX_view = DX
    cdef float dx
    
    for k in range(nk):
        i = ij[k, 0]
        j = ij[k, 1]
        for l in range(3):
            dx = x[j, l] - x[i, l]
            dx = dx * dd[k]
            DX_view[j, l] += dx
            DX_view[i, l] -= dx
    return DX
