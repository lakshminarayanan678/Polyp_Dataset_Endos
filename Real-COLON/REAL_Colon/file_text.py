import os
import xml.etree.ElementTree as ET
from pathlib import Path

# ====== CONFIG ======
input_dir = Path("/path/to/Annotations")  # Folder containing all subfolders with XMLs
output_dir = Path("/path/to/YOLO_labels")  # Where YOLO-format .txt files go
output_dir.mkdir(parents=True, exist_ok=True)

TARGET_CLASS = "lesion"  # Only convert these (polyp)
CLASS_ID = 0  # YOLO class ID for lesion

# ====== STATS COUNTERS ======
total_images = 0
polyp_images = 0
non_polyp_images = 0
multiple_polyps = 0
other_classes_found = set()

# ====== CONVERSION FUNC ======
def convert_to_yolo(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x_center = (box[0] + box[1]) / 2.0
    y_center = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return [x_center * dw, y_center * dh, w * dw, h * dh]

# ====== PROCESS FILES ======
for xml_file in input_dir.rglob("*.xml"):
    total_images += 1
    tree = ET.parse(xml_file)
    root = tree.getroot()

    size_tag = root.find("size")
    width = int(size_tag.find("width").text)
    height = int(size_tag.find("height").text)

    yolo_lines = []
    object_count = 0

    for obj in root.findall("object"):
        class_name = obj.find("name").text.strip().lower()
        if class_name != TARGET_CLASS:
            other_classes_found.add(class_name)
            continue

        bbox = obj.find("bndbox")
        xmin = int(bbox.find("xmin").text)
        xmax = int(bbox.find("xmax").text)
        ymin = int(bbox.find("ymin").text)
        ymax = int(bbox.find("ymax").text)

        # Skip if bbox is empty or invalid
        if xmax <= xmin or ymax <= ymin:
            continue

        yolo_box = convert_to_yolo((width, height), (xmin, xmax, ymin, ymax))
        yolo_line = f"{CLASS_ID} " + " ".join(f"{coord:.6f}" for coord in yolo_box)
        yolo_lines.append(yolo_line)
        object_count += 1

    # Always create the .txt file (even if empty)
    txt_filename = xml_file.stem + ".txt"
    txt_path = output_dir / txt_filename

    if object_count > 0:
        polyp_images += 1
        if object_count > 1:
            multiple_polyps += 1
        with open(txt_path, "w") as f:
            f.write("\n".join(yolo_lines))
    else:
        non_polyp_images += 1
        txt_path.touch()  # Create empty .txt file

# ====== STATS OUTPUT ======
print("\n==== CONVERSION SUMMARY ====")
print(f"Total XML files processed         : {total_images}")
print(f"Images with at least 1 polyp     : {polyp_images}")
print(f"Images with no polyp             : {non_polyp_images}")
print(f"Images with multiple polyps      : {multiple_polyps}")
if other_classes_found:
    print(f"\n⚠️  Unexpected class names found:")
    for cls in sorted(other_classes_found):
        print(f" - {cls}")
else:
    print("\n✅ No unexpected class names found.")