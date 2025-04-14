import geopandas as gpd
import pandas as pd
from math import sqrt


def get_distance_function(shape_file, zone_id):
    """
    Return a function that calculates the distance between two points given a shape file.
    :param shape_file: str: path to the shape file
    :param zone_id: str: geo dataframe attribute to use as zone ID
    :return: function(zone_id1, zone_id2) -> int: function that calculates the distance between two zone IDs
    """
    gdf = gpd.read_file(shape_file)

    # Initialize an empty list to store the distances
    distances = []

    # Iterate through each pair of geometries
    for idx1, zone1 in gdf.iterrows():
        for idx2, zone2 in gdf.iterrows():
            id1 = zone1[zone_id]
            id2 = zone2[zone_id]

            if id1 < id2:  # avoid redundant pairs
                geom1 = zone1.geometry
                geom2 = zone2.geometry

                # Calculate Euclidian distance using centroids
                dist = sqrt((geom1.centroid.x - geom2.centroid.x)**2 + abs(geom1.centroid.y - geom2.centroid.y)**2)
                distances.append((id1, id2, dist))

    # Convert to pivot DF
    distance_df = pd.DataFrame(distances, columns=["Zone1", "Zone2", "Distance"])
    distance_df = distance_df.drop_duplicates(subset=["Zone1", "Zone2"])
    pivot_df = distance_df.pivot(index="Zone1", columns="Zone2", values="Distance")

    def get_distance(z1, z2):
        if z1 == z2:
            return 0
        elif z1 < z2:
            return pivot_df[z2][z1]
        else:
            return pivot_df[z1][z2]

    return get_distance


def get_position_dict(shape_file, zone_id):
    """
    Return a function that calculates the position of a zone given a shape file.
    :param shape_file: str: path to the shape file
    :param zone_id: str: geo dataframe attribute to use as zone ID
    :return: positions: dict: positions dictionary that maps zone ID to its position
    """
    gdf = gpd.read_file(shape_file)

    # Initialize an empty dictionary to store the positions
    positions = {}

    # Iterate through each geometry
    for idx, zone in gdf.iterrows():
        zid = zone[zone_id]
        pos = zone.geometry.centroid.x, zone.geometry.centroid.y
        positions[zid] = pos

    return positions


d = get_position_dict("taxi-zones/taxi_zones.shp", "LocationID")
f = get_distance_function("taxi-zones/taxi_zones.shp", "LocationID")
