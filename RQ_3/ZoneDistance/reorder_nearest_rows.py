from annoy import AnnoyIndex


def reorder_nearest_rows(df, n_trees=10):
    """
    Reorder rows based on proximity of locations
    :param df: pd.DataFrame: Input DataFrame with columns for pickup_x, pickup_y, dropoff_x, dropoff_y
    :param n_trees: int: default=10: number of trees for building Annoy index
    :return: pd.DataFrame: Reordered DataFrame
    """

    # Calculate the center points
    df['center_x'] = (df["pickup_x"] + df["dropoff_x"]) / 2
    df['center_y'] = (df["pickup_y"] + df["dropoff_y"]) / 2
    vectors = df[['center_x', 'center_y']].values

    # Annoy index
    f = 2  # Dimension of the vectors (center_x, center_y)
    t = AnnoyIndex(f, 'euclidean')
    for i, vector in enumerate(vectors):
        t.add_item(i, vector)
    t.build(n_trees)

    # Reorder Dataframe
    ordered_rows = []
    for i in range(len(df)):
        nearest_neighbors = t.get_nns_by_item(i, len(df) - 1)  # rows closest to row i
        ordered_rows.append(nearest_neighbors)
    ordered_indices = sorted(set([idx for sublist in ordered_rows for idx in sublist]))
    ordered_df = df.iloc[ordered_indices].reset_index(drop=True)

    return ordered_df
