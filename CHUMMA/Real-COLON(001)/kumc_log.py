from pathlib import Path

# --- CONFIG ---
annotations_dir = Path("/media/endodl/NewVolume/moved_unknown/mln/POLYP/codes_MLN/combined/root_data/splits/val/labels")   # Folder with YOLO .txt files
exclude_prefix = "001-003"    
log_output_path = Path("/media/endodl/NewVolume/moved_unknown/mln/PAPER/data/Real-COLON/log_test.txt")  # Where to save stats

# --- Counters ---
total_images = 0
polyp_count = 0
multi_polyp_count = 0
non_polyp_count = 0
multi_polyp_files = []

# --- Process each annotation file ---
for txt_file in sorted(annotations_dir.glob("*.txt")):
    if txt_file.name.startswith(exclude_prefix):
        continue

    total_images += 1

    with open(txt_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) == 0:
        non_polyp_count += 1
    elif len(lines) == 1:
        polyp_count += 1
    else:
        polyp_count += 1
        multi_polyp_count += 1
        multi_polyp_files.append(txt_file.name)

# --- Print to console ---
print(f"🖼️ Total images: {total_images}")
print(f"✅ Polyp images: {polyp_count}")
print(f"✅ Multiple polyp images: {multi_polyp_count}")
print(f"✅ Non-polyp images: {non_polyp_count}")

if multi_polyp_files:
    print("📌 Files with multiple polyps:")
    for fname in multi_polyp_files:
        print(f" - {fname}")

# --- Save to log file ---
with open(log_output_path, "w") as log_file:
    log_file.write(f"🖼️ Total images: {total_images}\n")
    log_file.write(f"✅ Polyp images: {polyp_count}\n")
    log_file.write(f"✅ Multiple polyp images: {multi_polyp_count}\n")
    log_file.write(f"✅ Non-polyp images: {non_polyp_count}\n")
    log_file.write("📌 Files with multiple polyps:\n")
    for fname in multi_polyp_files:
        log_file.write(f" - {fname}\n")

print(f"📝 Log saved to: {log_output_path}")
