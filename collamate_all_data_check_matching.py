import shutil
from pathlib import Path

# ====== CONFIG ======

# List your datasets with renamed files
datasets = [
    {
        "images": Path("/home/endoai/Desktop/PAPER/LDPolypVideo/bef_annot_data/images"),
        "annotations": Path("/home/endoai/Desktop/PAPER/LDPolypVideo/bef_annot_data/annotations_yolo"),
    },
    {
        "images": Path("/home/endoai/Desktop/PAPER/PolypGen/images"),
        "annotations": Path("/home/endoai/Desktop/PAPER/PolypGen/annotations_yolo"),
    },
    {
        "images": Path("/home/endoai/Desktop/PAPER/Real-COLON/002-001_frames"),
        "annotations": Path("/home/endoai/Desktop/PAPER/Real-COLON/REAL_Colon/002-001/annotations_yolo"),
    },
    {
        "images": Path("/home/endoai/Desktop/PAPER/Real-COLON/003-001_frames"),
        "annotations": Path("/home/endoai/Desktop/PAPER/Real-COLON/REAL_Colon/003-001/annotations_yolo"),
    },
    {
        "images": Path("/home/endoai/Desktop/PAPER/Real-COLON/004-008_frames"),
        "annotations": Path("/home/endoai/Desktop/PAPER/Real-COLON/REAL_Colon/004-008/annotations_yolo"),
    },    {
        "images": Path("/home/endoai/Desktop/PAPER/SegDatasets/Kvasir-SEG/images"),
        "annotations": Path("/home/endoai/Desktop/PAPER/SegDatasets/Kvasir-SEG/annotations_yolo"),
    },
]

# Target directory where everything will be copied
target_dir = Path("/home/endoai/Desktop/PAPER/DATA")
images_dst = target_dir / "images"
annots_dst = target_dir / "annotations"

# Ensure output directories exist
images_dst.mkdir(parents=True, exist_ok=True)
annots_dst.mkdir(parents=True, exist_ok=True)

# ====== COPY ======

for ds in datasets:
    img_dir = ds["images"]
    annot_dir = ds["annotations"]

    if not img_dir.exists() or not annot_dir.exists():
        print(f"⚠️ Skipping a dataset: one or both folders missing")
        continue

    # Copy all image files
    img_files = list(img_dir.glob("*"))
    for img_path in img_files:
        shutil.copy2(img_path, images_dst / img_path.name)

    # Copy all annotation files
    txt_files = list(annot_dir.glob("*.txt"))
    for txt_path in txt_files:
        shutil.copy2(txt_path, annots_dst / txt_path.name)

    print(f"✅ Copied {len(img_files)} images and {len(txt_files)} annotations from: {img_dir.parent.name}")

print(f"\n🎉 All files copied into: {target_dir}")
