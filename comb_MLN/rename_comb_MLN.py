import shutil
from pathlib import Path

# --- CONFIG ---
mixed_dataset_path = Path("/home/endoai/Desktop/PAPER/comb_MLN")  # contains images/ and annotations/
images_dir = mixed_dataset_path / "images"
annots_dir = mixed_dataset_path / "labels"

output_dir = Path("/home/endoai/Desktop/PAPER/comb_MLN_renamed")
images_out = output_dir / "images"
annots_out = output_dir / "annotations"

# --- Create output dirs ---
images_out.mkdir(parents=True, exist_ok=True)
annots_out.mkdir(parents=True, exist_ok=True)

# --- Helper: Decide dataset source from filename ---
def get_dataset_prefix(filename_stem: str) -> str:
    if filename_stem.startswith("001-003"):
        return "realcolon"
    else:
        return "kumc"

# --- Process Images ---
for img_path in sorted(images_dir.glob("*")):
    prefix = get_dataset_prefix(img_path.stem)
    new_name = f"{prefix}_{img_path.name}"
    shutil.copy2(img_path, images_out / new_name)

# --- Process Annotations ---
for annot_path in sorted(annots_dir.glob("*.txt")):
    prefix = get_dataset_prefix(annot_path.stem)
    new_name = f"{prefix}_{annot_path.name}"
    shutil.copy2(annot_path, annots_out / new_name)

print("✅ Done renaming and organizing mixed dataset!")
print(f"📁 Output saved to: {output_dir}")
