import os
import shutil
import csv
from pathlib import Path
from collections import defaultdict
from PIL import Image

# --- CONFIG ---
BASE_DIR = Path("/home/endodl/PHASE-1/LDPolypVideo/org_data")  # Original TrainValid path
IMAGES_SRC = BASE_DIR / "Images"
ANNOTS_SRC = BASE_DIR / "Annotations"

OUTPUT_DIR = Path("/home/endodl/PHASE-1/LDPolypVideo/bef_annot_data")
IMAGES_DST = OUTPUT_DIR / "images"
ANNOTS_DST = OUTPUT_DIR / "annotations"
CSV_OUTPUT_PATH = OUTPUT_DIR / "ldpolyp_annotations_bbox_rows.csv"
LOG_OUTPUT_PATH = OUTPUT_DIR / "ldpolyp_annotation_stats.txt"

# --- STEP 1: Flatten & Rename ---
IMAGES_DST.mkdir(parents=True, exist_ok=True)
ANNOTS_DST.mkdir(parents=True, exist_ok=True)

print("🔄 Flattening and renaming files...")

for folder_idx in range(1, 161):
    img_folder = IMAGES_SRC / str(folder_idx)
    annot_folder = ANNOTS_SRC / str(folder_idx)

    img_files = sorted(img_folder.glob("*"))
    annot_files = sorted(annot_folder.glob("*.txt"))

    for img_file, annot_file in zip(img_files, annot_files):
        img_name = img_file.stem
        ext = img_file.suffix
        new_name = f"ldpolyp_{folder_idx}_{img_name}"

        shutil.copy2(img_file, IMAGES_DST / f"{new_name}{ext}")
        shutil.copy2(annot_file, ANNOTS_DST / f"{new_name}.txt")

print("✅ All images and annotations flattened and renamed.")

# --- STEP 2: Generate YOLO CSV ---
print("🧮 Converting annotations to YOLO-format CSV...")

total_images = 0
polyp_count = 0
multi_polyp_count = 0
non_polyp_count = 0

csv_data = [("image_filename", "label", "cx", "cy", "bw", "bh")]

for img_file in sorted(IMAGES_DST.glob("*")):
    total_images += 1
    annot_file = ANNOTS_DST / f"{img_file.stem}.txt"

    with Image.open(img_file) as img:
        w, h = img.size

    has_polyp = False
    bbox_written = 0

    if annot_file.exists():
        with open(annot_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        if len(lines) > 1:
            coords = lines[1:]  # Skip any header
            for box in coords:
                try:
                    x1, y1, x2, y2 = map(int, box.split())
                    cx = (x1 + x2) / 2 / w
                    cy = (y1 + y2) / 2 / h
                    bw = (x2 - x1) / w
                    bh = (y2 - y1) / h

                    csv_data.append((img_file.name, "0", f"{cx:.6f}", f"{cy:.6f}", f"{bw:.6f}", f"{bh:.6f}"))
                    has_polyp = True
                    bbox_written += 1
                except ValueError:
                    print(f"⚠️ Malformed bbox line in {annot_file.name}: {box}")

    if has_polyp:
        polyp_count += 1
        if bbox_written > 1:
            multi_polyp_count += 1
    else:
        csv_data.append((img_file.name, "", "", "", "", ""))
        non_polyp_count += 1

# --- Write CSV ---
with open(CSV_OUTPUT_PATH, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)

# --- Write Stats Log ---
with open(LOG_OUTPUT_PATH, "w") as log_file:
    log_file.write(f"🖼️ Total images: {total_images}\n")
    log_file.write(f"✅ Polyp images: {polyp_count}\n")
    log_file.write(f"✅ Multiple polyp images: {multi_polyp_count}\n")
    log_file.write(f"✅ Non-polyp images: {non_polyp_count}\n")
    log_file.write(f"📄 CSV saved to: {CSV_OUTPUT_PATH}\n")

# --- Print Summary ---
print(f"🖼️ Total images: {total_images}")
print(f"✅ Polyp images: {polyp_count}")
print(f"✅ Multiple polyp images: {multi_polyp_count}")
print(f"✅ Non-polyp images: {non_polyp_count}")
print(f"📄 CSV saved to: {CSV_OUTPUT_PATH}")
print(f"📝 Stats saved to: {LOG_OUTPUT_PATH}")
