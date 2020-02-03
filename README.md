# roughmesh
Generate surface roughness in finite element meshes.

## Requirements

You need Python and the mesh genertator [Gmsh](https://gmsh.info).

## Getting started

To get started follow the example to generate a rough sphere.
First, open [`example/sphere.geo`](./example/sphere.geo)  with Gmsh,
generate a two-dimensional mesh and save it in the `ply2` format
either via the graphical user interface or via the terminal
```
gmsh sphere.geo -2 -format ply2
```
Next, run [`example.py`](./example.py) by entering `python3 example.py`
in the terminal or `%run example.py` in the IPython shell.
It creates a mesh file of a rough sphere with a name of the format
`sphere_corlNUMBER_rmsrNUMBER_NUMBER.ply2`, where the numbers denote the
correlation length (corl), the root mean squared roughness (rmsr) and the
sample index.
You can change the corl and the rmsr to a different value or
an array of values.
Furthermore you can change the number of samples n.
Then, for each combination of corl and rmsr you get n meshes.
For a spherical mesh, which is centered at the origin, you can optionally pass
the radius. As a consequence, the distance between the vertices is computed as
the orthodromic distance instead of the Euclidean distance.
A mesh of a rough surface can be loaded back into gmsh and used to generate
a three-dimensional mesh.

## Author

Fabian Loth
e-mail: loth@physik.hu-berlin.de
