import numpy as np
from open3d import *
from open3d.cpu.pybind.io import read_point_cloud
from open3d.cpu.pybind.visualization import draw_geometries


def main():
    cloud = read_point_cloud("test.ply")  # Read the point cloud
    draw_geometries([cloud])

if __name__ == "__main__":
    main()