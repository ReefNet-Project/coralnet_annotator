import PIL
import matplotlib.pyplot as plt
import numpy as np
from urllib.request import urlopen

def get_labels_from_points(points):
    labels = []
    for point in points:
        classifications = point['classifications']
        # get highest scoring classification 
        highest_scoring_classification = max(classifications, key=lambda c: c['score'])
        # append to highest_scoring_classification dictionary both row and column
        highest_scoring_classification['row'] = point['row']
        highest_scoring_classification['column'] = point['column']
        labels.append(highest_scoring_classification)

    return labels

# get label dictionary from csv file
def get_label_dict():
    label_dict = {}
    with open('labelset.csv') as f:
        for index, line  in enumerate(f):
            if index == 0:
                continue
            label = line.split(',')[1]
            # remove newline character
            label = label.strip()
            label_dict[label] = index - 1
    return label_dict

def main():
    label_dict = get_label_dict()
    # load classification_result.json file 
    classification_result_file = open("classification_result.json", "r")
    classification_result = classification_result_file.read()
    classification_result_file.close()
    classification_result = eval(classification_result)
    data = classification_result['data']
    for index, image in enumerate(data):
        attributes = image['attributes']
        url = attributes['url']
        points = attributes['points']
        labels = get_labels_from_points(points)
        #load the image frol url and plot labels on it 
        np_image = PIL.Image.open(urlopen(url))
        cmap = plt.get_cmap('nipy_spectral', 98)  # The second argument is the number of distinct colors
        # Convert labels to integers
        labels_mapped = [label_dict[label["label_code"]] for label in labels]  # Assume label_dict maps labels to integers
        # Extract the x and y coordinates of the points
        x_coords = [label['column'] for label in labels]
        y_coords = [label['row'] for label in labels]
        # Create a scatter plot with colored points
        plt.figure(figsize=(10, 10))
        plt.imshow(np_image)
        plt.scatter(x_coords, y_coords, c=labels_mapped, cmap=cmap, s=10)
        # Add a colorbar for reference
        plt.colorbar(ticks=range(80), label='Labels')
        plt.savefig(f"image_{index}.png")


if __name__ == "__main__":
    main()