## GPX Image Matcher
This Python script matches geotagged images (with EXIF timestamps) to GPS trackpoints and waypoints from a `.gpx` file.  
The result is a CSV file containing image names and their closest spatial match from the track by assigning each image to a trackpoint via their timestamps. It also includes the trackpoint's coordinates.

## Expected folder structure

├── `01_data`/

│ ├── images/ = JPG files with EXIF timestamps

│ └── tracks/ = .gpx file containing trkpt or wpt entries

├── `02_output`/

│ └── matched_images.csv = Output CSV

├── `03_match_images_to_gpx.py`

## How to run
1. Install dependencies:
   
   `gpxpy`, `exifread` & `pandas`
   
3. Run the script:
   
   python match_images_to_gpx.py

## Output
The script outputs a CSV with:
- image filename
- original EXIF timestamp
- matched trackpoint time
- latitude & longitude
- time difference in seconds

