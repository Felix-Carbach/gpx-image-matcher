# GPX Image Matcher
This Python script matches geotagged images (with EXIF timestamps) to GPS trackpoints and waypoints from a `.gpx` file.  
The result is a CSV file containing image names and their closest spatial match from the track by assigning each image to a trackpoint via their timestamps. It also includes the trackpoint's coordinates.

# Expected folder structure

project/

├── match_images_to_gpx.py
├── data/
│ ├── images/ # JPG files with EXIF timestamps
│ └── tracks/ # .gpx file containing trkpt or wpt entries
├── output/
│ └── matched_images.csv # Output CSV

# How to run
1. Install dependencies:
   pip install gpxpy exifread pandas
   
2. Run the script:
   python match_images_to_gpx.py

# Output
The script outputs a CSV with:
- image filename
- original EXIF timestamp
- matched trackpoint time
- latitude & longitude
- time difference in seconds

# Author
Felix Carbach – as part of an internship at the ZFL in Bonn
