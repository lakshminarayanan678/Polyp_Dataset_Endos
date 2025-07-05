import os
from pathlib import Path

# ====== CONFIG ======
image_folder = Path("/home/endoai/Desktop/PAPER/SegDatasets/CVC-ClinicDB/images")  # 🔁 CHANGE THIS
prefix_to_add = "CVC-ClinicDB_"  # Prefix to add to each file

# ====== Process Files ======
renamed_count = 0

# for file in sorted(image_folder.iterdir()):
#     if file.is_file() and file.name.startswith("c") and file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
#         new_name = prefix_to_add + file.name
#         new_path = image_folder / new_name
#         if not new_path.exists():
#             file.rename(new_path)
#             renamed_count += 1
#             print(f"✅ Renamed: {file.name} → {new_name}")
#         else:
#             print(f"⚠️ Skipped (already exists): {new_name}")

### For images starting with an number
for file in sorted(image_folder.iterdir()):
    if file.is_file() and file.stem.isdigit() and file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
        new_name = f"{prefix_to_add}{file.name}"
        new_path = image_folder / new_name
        if not new_path.exists():
            file.rename(new_path)
            renamed_count += 1
            print(f"✅ Renamed: {file.name} → {new_name}")
        else:
            print(f"⚠️ Skipped (already exists): {new_name}")        

print(f"\n🔁 Total files renamed: {renamed_count}")
