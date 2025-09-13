### 📊 Datasets

This work aggregates publicly available colonoscopy datasets for polyp detection and classification.

### ✅ Benchmark Datasets

The following datasets were used as benchmarks for evaluation, as they are widely adopted in prior research:

CVC-ClinicDB

CVC-ColonDB

ETIS-LaribDB

### 📦 Training Datasets

The remaining datasets were used to build a composite training set and for pretraining models, enabling both:

Intra-dataset testing – training and evaluating on splits of the same dataset.

Inter-dataset testing – training on one dataset and evaluating on unseen datasets to assess generalization.

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
