import boto3
import math
from PIL import Image
import requests
import numpy as np
import io
from dotenv import load_dotenv
import os


load_dotenv()
BUCKET_NAME = os.getenv('BUCKET_NAME') 

def get_s3_image_download_links():
    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(BUCKET_NAME)
    download_links = []

    # List all objects in the bucket
    objects = bucket.objects.all()

    for index, obj in enumerate(objects):
        # Generate pre-signed URL without an expiration time
        download_link = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': obj.key}
        )
        download_links.append(download_link)
        if index > 1:
            break
    print(f"[INFO]: Getting S3 image download links, total images: {len(download_links)}")
    return download_links

def create_grid_points(width, height, num_points):
    # Calculate the number of points in the x and y directions
    points_x = round(math.sqrt(num_points * width / height))
    points_y = round(num_points / points_x)

    # Adjust the number of points in each direction if the total exceeds the limit
    while points_x * points_y > num_points:
        if points_x > points_y:
            points_x -= 1
        else:
            points_y -= 1

    # Calculate the 5% margin for width and height
    margin_width = width * 0.05
    margin_height = height * 0.05

    # Adjust the width and height to exclude margins
    width -= 2 * margin_width
    height -= 2 * margin_height

    # Calculate the spacing between points in the x and y directions
    spacing_x = width / (points_x - 1) if points_x > 1 else width
    spacing_y = height / (points_y - 1) if points_y > 1 else height

    # Generate the grid points
    points = []
    for i in range(points_x):
        for j in range(points_y):
            points.append({
                "row": round(margin_height + j * spacing_y),  # Y-coordinate corresponds to row
                "column": round(margin_width + i * spacing_x)  # X-coordinate corresponds to column
            })

    return points



# Prepare image data
def prepare_image_data():
    print("[INFO]: Preparing image data")
    image_urls = get_s3_image_download_links()
    # Create the data object
    data = {
        "data": []
    }

    for index ,url in enumerate(image_urls):
        # Download the image data
        image_data = requests.get(url).content

        # Open the image with Pillow
        image = Image.open(io.BytesIO(image_data))

        # Get the image dimensions
        width, height = image.size
        print(f" width: {width} height: {height} \n")
        # Create grid points
        points = create_grid_points(width, height, 200)
        print(len(points))
        # Append image data
        data["data"].append({
            "type": "image",
            "attributes": {
                "url": url,
                "points": points
            }
        })
        if index > 1: 
            break
        
    print(f"[INFO]: Done Preparing image data: {len(data['data'])} images")
    return data

