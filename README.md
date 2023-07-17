# Image Metadata Extraction Script

This script is designed to extract metadata from image files, such as JPEG, PNG, GIF, and BMP formats. It reads the EXIF data of the image, including information like image size, format, mode, camera make and model, GPS coordinates (if available), and other relevant details. Additionally, it calculates and lists the dominant colors present in the image.

## Usage

1. Place the script in the same directory as the images you want to analyze.
2. Run the script, and it will prompt you to enter the name of the image file you want to analyze.
3. The script will display the extracted metadata on the console and also save it in a text file with the same name as the image file.

## Dependencies

- Python Imaging Library (PIL): Used for reading EXIF data and image processing.
- Geopy: Used to fetch location information based on GPS coordinates.

---

# Image Metadata Extraction for Multiple Images

This script is an extension of the previous one and automates the extraction process for multiple images. It reads all image files with common extensions (JPEG, PNG, GIF, BMP) from a folder called "pic" and extracts their metadata. If an image contains GPS location data, it generates location information and Google Maps links, saving the results in a folder called "location" with corresponding text files.

## Usage

1. Create a folder named "pic" and place all the images you want to analyze in it.
2. Ensure the script is in the same directory as the "pic" folder.
3. Run the script, and it will process all images in the "pic" folder.
4. The script will create a new folder called "location" and save the output files there.

## Dependencies

- Python Imaging Library (PIL): Used for reading EXIF data and image processing.
- Geopy: Used to fetch location information based on GPS coordinates.

**Note:** Before running the scripts, make sure to install the required dependencies. You can install them using the following commands:

```bash
pip install Pillow
pip install geopy
