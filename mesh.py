"""Collection of routines to process triangular meshes.
"""

import numpy as np
import os
import logging

def get_normal(vertex, face):
    """Return normal vectors.
    
    Return unit normal vector at each face of a triangle mesh.
    
    Args:
        vertex(ndarray): mx3-array with coordinates of m vertices.
        face(ndarray): nx3-array with vertex indices that form n triangles.
    
    Returns:
        face_normal(ndarray): nx3-array with face normal vectors.
    """
    face_normal = np.zeros((face.shape[0], 3))
    vertex_normal = np.zeros((vertex.shape[0], 3))
    
    for i in range(face.shape[0]):
        # Coordinates of corners of i-th face
        p = vertex[face[i,:],:]
        n = np.cross((p[1,:]-p[0,:]),(p[2,:]-p[0,:]))
        face_normal[i,:] = n / np.linalg.norm(n)
        vertex_normal[face[i,:],:] += face_normal[i,:]
    
    vertex_normal /= np.linalg.norm(vertex_normal, axis=1, keepdims=True)
    
    return(vertex_normal, face_normal)

def read_mesh(fname):
    """Read a triangle mesh file.
    
    Read a triangle mesh file and return the vertices and faces.
    Supported file formats: ply2.
    
    Args:
        fname(str): File name of the mesh.
    
    Returns:
        vertex(ndarray): mx3-array with coordinates of m vertices.
        face(ndarray): nx3-array with vertex indices that form n triangles.        
    """
    extension = os.path.splitext(os.path.basename(fname))[1]
    
    if(extension == '.ply2'):
        logging.info('Read mesh file "{}"'.format(fname))
        vertex, face = read_ply2(fname)
        logging.info('Number of vertices: {}'.format(vertex.shape[0]))
    else:
        raise ValueError('Could not read file "{}"'.format(fname))
        
    return vertex, face

def write_mesh(fname, vertex, face):
    """Write a triangle mesh file.
    
    Take vertices and faces and write it into mesh file.
    Supported file formats: ply2.
    
    Args:
        fname(str): File name of the mesh.
        vertex(ndarray): mx3-array with coordinates of m vertices.
        face(ndarray): nx3-array with vertex indices that form n triangles.
    """
    extension = os.path.splitext(os.path.basename(fname))[1]
    
    if(extension == '.ply2'):
        write_ply2(fname, vertex, face)
        logging.info('Write mesh file "{}"'.format(fname))
    
    else:
        raise ValueError('Could not write file "{}"', fname)
    

"""
Read and write 3D triangluar meshes in the ply2 file format.

The ply2 file format has the form:
number of vertices (int)
number of triangles (int)
set of vertex coordinates (double double double)
set of vertex indices that form the triangle (3 int int int)
"""

import numpy as np

def read_ply2(fname):
    """
    Read triangle mesh in the ply2 format.
    
    Args:
        fname(str): File name of the mesh.
    
    Returns:
        vertex(ndarray): mx3-array with coordinates of m vertices.
        face(ndarray): nx3-array with vertex indices that form n triangles.
    """

    with open(fname, 'r') as f:
        try:
            vertex_count = np.fromstring(f.readline(), dtype=int, sep=' ')[0]
            vertex = np.zeros((vertex_count,3), dtype=float)

            face_count = np.fromstring(f.readline(), dtype=int, sep=' ')[0]
            face = np.zeros((face_count,3), dtype=int)

            for i in range(vertex_count):
                vertex[i,:] = np.fromstring(f.readline(), dtype=float, sep=' ')

            for i in range(face_count):
                face[i,:] = np.fromstring(f.readline(),dtype=int,sep=' ')[1:]
        except ValueError as e:
            print(e)
            raise
            

    return vertex, face

def write_ply2(fname, vertex, face):
    """
    Write triangle mesh in the ply2 format.
    
    Args:
        fname(str): File name of the mesh.
        vertex(ndarray): mx3-array with coordinates of m vertices.
        face(ndarray): nx3-array with vertex indices that form n triangles.
    """
    with open(fname, 'w') as f:
        vertex_count = vertex.shape[0]
        face_count = face.shape[0]
        f.write('{}\n{}\n'.format(vertex_count, face_count))

        for i in range(vertex_count):
            f.write('{} {} {}\n'.format(vertex[i,0], vertex[i,1], vertex[i,2]))

        for i in range(face_count):
            f.write('3 {} {} {}\n'.format(face[i,0], face[i,1],face[i,2]))



def get_inradius(vertex, face):
    inradius = np.zeros(face.shape[0])

    for i in range(face.shape[0]):
       # Coordinates of corners of i-th face
        p = vertex[face[i,:],:]
        a = np.linalg.norm(p[0,:])
        b = np.linalg.norm(p[1,:])
        c = np.linalg.norm(p[2,:])
        s = (a + b + c) / 2
        inradius[i] = np.sqrt((s - a) * (s - b) * (s - c) / s)

    return inradius

