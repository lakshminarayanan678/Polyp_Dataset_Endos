import csv
from pathlib import Path
from collections import defaultdict

# --- CONFIG ---
csv_path = Path("/home/endoai/Desktop/PAPER/PolypGen/normalized.csv")  # << UPDATE THIS
output_txt_dir = Path("/home/endoai/Desktop/PAPER/PolypGen/annotations_yolo")  # Output folder
output_txt_dir.mkdir(parents=True, exist_ok=True)

# --- Read CSV & group bboxes by image ---
bboxes_by_image = defaultdict(list)
all_images = set()

with open(csv_path, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        img_name = row["image_filename"]
        all_images.add(img_name)

        # If bbox values are present
        if all(row[k] for k in ("cx", "cy", "bw", "bh")):
            cx = float(row["cx"])
            cy = float(row["cy"])
            bw = float(row["bw"])
            bh = float(row["bh"])
            yolo_line = f"0 {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}"
            bboxes_by_image[img_name].append(yolo_line)

# --- Write YOLO txt files ---
for img_name in sorted(all_images):
    txt_path = output_txt_dir / f"{Path(img_name).stem}.txt"
    with open(txt_path, "w") as f:
        for bbox in bboxes_by_image.get(img_name, []):
            f.write(bbox + "\n")

# --- Stats ---
print(f"✅ YOLO .txt annotations saved to: {output_txt_dir}")
print(f"🟢 Images with polyps: {len(bboxes_by_image)}")
print(f"⚪ Images without polyps: {len(all_images) - len(bboxes_by_image)}")
print(f"📝 Total .txt files written: {len(all_images)}")
