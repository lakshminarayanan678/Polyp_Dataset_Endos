import csv
import random
from pathlib import Path

# --- CONFIG ---
input_csv = Path("/home/endoai/Desktop/PAPER/Real-COLON/REAL_Colon/004-008/normalized.csv")  # Update this
output_csv = Path("/home/endoai/Desktop/PAPER/Real-COLON/REAL_Colon/004-008/red_normalized.csv")  # Output file

with open(input_csv, "r") as f:
    reader = list(csv.reader(f))
    header = reader[0]
    data_rows = reader[1:]

# --- Split rows ---
total_original_rows = len(data_rows)
polyp_rows = [row for row in data_rows if row[1] == "0"]
nonpolyp_rows = [row for row in data_rows if row[1] == ""]

# --- Sample 50% of non-polyp rows ---
keep_count = len(nonpolyp_rows) // 2
random.seed(42)  # For reproducibility
kept_nonpolyps = random.sample(nonpolyp_rows, keep_count)

# --- Combine final rows ---
final_rows = polyp_rows + kept_nonpolyps
final_rows.sort()  # Optional: sort by filename

# --- Write new CSV ---
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(final_rows)

# --- Summary ---
print("=== CSV Filtering Summary ===")
print(f"📄 Input CSV: {input_csv}")
print(f"📝 Output CSV: {output_csv}")
print(f"🔢 Total rows in input CSV      : {total_original_rows}")
print(f"✅ Polyp rows kept              : {len(polyp_rows)}")
print(f"✅ Non-polyp rows originally    : {len(nonpolyp_rows)}")
print(f"✅ Non-polyp rows kept (50%)    : {len(kept_nonpolyps)}")
print(f"🟢 Total rows in filtered output: {len(final_rows)}")
