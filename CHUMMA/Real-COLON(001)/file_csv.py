import os
import csv
import xml.etree.ElementTree as ET
from pathlib import Path

# ====== CONFIG ======
input_dir = Path("/media/endodl/NewVolume/moved_unknown/mln/PAPER/data/Real-COLON/001-003_annotations")  # Directory with XML annotation files
output_csv = Path("/media/endodl/NewVolume/moved_unknown/mln/PAPER/data/Real-COLON/normalized.csv")
log_file = Path("/media/endodl/NewVolume/moved_unknown/mln/PAPER/data/Real-COLON/log.txt")  # Log output

TARGET_CLASS = "lesion"
CLASS_ID = 0  # Label number for 'lesion' (polyp)

# ====== STATS TRACKING ======
total_images = 0
polyp_images = 0
non_polyp_images = 0
multiple_polyps = 0
multiple_polyp_images_list = []
other_classes_found = set()

# ====== CSV HEADER ======
csv_rows = [["image_filename", "label", "cx", "cy", "bw", "bh"]]

# ====== CONVERSION FUNC ======
def convert_to_yolo(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x_center = (box[0] + box[1]) / 2.0
    y_center = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return [x_center * dw, y_center * dh, w * dw, h * dh]

# ====== PROCESSING ======
for xml_file in input_dir.rglob("*.xml"):
    total_images += 1
    tree = ET.parse(xml_file)
    root = tree.getroot()

    size_tag = root.find("size")
    width = int(size_tag.find("width").text)
    height = int(size_tag.find("height").text)
    image_filename = root.find("filename").text.strip()

    found_polyp = False
    polyp_count = 0

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

        if xmax <= xmin or ymax <= ymin:
            continue  # skip invalid boxes

        yolo_box = convert_to_yolo((width, height), (xmin, xmax, ymin, ymax))
        csv_rows.append([
            image_filename,
            str(CLASS_ID),
            f"{yolo_box[0]:.6f}",
            f"{yolo_box[1]:.6f}",
            f"{yolo_box[2]:.6f}",
            f"{yolo_box[3]:.6f}"
        ])
        found_polyp = True
        polyp_count += 1

    if found_polyp:
        polyp_images += 1
        if polyp_count > 1:
            multiple_polyps += 1
            multiple_polyp_images_list.append(image_filename)
    else:
        non_polyp_images += 1
        csv_rows.append([image_filename, "", "", "", "", ""])

# ====== WRITE CSV ======
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_rows)
print(f"✅ CSV saved at: {output_csv}")

# ====== WRITE LOG ======
log_lines = [
    "==== CONVERSION SUMMARY ====",
    f"Total XML files processed         : {total_images}",
    f"Images with at least 1 polyp     : {polyp_images}",
    f"Images with no polyp             : {non_polyp_images}",
    f"Images with multiple polyps      : {multiple_polyps}",
]

if other_classes_found:
    log_lines.append("\n⚠️  Unexpected class names found:")
    for cls in sorted(other_classes_found):
        log_lines.append(f" - {cls}")
else:
    log_lines.append("\n✅ No unexpected class names found.")

if multiple_polyp_images_list:
    log_lines.append("\n🖼️ Images with multiple polyps:")
    for img in multiple_polyp_images_list:
        log_lines.append(f" - {img}")
else:
    log_lines.append("\nℹ️ No images with multiple polyps.")

# Print and save log
log_content = "\n".join(log_lines)
print("\n" + log_content)

with open(log_file, "w") as f:
    f.write(log_content)

print(f"\n📄 Stats log saved at: {log_file}")