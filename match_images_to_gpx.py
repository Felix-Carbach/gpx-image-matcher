# Expected folder structure:
# - data/images/ (input JPGs)
# - data/tracks/ (input .gpx)
# - output/      (output CSV will be created here)
# - match_images_to_gpx.py

import os
import exifread
import gpxpy
from datetime import datetime
import pandas as pd
from pathlib import Path


# Image and GPX Handling

def get_image_times(directory):
    """
    Reads all .jpg images in the given directory and extracts the EXIF DateTimeOriginal timestamp.
    """
    image_times = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(".jpg"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'rb') as f:
                tags = exifread.process_file(f, stop_tag="EXIF DateTimeOriginal", details=False)
                if "EXIF DateTimeOriginal" in tags:
                    time_str = str(tags["EXIF DateTimeOriginal"])
                    try:
                        time_obj = datetime.strptime(time_str, "%Y:%m:%d %H:%M:%S")
                        image_times.append((filename, time_obj))
                    except ValueError:
                        print(f"[ERROR] Invalid timestamp in image '{filename}': {time_str}")
    return image_times


def get_trackpoints(gpx_path):
    """
    Extracts all trackpoints and waypoints from the GPX file (datetime, elevation, lat, lon).
    """
    trackpoints = []
    try:
        with open(gpx_path, 'r', encoding='utf-8') as gpx_file:
            gpx = gpxpy.parse(gpx_file)

        # Trackpoints
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    if point.time:
                        trackpoints.append((point.time.replace(tzinfo=None), point.latitude, point.longitude))

        # Waypoints
        for waypoint in gpx.waypoints:
            if waypoint.time:
                trackpoints.append((waypoint.time.replace(tzinfo=None), waypoint.latitude, waypoint.longitude))

    except Exception as e:
        print(f"[ERROR] Failed to read GPX file: {e}")

    return sorted(trackpoints)


# Matching


def match_images_to_trackpoints(image_times, trackpoints, max_time_diff_sec=300):
    """
    Matches each image timestamp to the temporally closest trackpoint within a given threshold (default: 300 seconds).
    """
    matched = []
    unmatched = []

    if not trackpoints:
        print("[WARNING] No trackpoints found. Matching skipped.")
        return matched

    for filename, img_time in image_times:
        closest_point = None
        min_diff = float("inf")

        for tp_time, lat, lon in trackpoints:
            time_diff = abs((tp_time - img_time).total_seconds())
            if time_diff < min_diff:
                min_diff = time_diff
                closest_point = (tp_time, lat, lon)

        if closest_point and min_diff <= max_time_diff_sec:
            matched.append({
                "image": filename,
                "image_time": img_time,
                "matched_trackpoint_time": closest_point[0],
                "lat": closest_point[1],
                "lon": closest_point[2],
                "time_diff_sec": round(min_diff)
            })
        else:
            unmatched.append(filename)
            print(f"[IGNORED] '{filename}' (time difference {round(min_diff)}s > {max_time_diff_sec}s)")

    print(f"\nMatched images: {len(matched)}")
    print(f"Ignored images: {len(unmatched)}\n")
    return matched



# Main Routine


def main():
    images_path = Path("data/images/20250201")
    gpx_file_path = Path("data/tracks/Track 2025-01-FEB.gpx")
    output_path = Path("output/matched_images_01-FEB.csv")

    image_times = get_image_times(images_path)
    print(f"Images found with EXIF timestamps: {len(image_times)}")

    trackpoints = get_trackpoints(gpx_file_path)
    print(f"Trackpoints loaded (trkpt + wpt): {len(trackpoints)}")

    matched = match_images_to_trackpoints(image_times, trackpoints)

    df = pd.DataFrame(matched)
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Matching result saved to: {output_path.resolve()}")


if __name__ == "__main__":
    main()


