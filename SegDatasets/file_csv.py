import cv2
import numpy as np
import csv
from pathlib import Path

# --- CONFIG ---
dataset_name = "ETIS-LaribPolypDB"  # <--- Add your dataset name prefix here
masks_dir = Path("/home/endodl/PHASE-1/ETIS-LaribPolypDB/masks")           # Folder with binary masks
images_dir = Path("/home/endodl/PHASE-1/ETIS-LaribPolypDB/images")         # Folder with corresponding images
output_csv = Path("/home/endodl/PHASE-1/ETIS-LaribPolypDB/normalized.csv")     # CSV output file
log_output_path = Path("/home/endodl/PHASE-1/ETIS-LaribPolypDB/log.txt")  # Stats log file

# --- Prepare output ---
csv_data = [("image_filename", "label", "cx", "cy", "bw", "bh")]
total_images = 0
polyp_count = 0
multi_polyp_count = 0
non_polyp_count = 0
multiple_polyp_files = []  # Track which masks had multiple polyps

# --- Process each mask ---
for mask_path in sorted(masks_dir.glob("*")):
    orig_filename = mask_path.name
    image_path = images_dir / orig_filename
    if not image_path.exists():
        print(f"⚠️ Skipping {orig_filename} — image not found.")
        continue

    total_images += 1
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
    h, w = mask.shape
    _, binary_mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_mask, connectivity=8)

    polyp_boxes = []

    for label in range(1, num_labels):  # skip background
        x, y, bw, bh, area = stats[label]
        if area < 10:
            continue

        cx = (x + bw / 2) / w
        cy = (y + bh / 2) / h
        norm_w = bw / w
        norm_h = bh / h
        polyp_boxes.append((f"{cx:.6f}", f"{cy:.6f}", f"{norm_w:.6f}", f"{norm_h:.6f}"))

    filename_with_prefix = f"{dataset_name}_{orig_filename}"

    if polyp_boxes:
        polyp_count += 1
        if len(polyp_boxes) > 1:
            multi_polyp_count += 1
            multiple_polyp_files.append(filename_with_prefix)

        for bbox in polyp_boxes:
            csv_data.append((filename_with_prefix, "0", *bbox))
    else:
        non_polyp_count += 1
        csv_data.append((filename_with_prefix, "", "", "", "", ""))

# --- Save CSV ---
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)

# --- Save log file ---
with open(log_output_path, "w") as log_file:
    log_file.write(f"Dataset: {dataset_name}\n")
    log_file.write(f"🖼️ Total images: {total_images}\n")
    log_file.write(f"✅ Polyp images: {polyp_count}\n")
    log_file.write(f"✅ Multiple polyp images: {multi_polyp_count}\n")
    log_file.write(f"✅ Non-polyp images: {non_polyp_count}\n")
    log_file.write(f"📄 CSV saved to: {output_csv}\n")
    log_file.write(f"📌 Masks with multiple polyps:\n")
    for fname in multiple_polyp_files:
        log_file.write(f" - {fname}\n")

# --- Print to console ---
print(f"🖼️ Total images: {total_images}")
print(f"✅ Polyp images: {polyp_count}")
print(f"✅ Multiple polyp images: {multi_polyp_count}")
print
