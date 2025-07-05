import os
from pathlib import Path

# ==== CONFIG ====
images_dir = Path("/home/endoai/Desktop/PAPER/Real-COLON/004-008_frames")         # Replace with your image folder
annotations_dir = Path("/home/endoai/Desktop/PAPER/Real-COLON/REAL_Colon/004-008/annotation_yolo")  # Replace with your annotation folder
dataset_prefix = "realcolon"

# ==== Gather annotation filenames (with prefix) ====
annotation_stems = {ann.stem for ann in annotations_dir.glob(f"{dataset_prefix}_*.txt")}
print(f"📄 Found {len(annotation_stems)} annotation files.")

# ==== Track stats ====
renamed = 0
deleted = 0

# ==== Process image files ====
for img_file in images_dir.glob("*"):
    if img_file.suffix.lower() not in [".jpg", ".png", ".jpeg"]:
        continue

    orig_stem = img_file.stem
    ext = img_file.suffix
    new_name = f"{dataset_prefix}_{orig_stem}{ext}"
    new_path = images_dir / new_name

    # Only keep and rename if corresponding annotation exists
    if f"{dataset_prefix}_{orig_stem}" in annotation_stems:
        if img_file.name != new_name:
            img_file.rename(new_path)
            renamed += 1
            print(f"✅ Renamed: {img_file.name} → {new_name}")
    else:
        img_file.unlink()
        deleted += 1
        print(f"🗑️ Deleted (no matching annotation): {img_file.name}")

print(f"\n✅ Done. Renamed: {renamed}, Deleted: {deleted}")
