from constants import X_PICKING_OFFSET, Y_PICKING_OFFSET


def cloud2robot(cloud_coords: list[float]) -> list[float]:
    cloud_coords[0] += X_PICKING_OFFSET
    cloud_coords[1] += Y_PICKING_OFFSET
    return cloud_coords
