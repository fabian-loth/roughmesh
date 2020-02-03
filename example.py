import numpy as np
import logging

from roughmesh import roughmesh

logging.basicConfig(level=logging.INFO)

fname = './example/sphere.ply2'
#corl = np.array([5.0, 7.5, 10.0, 12.5, 15.0])
corl = 10.0
rmsr = np.array([2.0, 4.0])
num = 1
radius = 50.0
roughmesh(fname, corl, rmsr, num, radius)



