### 📊 Datasets

This work aggregates publicly available colonoscopy datasets for polyp detection and classification.

### ✅ Benchmark Datasets

The following datasets were used as benchmarks for evaluation, as they are widely adopted in prior research:
- CVC-ClinicDB
- CVC-ColonDB 
- ETIS-LaribDB

### 📦 Training Datasets

The remaining datasets were used to build a composite training set and for pretraining models, enabling both:
- Intra-dataset testing – training and evaluating on splits of the same dataset.
- Inter-dataset testing – training on one dataset and evaluating on unseen datasets to assess generalization.

## 📦 Dataset Summary  

| Dataset              | Total Images | Polyp Images | Multiple Polyp Images | Non-Polyp Images |
|----------------------|-------------:|-------------:|----------------------:|-----------------:|
| **CVC-ClinicDB**     | 612          | 612          | 30                    | 0                |
| **CVC-ColonDB**      | 380          | 380          | –                     | 0                |
| **Kvasir-SEG**       | 1,000        | 1,000        | 48                    | 0                |
| **PolypGen**         | 1,473        | 1,347        | 123                   | 126              |
| **ETIS-LaribDB**     | 196          | 196          | 6                     | 0                |
| **LD-PolypVideo**    | 40,186       | 33,875       | 2,360                 | 6,311            |
| **KUMC (PolypSet)**  | 37,899       | 35,996       | 1                     | 1,903            |
| **Real-COLON (Raw)** | 138,091      | 15,660       | 3                     | 122,431          |
| **Real-COLON (Balanced)** | 76,876  | 15,660       | 3                     | 61,216           |
| **TOTAL (Raw)**      | 219,837      | 89,066       | –                     | 130,771          |
| **TOTAL (Balanced)** | 158,622      | 89,066       | –                     | 69,556           |


# 📂 Polyp Datasets  

This repository consolidates multiple gastrointestinal (GI) polyp datasets into a unified structure for both classification and segmentation tasks. All datasets have been standardized in terms of naming, format, and organization.  

---

### 🔹 DATA  
The `DATA/` folder contains the **collated master dataset**.  
- All images and annotations from different sources (Kvasir-SEG, CVC, PolypGen, LD-PolypVideo, Real-COLON, KUMC, etc.) are unified here.  
- Files are renamed with a dataset prefix (e.g., `Kvasir-SEG_xxx.jpg`, `realcolon_xxx.jpg`, `kumc_xxx.jpg`, `polypgen_xxx.jpg`) for traceability.  
- A `log.txt` file summarizes dataset integrity and statistics, including:  
  - Total number of images and annotations.  
  - Count of polyp vs. non-polyp images.  
  - Images with multiple polyps.  
  - Polyp count distribution (when available).  

---

### 🔹 SPLITDATA  
The `SPLITDATA/` folder contains the **train/validation/test splits** derived from the `DATA/` folder.  
- The entire collated dataset (`DATA/`) is split into train, val, and test sets.  
- These splits are **not per dataset** but rather across the full combined dataset.  
- A `log.txt` file here records split statistics (number of images, annotation matches, polyp vs. non-polyp counts, multiple polyps, etc.).  

---

### 🔹 SEGDATASETS  
The `SegDatasets/` folder contains datasets that include **segmentation masks**.  
- Each dataset with masks (e.g., **Kvasir-SEG, CVC-Clinic, CVC-Colon, ETIS-Larib**) has its own subfolder.  
- Each subfolder includes images, masks, and a `log.txt` file that reports dataset statistics (total images, multiple polyps, CSV with normalized paths, etc.).  

---

### 🔹 Logs & Integrity Checks  
- Every dataset folder (in `DATA/`, `SPLITDATA/`, and `SegDatasets/`) contains a `log.txt` file.  
- These logs ensure reproducibility by documenting:  
  - Dataset size and integrity (image–annotation matches).  
  - Polyp vs. non-polyp distribution.  
  - Multiple polyp breakdowns with file references.  

---

### 🔹 Balancing Strategy  
Some datasets, particularly **Real-COLON**, originally contained significantly more non-polyp than polyp images. To address this imbalance:  
- The number of non-polyp images was reduced by half in each subset.  
- This adjustment ensures a more balanced ratio between polyp and non-polyp images for training.  

---
