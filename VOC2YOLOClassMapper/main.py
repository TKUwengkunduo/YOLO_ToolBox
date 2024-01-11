import os
import xml.etree.ElementTree as ET

# Function to read class mappings from a file, allowing multiple classes to map to the same ID
def read_class_mappings(file_path):
    class_mappings = {}
    with open(file_path, 'r') as file:
        for line in file:
            print(f"Reading line from class mappings: {line.strip()}")  # Debug print
            parts = line.strip().split(',')
            if len(parts) == 2:
                class_name, class_id = parts
                class_mappings[class_name] = int(class_id)
    print(f"Final class mappings: {class_mappings}")  # Debug print
    return class_mappings


# Function to convert coordinates from PascalVOC format to YOLO format
def convert_coordinates(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

# Function to convert a single PascalVOC XML file to a YOLO text file
def convert_annotation(xml_file, class_mappings):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    yolo_data = []
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls in class_mappings:
            cls_id = class_mappings[cls]
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert_coordinates((w, h), b)
            yolo_data.append(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    # Save the YOLO annotation to a .txt file if there is at least one object
    if yolo_data:
        txt_file = os.path.splitext(xml_file)[0] + '.txt'
        with open(txt_file, 'w') as file:
            file.writelines(yolo_data)

# Replace with the path to your class mapping file
class_mappings_file = './VOC2YOLOClassMapper/classes.txt'

# Replace with the path to your directory containing PascalVOC annotation files
annotations_directory = '../yolov7/Dataset/Plate_Recognition/images/'

# Read the class mappings
class_mappings = read_class_mappings(class_mappings_file)
print("Class Mappings:", class_mappings)  # Debug statement

# Convert all PascalVOC annotation files in the directory
for file in os.listdir(annotations_directory):
    if file.endswith('.xml'):
        print(f"Processing file: {file}")  # Debug statement
        convert_annotation(os.path.join(annotations_directory, file), class_mappings)
        print(f"Finished processing file: {file}")  # Debug statement