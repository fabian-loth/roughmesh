SetFactory("OpenCASCADE");

Mesh.Algorithm = 6; // Frontal-Delaunay for best mesh quality

// Set parameters
radius = 100;
characteristic_length = 3.0; // mesh element size

// Create sphere
sphere = newv;
Sphere(sphere) = {0, 0, 0, radius};
Physical Surface("Sphere") = {sphere};

// Specify mesh element sizes
PointsOfSphere[] = PointsOf{Volume{sphere};};
Characteristic Length{PointsOfSphere[]} = characteristic_length;
