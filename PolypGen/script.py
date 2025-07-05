import os
import shutil
import csv
from PIL import Image
from pathlib import Path

BASE_DIR= Path("/home/endodl/PHASE-1/PolypGen2021_MultiCenterData_v3")
OUTPUT_DIR= Path("/home/endodl/PHASE-1/PolypGen")
# BASE_DIR = os.getcwd()
#OUTPUT_DIR = os.path.join(BASE_DIR, "DATA")
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
BBOX_DIR = os.path.join(OUTPUT_DIR, "annotations")
CSV_PATH = os.path.join(OUTPUT_DIR, "normalized.csv")
LOG_PATH = os.path.join(OUTPUT_DIR, "log.txt")

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(BBOX_DIR, exist_ok=True)

csv_rows = [("image_filename", "label", "cx", "cy", "bw", "bh")]

total_images = 0
total_txt = 0
multi_polyp_images = 0
total_polyp_images = 0
total_no_polyp_images = 0

print("\n--- Starting _mask Removal Process ---\n")

# Remove _mask from bbox file names
for folder_name in sorted(os.listdir(BASE_DIR)):
    if folder_name.startswith("data_C") and os.path.isdir(os.path.join(BASE_DIR, folder_name)):
        
        cluster_id = folder_name.split("_")[1]
        bbox_folder = os.path.join(BASE_DIR, folder_name, f"bbox_{cluster_id}")

        if not os.path.exists(bbox_folder):
            continue
        
        for file in os.listdir(bbox_folder):
            if file.endswith(".txt") and "_mask" in file:
                new_name = file.replace("_mask", "")
                src = os.path.join(bbox_folder, file)
                dst = os.path.join(bbox_folder, new_name)
                
                if not os.path.exists(dst):
                    os.rename(src, dst)
                    print(f"Renamed: {file} -> {new_name}")

print("\n--- _mask Cleanup Complete ---\n")

# Processing images and bboxes
for folder_name in sorted(os.listdir(BASE_DIR)):
    if folder_name.startswith("data_C") and os.path.isdir(os.path.join(BASE_DIR, folder_name)):
        
        cluster_id = folder_name.split("_")[1]
        images_folder = os.path.join(BASE_DIR, folder_name, f"images_{cluster_id}")
        bbox_folder = os.path.join(BASE_DIR, folder_name, f"bbox_{cluster_id}")

        if not os.path.exists(images_folder) or not os.path.exists(bbox_folder):
            continue

        image_files = {os.path.splitext(f)[0]: f for f in os.listdir(images_folder) if f.lower().endswith((".jpg", ".png"))}
        bbox_files = {os.path.splitext(f)[0]: f for f in os.listdir(bbox_folder) if f.lower().endswith(".txt")}

        common_keys = sorted(set(image_files.keys()) & set(bbox_files.keys()))

        for idx, key in enumerate(common_keys, start=1):
            ordered_id = f"{idx:05d}"
            new_name = f"{cluster_id}_{ordered_id}"
            
            src_img = os.path.join(images_folder, image_files[key])
            dest_img = os.path.join(IMAGES_DIR, f"polypgen_{new_name}{os.path.splitext(src_img)[1]}")
            shutil.copy2(src_img, dest_img)

            src_txt = os.path.join(bbox_folder, bbox_files[key])
            dest_txt = os.path.join(BBOX_DIR, f"polypgen_{new_name}.txt")
            shutil.copy2(src_txt, dest_txt)

            total_images += 1
            total_txt += 1

            with Image.open(src_img) as img:
                width, height = img.size

            with open(src_txt, "r") as f:
                lines = [line.strip() for line in f if line.strip()]

            polyp_count = sum(1 for line in lines if "polyp" in line.lower())

            if not lines:
                csv_rows.append((f"polypgen_{new_name}{os.path.splitext(src_img)[1]}", "", "", "", "", ""))
                total_no_polyp_images += 1
            else:
                for line in lines:
                    parts = line.split()
                    if len(parts) != 5:
                        continue
                    
                    label, x_min, y_min, x_max, y_max = parts
                    label = 0 if label.lower() == "polyp" else label
                    x_min, y_min, x_max, y_max = map(float, (x_min, y_min, x_max, y_max))

                    center_x = (x_min + x_max) / 2 / width
                    center_y = (y_min + y_max) / 2 / height
                    bbox_w = (x_max - x_min) / width
                    bbox_h = (y_max - y_min) / height

                    csv_rows.append((f"polypgen_{new_name}{os.path.splitext(src_img)[1]}", label, f"{center_x:.6f}", f"{center_y:.6f}", f"{bbox_w:.6f}", f"{bbox_h:.6f}"))

                if polyp_count > 1:
                    multi_polyp_images += 1
                if polyp_count >= 1:
                    total_polyp_images += 1
                if polyp_count == 0:
                    total_no_polyp_images += 1

# Save CSV
with open(CSV_PATH, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_rows)

# Save log
with open(LOG_PATH, "w") as f:
    f.write(f"Total images saved: {total_images}\n")
    f.write(f"Total txt files saved: {total_txt}\n")
    f.write(f"Total multiple polyp images: {multi_polyp_images}\n")
    f.write(f"Total polyp images found: {total_polyp_images}\n")
    f.write(f"Total no polyp images: {total_no_polyp_images}\n")

print(f"\nCSV saved to {CSV_PATH}")
print(f"Log saved to {LOG_PATH}\n")
print("--- Process Complete ---")
