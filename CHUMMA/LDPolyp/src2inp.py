import os
import shutil

from pathlib import Path

# Change this to the path where your "TrainValid" folder is located
BASE_DIR = Path("/home/endodl/PHASE-1/LDPolypVideo/org_data")
IMAGES_SRC = BASE_DIR / "Images"
ANNOTS_SRC = BASE_DIR / "Annotations"

# New organized output directories
OUTPUT_DIR = Path("/home/endodl/PHASE-1/LDPolypVideo/bef_annot_data")
IMAGES_DST = OUTPUT_DIR / "images"
ANNOTS_DST = OUTPUT_DIR / "annotations"

# Create output folders if they don’t exist
IMAGES_DST.mkdir(parents=True, exist_ok=True)
ANNOTS_DST.mkdir(parents=True, exist_ok=True)

# Iterate through folders 1 to 160
for folder_idx in range(1, 161):
    img_folder = IMAGES_SRC / str(folder_idx)
    annot_folder = ANNOTS_SRC / str(folder_idx)

    img_files = sorted(img_folder.glob("*"))
    annot_files = sorted(annot_folder.glob("*.txt"))

    for img_file, annot_file in zip(img_files, annot_files):
        img_name = img_file.stem  # e.g., frame_001
        ext = img_file.suffix     # e.g., .jpg or .png

        new_name = f"ldpolyp_{folder_idx}_{img_name}"

        new_img_path = IMAGES_DST / f"{new_name}{ext}"
        new_annot_path = ANNOTS_DST / f"{new_name}.txt"

        shutil.copy2(img_file, new_img_path)
        shutil.copy2(annot_file, new_annot_path)

print("✅ All images and annotations flattened and renamed.")
