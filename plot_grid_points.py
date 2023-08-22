import matplotlib.pyplot as plt
import requests
from PIL import Image
from prepare_images import create_grid_points, get_s3_image_download_links
import io 
import numpy as np
import cv2

def plot_points_on_image(image, points, image_name):
    # Convert the image to a numpy array
    np_image = np.array(image)

    # Extract the x and y coordinates of the points
    x_coords = [point['column'] for point in points]
    y_coords = [point['row'] for point in points]

    # Create a plot
    plt.figure(figsize=(10, 10))
    plt.imshow(np_image)
    plt.scatter(x_coords, y_coords, color='red', s=10)
    output = f'./output/{image_name}'
    plt.savefig(output)
    plt.show()

# Test with an image URL and generated grid points
image_links = get_s3_image_download_links()


image_path = './Red Sea Global data/Imagery_Rhonda_RSG/SLPK22/20220523/06/DSC_8079.JPG'
image = cv2.imread(image_path)

# width, height = image.size
height, width, _ = image.shape
print(width, height)
points = create_grid_points(width, height, 200)
print(f"number of points {len(points)}")
plot_points_on_image(image, points, 'annotated_image')

# for i in range(len(image_links)):
#     image_url = image_links[i]
#     image_data = requests.get(image_url).content
#     image = Image.open(io.BytesIO(image_data))

#     # Check for orientation metadata and rotate the image if necessary
#     # if hasattr(image, "_getexif"):
#     #     orientation = image._getexif().get(0x0112, 1)  # 0x0112 is the EXIF tag for Orientation
#     #     print(orientation)
#     #     if orientation == 3:
#     #         image = image.rotate(180)
#     #     elif orientation == 6:
#     #         image = image.rotate(270)
#     #     elif orientation == 8:
#     #         image = image.rotate(90)

#     # print(image)
#     width, height = image.size
#     print(width, height)
#     points = create_grid_points(width, height, 200)
#     print(f"[{i}]: number of points {len(points)}")
#     plot_points_on_image(image, points, f'image_{i}')