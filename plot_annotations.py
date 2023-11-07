from PIL import Image, ImageDraw, ImageFont
import json
import numpy as np
from urllib.request import urlopen
import matplotlib
import openpyxl
matplotlib.use('Agg')  # Use the Agg backend
import matplotlib.pyplot as plt

# Set a font family that is available on your system
font = {'family': 'sans-serif', 'size': 10}
plt.rc('font', **font)



def get_color_based_on_score(score):
    if score >= 0.8:
        return (0, 255, 0)  # Green
    elif score >= 0.4:
        return (255, 0, 0)  # Red
    else:
        return (0, 0, 255)  # Blue

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
    
    # Save the updated classification_result into the file
    with open('label_dict.json', 'w') as f:
        json.dump({'data': label_dict}, f)

    return label_dict


def write_data_to_excel(data, filename="output.xlsx"):
    # Create a new Excel workbook and add a worksheet to it
    wb = openpyxl.Workbook()
    ws = wb.active

    headers = ['Name','Row','Column','Label Code(abbreviation)', 'Label Name', 'Label Number', 'Valid']

    ws.append(headers)

    # Loop through the array of dictionaries
    for entry in data:
        row = [entry[header] for header in headers]
        ws.append(row)

    # Save the workbook to a file
    wb.save(filename)


def main():
    label_dict = get_label_dict()
    # load classification_result.json file 
    classification_result_file = open("classification_result.json", "r")
    classification_result = classification_result_file.read()
    classification_result_file.close()
    classification_result = eval(classification_result)
    data = classification_result['data']
    xlsx_data = []
    for index, image in enumerate(data):
        image_name = (image['id'].split('?')[0]).split('/')[-1]
        attributes = image['attributes']
        url = attributes['url']
        points = attributes['points']
        labels = get_labels_from_points(points)
        print(labels[0])
        np_image = Image.open(urlopen(url))
        labels_mapped = [label_dict[label["label_code"]] for label in labels]
        labels_scores = [label["score"] for label in labels]
        x_coords = [label['column'] for label in labels]
        y_coords = [label['row'] for label in labels]
        draw = ImageDraw.Draw(np_image)
        # Font setup - Adjust the font path and size accordingly
        font = ImageFont.truetype("arial.ttf", 100)  # You might need to specify the full path to arial.ttf

        for i, (x, y) in enumerate(zip(x_coords, y_coords)):
            # save data into xls file 
            # image name, label code, row , column 
            label_name = labels[i]['label_name']
            label_code = labels[i]['label_code']
            label = labels_mapped[i]
            score = labels_scores[i]
            color = get_color_based_on_score(score)
            draw.text((x, y), str(label), font=font, fill=color)
            xlsx_data.append({'Name':image_name, 'Row': y, 'Column':x, 'Label Code(abbreviation)': label_code,  'Label Name': label_name,  'Label Number': str(label) ,'Valid': ''})
        # Save the labeled image
        np_image.save(f"output/{image_name}.jpg")

    write_data_to_excel(xlsx_data)

if __name__ == "__main__":
    main()