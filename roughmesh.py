"""Generate unstructured mesh of general two-dimensional rough surface
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform
import os
import logging

import mesh
import linalg


def roughmesh(fname, corl, rmsr, num, radius = 0):
    """Rough surface generator.
    
    Takes a triangle mesh of the nominal surface and generates `num`
    triangle meshes of the corresponding rough surface
    with given correlation length `corl` and root mean squared roughness `rmsr`.
    
    Args:
        fname (str): File name of the mesh.
        corl (float or ndarray): Correlation length.
        rmsr (float or ndarray): Root mean squared roughness.
        num (int): Number of samples.
        radius (float, optional): radius of a spherical mesh,
            which is centred around the origin. Note, that this is not checked.
            If radius > 0, then the orthodromic distance is computed and
            the normal vectors at the vertices are computed as
            the normalized postiton vectors of the vertices.
    """
    
    # File stem and extension
    stem, ext = os.path.splitext(os.path.basename(fname))
    
    # Transformation of scalar corl and rmsr into array
    corl = np.atleast_1d(corl)
    rmsr = np.atleast_1d(rmsr)
    
    vertex, face = mesh.read_mesh(fname)
    
    if radius > 0:
        logging.info('Compute orthodromic distance matrix '
            + 'for spherical mesh with radius {}'.format(radius))
        distmat = (squareform(pdist(vertex,
            lambda u, v: np.arccos(np.vdot(u,v)/(radius**2))*radius)))
        logging.info('Compute vertex normal vectors')
        normal = vertex / radius

    else:
        logging.info('Compute Eulidean distance matrix')
        distmat = squareform(pdist(vertex))
        logging.info('Compute vertex normal vectors')
        normal = mesh.get_normal(vertex, face)[0]

    
    for i in range(corl.shape[0]):
        
        logging.info('Compute correlation matrix for correlation length: '
            + '{}'.format(corl[i]))
        cormat = np.exp(-0.5*(distmat/corl[i])**2)

        if radius > 0:
            logging.info('Minimum of correlation matrix: '
                + '{}'.format(np.amin(cormat)))

        corfac = linalg.chol_eigh(cormat)
            
        for j in range(rmsr.shape[0]):
            for k in range(num):
                
                gaussian_white_noise = np.random.randn(vertex.shape[0])
                
                height = rmsr[j] * (corfac @ gaussian_white_noise)
                
                vertex_rough = vertex + (height * normal.T).T
                
                # description string
                descr = '_corl{}_rmsr{}_{}'.format(corl[i], rmsr[j], k)
                
                # output filename
                fname_rough = stem + descr + ext
                
                full_fname_rough = os.path.join(os.path.dirname(fname),
                                                fname_rough)
                
                mesh.write_mesh(full_fname_rough, vertex_rough, face)



