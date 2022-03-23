def cloud2robot(cloud_coords: list[float]) -> list[float]:
    cloud_coords[0] += 0.05
    cloud_coords[1] += 0.1
    return cloud_coords
