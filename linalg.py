import numpy as np
import logging

def chol_eigh(A):
    """Modified Cholesky decomposition.

    Try to compute Cholesky decomposition of matrix A.
    If it fails, then compute eigendecomposition,
    set negative eigenvalues to zero and return
    eigenvectors * sqrt(eigenvalues).

    Args:
    A (ndarray): symmetric nxn-matrix
    
    Returns:
    L (ndarray): nxn-matrix such that A = L L*, where * denotes the transpose
    """
    try:
        logging.info('Compute Cholesky decomposition')
        L = np.linalg.cholesky(A)
    except np.linalg.LinAlgError as e:
        logging.info(e)
        logging.info('Compute eigendecomposition')
        eigenvalues, eigenvectors = np.linalg.eigh(A)

        logging.info('Number of negative eigenvalues: {}'.format(
            eigenvalues[eigenvalues < 0.0].shape[0]))
        logging.info('Smallest eigenvalue: {}'.format(np.amin(eigenvalues)))

        eigenvalues[eigenvalues < 0.0] = 0.0
        L = eigenvectors @ np.diag(np.sqrt(eigenvalues))
    
    return L

