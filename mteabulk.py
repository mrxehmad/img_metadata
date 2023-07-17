from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
import os

def extract_image_metadata(image_path):
    try:
        image = Image.open(image_path)

        metadata = {
            "File Name": os.path.basename(image_path),
            "Image Size": image.size,
            "Image Format": image.format,
            "Image Mode": image.mode,
        }

        # Get EXIF data
        exif_data = image._getexif()

        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name == 'GPSInfo':
                    gps_info = {}
                    for key in value:
                        sub_decoded_tag = GPSTAGS.get(key, key)
                        gps_info[sub_decoded_tag] = value[key]
                    metadata[tag_name] = gps_info
                else:
                    metadata[tag_name] = value

        # Calculate the dominant colors in the image
        colors = image.getcolors(image.size[0] * image.size[1])
        dominant_colors = [color for count, color in sorted(colors, reverse=True)][:5]
        metadata["Dominant Colors"] = dominant_colors

        return metadata

    except Exception as e:
        return str(e)

def format_coordinate_part(coordinate):
    deg, minute, sec = coordinate
    return deg + minute / 60.0 + sec / 3600.0

def format_coordinates(latitude, longitude):
    formatted_latitude = format_coordinate_part(latitude)
    formatted_longitude = format_coordinate_part(longitude)
    return formatted_latitude, formatted_longitude

def get_location_info(latitude, longitude):
    geolocator = Nominatim(user_agent="image-metadata-tool")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location:
        return location.address
    else:
        return None

def save_metadata_to_file(metadata, image_name):
    output_file_name = image_name.replace('.', '_') + ".txt"

    with open(output_file_name, "w", encoding="utf-8") as file:
        for key, value in metadata.items():
            if isinstance(value, dict):
                file.write(f"{key}:\n")
                for sub_key, sub_value in value.items():
                    file.write(f"  {sub_key}: {sub_value}\n")
                if "GPSLatitude" in value and "GPSLongitude" in value:
                    latitude, longitude = value["GPSLatitude"], value["GPSLongitude"]
                    if latitude and longitude:
                        formatted_latitude, formatted_longitude = format_coordinates(latitude, longitude)
                        location_info = get_location_info(formatted_latitude, formatted_longitude)
                        if location_info:
                            file.write(f"  Location: {location_info}\n")
                            file.write(f"  Google Maps URL: https://www.google.com/maps/search/{formatted_latitude},{formatted_longitude}\n")
                        else:
                            file.write(f"  Location: {formatted_latitude}, {formatted_longitude}\n")
                            file.write(f"  Google Maps URL: https://www.google.com/maps/search/{formatted_latitude},{formatted_longitude}\n")
                    else:
                        file.write("  Location: Not available\n")
                else:
                    file.write("  Location: Not available\n")
            else:
                file.write(f"{key}: {value}\n")
        
        # If GPSInfo tag is missing, mention that location data is not available
        if "GPSInfo" not in metadata:
            file.write("GPS Location Data: Not available\n")

if __name__ == "__main__":
    pic_folder = "pic"
    output_folder = "location"

    if not os.path.exists(pic_folder):
        print(f"Folder '{pic_folder}' not found.")
    else:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for filename in os.listdir(pic_folder):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                image_path = os.path.join(pic_folder, filename)
                metadata = extract_image_metadata(image_path)
                save_metadata_to_file(metadata, os.path.join(output_folder, filename))