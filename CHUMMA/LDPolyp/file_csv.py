import os
import csv
from pathlib import Path
from PIL import Image

# Set paths
base_dir = Path("/home/endodl/PHASE-1/LDPolypVideo/bef_annot_data") 
images_dir = base_dir / "images"
annotations_dir = base_dir / "annotations"
csv_output_path = base_dir / "ldpolyp_annotations_bbox_rows.csv"
log_output_path = base_dir / "ldpolyp_annotation_stats.txt"

# Stats counters
total_images = 0
polyp_count = 0
multi_polyp_count = 0
non_polyp_count = 0

# Prepare CSV data
csv_data = [("image_filename", "label", "cx", "cy", "bw", "bh")]

# Process each image
for img_file in sorted(images_dir.glob("*")):
    total_images += 1
    annot_file = annotations_dir / f"{img_file.stem}.txt"

    with Image.open(img_file) as img:
        w, h = img.size

    has_polyp = False
    bbox_written = 0

    if annot_file.exists():
        with open(annot_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        if len(lines) > 1:
            coords = lines[1:]  # skip box count line
            for box in coords:
                x1, y1, x2, y2 = map(int, box.split())
                cx = (x1 + x2) / 2 / w
                cy = (y1 + y2) / 2 / h
                bw = (x2 - x1) / w
                bh = (y2 - y1) / h

                csv_data.append((img_file.name, "0", f"{cx:.6f}", f"{cy:.6f}", f"{bw:.6f}", f"{bh:.6f}"))
                has_polyp = True
                bbox_written += 1

    if has_polyp:
        polyp_count += 1
        if bbox_written > 1:
            multi_polyp_count += 1
    else:
        csv_data.append((img_file.name, "", "", "", "", ""))
        non_polyp_count += 1

# Write to CSV
with open(csv_output_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)

# Save print logs to text file
with open(log_output_path, "w") as log_file:
    log_file.write(f"🖼️ Total images: {total_images}\n")
    log_file.write(f"✅ Polyp images: {polyp_count}\n")
    log_file.write(f"✅ Multiple polyp images: {multi_polyp_count}\n")
    log_file.write(f"✅ Non-polyp images: {non_polyp_count}\n")
    log_file.write(f"📄 CSV saved to: {csv_output_path}\n")

# Optionally also print to console
print(f"🖼️ Total images: {total_images}")
print(f"✅ Polyp images: {polyp_count}")
print(f"✅ Multiple polyp images: {multi_polyp_count}")
print(f"✅ Non-polyp images: {non_polyp_count}")
print(f"📄 CSV saved to: {csv_output_path}")
print(f"📝 Stats saved to: {log_output_path}")
