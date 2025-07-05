import os
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
from collections import defaultdict, Counter

# === CONFIGURATION ===
base_dir = Path("/home/endoai/Desktop/PAPER/DATA")  # Folder with 'images/' and 'labels/'
output_dir = Path("/home/endoai/Desktop/PAPER/SPLITDATA")  # Output folders: train/val/test

images_dir = base_dir / "images"
labels_dir = base_dir / "annotations"

# Split percentages
splits = {
    "train": 0.7,
    "val": 0.2,
    "test": 0.1
}

# === COLLECT IMAGE STEMS ===
image_files = sorted([f for f in images_dir.glob("*") if f.suffix.lower() in [".jpg", ".png"]])
image_stems = [f.stem for f in image_files]

# === SPLIT ===
train_stems, temp_stems = train_test_split(image_stems, test_size=(1 - splits["train"]), random_state=42)
val_stems, test_stems = train_test_split(temp_stems, test_size=(splits["test"] / (splits["val"] + splits["test"])), random_state=42)

dataset_split = {
    "train": train_stems,
    "val": val_stems,
    "test": test_stems,
}

# === HELPER FUNCTION ===
def analyze_split(split_name, stems, split_output_dir):
    split_img_dir = split_output_dir / "images"
    split_label_dir = split_output_dir / "labels"
    split_img_dir.mkdir(parents=True, exist_ok=True)
    split_label_dir.mkdir(parents=True, exist_ok=True)

    log_lines = []
    total_imgs = 0
    matched_labels = 0
    missing_labels = []
    polyp_images = 0
    no_polyp_images = 0
    multiple_polyps = 0

    polyp_count_dict = defaultdict(list)
    dataset_source_counter = Counter()

    for stem in stems:
        # Copy image
        img_src = images_dir / f"{stem}.jpg"
        if not img_src.exists():
            img_src = images_dir / f"{stem}.png"
        if img_src.exists():
            shutil.copy2(img_src, split_img_dir / img_src.name)
            total_imgs += 1

            # Count by dataset prefix (before first underscore)
            prefix = stem.split("_")[0]
            dataset_source_counter[prefix] += 1
        else:
            continue

        # Check label
        label_path = labels_dir / f"{stem}.txt"
        if not label_path.exists():
            missing_labels.append(img_src.name)
            continue

        shutil.copy2(label_path, split_label_dir / label_path.name)
        matched_labels += 1

        with open(label_path) as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            no_polyp_images += 1
        else:
            polyps = [line for line in lines if line.split()[0] == '0']
            num_polyps = len(polyps)
            if num_polyps > 0:
                polyp_images += 1
                if num_polyps > 1:
                    multiple_polyps += 1
                    polyp_count_dict[num_polyps].append(img_src.name)

    # === LOG CONTENT ===
    log_lines.append("===== DATASET INTEGRITY & POLYP STATS =====")
    log_lines.append(f"🖼️ Total image files                : {total_imgs}")
    log_lines.append(f"📝 Total label files                : {matched_labels + len(missing_labels)}")
    log_lines.append(f"✅ Image-label matches              : {matched_labels}")
    log_lines.append(f"❌ Missing labels                   : {len(missing_labels)}")

    log_lines.append("\n===== POLYP STATISTICS =====")
    log_lines.append(f"✅ Images with ≥1 polyp             : {polyp_images}")
    log_lines.append(f"❌ Images with 0 polyps             : {no_polyp_images}")
    log_lines.append(f"📦 Images with multiple polyps      : {multiple_polyps}")

    if polyp_count_dict:
        log_lines.append("\n--- Polyp Count Distribution ---")
        for k in sorted(polyp_count_dict.keys()):
            log_lines.append(f"Images with {k} polyps         : {len(polyp_count_dict[k])}")

        log_lines.append("\n--- Files per Polyp Count ---")
        for k in sorted(polyp_count_dict.keys()):
            log_lines.append(f">> {k} polyps:")
            for name in polyp_count_dict[k]:
                log_lines.append(f" - {name}")
            log_lines.append("")

    if missing_labels:
        log_lines.append("\n--- Missing Labels for Images ---")
        for name in missing_labels:
            log_lines.append(f" - {name}")

    # === Dataset Composition ===
    log_lines.append("\n===== DATASET COMPOSITION =====")
    for dataset_name, count in dataset_source_counter.items():
        log_lines.append(f"📁 {dataset_name} images in {split_name}: {count}")

    # Save log
    log_path = split_output_dir / "log.txt"
    with open(log_path, "w") as f:
        f.write("\n".join(log_lines))

    print(f"✅ {split_name.upper()} logged at: {log_path}")

# === PROCESS SPLITS ===
for split_name, stems in dataset_split.items():
    analyze_split(split_name, stems, output_dir / split_name)

print("\n🎉 Dataset split and logging complete.")
