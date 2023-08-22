import PIL
import matplotlib.pyplot as plt
import numpy as np
from urllib.request import urlopen

def get_labels_from_points(points):
    """
        get labels for each point based on the highest score.
    """
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

        np_image = PIL.Image.open(urlopen(url))
        labels_mapped = [label_dict[label["label_code"]] for label in labels]

        # Find the unique labels and corresponding color code
        unique_labels = list(set(labels_mapped))
        unique_labels_count = len(unique_labels)

        # Use the unique labels count for the color map
        cmap = plt.get_cmap('nipy_spectral', unique_labels_count)

        x_coords = [label['column'] for label in labels]
        y_coords = [label['row'] for label in labels]
        plt.figure(figsize=(10, 10))
        plt.imshow(np_image)
        scatter_plot = plt.scatter(x_coords, y_coords, c=labels_mapped, cmap=cmap, s=10)
        
        # Create a colorbar with custom tick labels
        offset = 0.5 / unique_labels_count  # Half the length of one color area
        cbar = plt.colorbar(scatter_plot, ticks=[label + offset for label in unique_labels])  # Add the offset to the tick positions
        cbar.ax.set_yticklabels([label for label, code in label_dict.items() if code in unique_labels])  # set the label names

        plt.savefig(f"image_{index}.png")


if __name__ == "__main__":
    main()