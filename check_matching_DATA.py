import os
from pathlib import Path

# ====== CONFIG ======
combined_dir = Path("/home/endoai/Desktop/PAPER/DATA")
images_dir = combined_dir / "images"
annotations_dir = combined_dir / "annotations"
log_path = Path("/home/endoai/Desktop/PAPER/DATA/stats_log.txt")

image_exts = [".jpg", ".jpeg", ".png"]

# === STATS ===
image_files = sorted([f for f in images_dir.iterdir() if f.suffix.lower() in image_exts])
annotation_files = sorted([f for f in annotations_dir.glob("*.txt")])

total_images = len(image_files)
total_annots = len(annotation_files)
matched = 0
missing_annots = 0

polyp_images = 0
non_polyp_images = 0
multi_polyp_images = 0

polyp_count_to_files = {}
missing_annotation_files = []

# === PROCESS ===
for img in image_files:
    stem = img.stem
    annot_file = annotations_dir / f"{stem}.txt"

    if not annot_file.exists():
        missing_annots += 1
        missing_annotation_files.append(img.name)
        continue

    matched += 1

    with open(annot_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    polyps = sum(1 for line in lines if line.split()[0] == '0')

    if polyps == 0:
        non_polyp_images += 1
    else:
        polyp_images += 1
        if polyps > 1:
            multi_polyp_images += 1
        if polyps not in polyp_count_to_files:
            polyp_count_to_files[polyps] = []
        polyp_count_to_files[polyps].append(img.name)

# === LOGGING ===
log_lines = [
    "===== DATASET INTEGRITY & POLYP STATS =====",
    f"🖼️ Total image files                : {total_images}",
    f"📝 Total annotation files           : {total_annots}",
    f"✅ Image-annotation matches         : {matched}",
    f"❌ Missing annotations              : {missing_annots}",
]

log_lines.append("\n===== POLYP STATISTICS =====")
log_lines.append(f"✅ Images with ≥1 polyp             : {polyp_images}")
log_lines.append(f"❌ Images with 0 polyps             : {non_polyp_images}")
log_lines.append(f"📦 Images with multiple polyps      : {multi_polyp_images}")

log_lines.append("\n--- Polyp Count Distribution ---")
for count in sorted(polyp_count_to_files):
    log_lines.append(f"Images with {count} polyps         : {len(polyp_count_to_files[count])}")

log_lines.append("\n--- Files per Polyp Count ---")
for count in sorted(polyp_count_to_files):
    if count == 1:
        continue  # Skip logging individual filenames for 1 polyp
    log_lines.append(f"\n>> {count} polyps:")
    for fname in polyp_count_to_files[count]:
        log_lines.append(f" - {fname}")

if missing_annotation_files:
    log_lines.append("\n--- Missing Annotations for Images ---")
    for fname in missing_annotation_files:
        log_lines.append(f" - {fname}")

# === WRITE LOG ===
with open(log_path, "w") as f:
    f.write("\n".join(log_lines))

print(f"\n✅ Stats saved to {log_path}")

