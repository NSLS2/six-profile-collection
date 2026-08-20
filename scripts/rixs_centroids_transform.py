"""Transform RIXSCAM XIP centroids into expected np.array format from Tiled.


E.g. for a Bluesky run:

<BlueskyRun v3.0 streams: {'baseline', 'primary'} scan_id=344687 uid='e467c580' 2026-07-28 11:11>
<BlueskyEventStream {'rixscam_image', 'rixscam_xip_count_event_3x3', 'rixscam_centroids_sum_regions', 'rixscam_xip_count_neighbours', 'rixscam_xip_count_possible_event', 'rixscam_centroids_x_eta', 'rixscam_centroids_y', 'rixscam_xip_count_event_2x2', 'rixscam_centroids_y_eta_iso', 'rixscam_centroids_y_eta', 'rixscam_centroids_x', 'rixscam_xip_count_below_threshold', 'rixscam_xip_count_above_threshold', 'rixscam_centroids_XIP_mode', 'time'} stream_name='primary'>
In [22]: run["primary"]["rixscam_centroids_y"]
Out[22]: <RaggedClient shape=(2, 3, None) size=15009 chunks=((2,), (3,), None) dtype=float64 dims=('time', 'dim_1', 'dim_2')>
In [23]: run["primary"]["rixscam_centroids_y"].read()
Out [23]:
ragged.array([
    [[0.1, 0.2, 0.3, 0.4, ..., 0.8, 0.9, 1.0, 1.1], ...],
    [[0.1, 0.2, 0.3, 0.4, ..., 0.8, 0.9, 1.0, 1.1], ...],
])
"""


def read_rixscam_centroids(tiled_client, uid, stream_name="primary"):
    import numpy

    legacy_columns = (
        "x",
        "y",
        "x_eta",
        "y_eta",
        "y_eta_iso",
        "sum_regions",
        "XIP mode",
    )
    legacy_dtype = numpy.dtype(
        [(name, "<f4") for name in legacy_columns] + [("frame", "<i2")]
    )
    # legacy_length = 4800
    legacy_length = 10000  # new length possible
    centroid_data_keys = tuple(
        (field, f"rixscam_centroids_{field.replace(' ', '_')}")
        for field in legacy_columns
    )

    run = tiled_client[uid]
    stream = run[stream_name]

    columns_data = []
    for legacy_field, data_key in centroid_data_keys:
        value = stream[data_key].read()
        nested = value.tolist() if hasattr(value, "tolist") else value
        columns_data.append((legacy_field, data_key, nested))

    first_column = columns_data[0][2]
    num_points = len(first_column)

    out = numpy.empty((num_points, legacy_length), dtype=legacy_dtype)
    out.fill(-1)

    for _, data_key, nested in columns_data[1:]:
        actual = len(nested)
        if actual != num_points:
            raise ValueError(
                f"Column {data_key!r} has {actual} points; expected {num_points}."
            )

    max_frame_index = numpy.iinfo(numpy.int16).max
    for point_index in range(num_points):
        first_frames = first_column[point_index]
        expected_frames = len(first_frames)

        for _, data_key, nested in columns_data[1:]:
            actual = len(nested[point_index])
            if actual != expected_frames:
                raise ValueError(
                    f"Column {data_key!r} has {actual} frames at point {point_index}; "
                    f"expected {expected_frames}."
                )

        start = 0
        for frame_index in range(expected_frames):
            first_centroids = first_frames[frame_index]
            expected_centroids = len(first_centroids)

            for legacy_field, data_key, nested in columns_data[1:]:
                actual = len(nested[point_index][frame_index])
                if actual != expected_centroids:
                    raise ValueError(
                        f"Column {data_key!r} has {actual} centroids at point "
                        f"{point_index} frame {frame_index}; expected "
                        f"{expected_centroids}."
                    )

            stop = start + expected_centroids
            if stop > legacy_length:
                raise ValueError(
                    f"Point {point_index} contains {stop} centroid rows, exceeding "
                    f"padding length {legacy_length}."
                )
            if expected_centroids and frame_index > max_frame_index:
                raise ValueError(
                    f"Point {point_index} has frame index {frame_index}, "
                    "exceeding int16 frame dtype."
                )

            out[legacy_columns[0]][point_index, start:stop] = first_centroids
            for legacy_field, _, nested in columns_data[1:]:
                out[legacy_field][point_index, start:stop] = nested[point_index][
                    frame_index
                ]
            out["frame"][point_index, start:stop] = frame_index
            start = stop

    return out
