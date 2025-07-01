
# stick-trap-pipeline

This repository contains code to process a batch of images to:

- Identify and isolate the **main yellow region** of each sticky trap,
- **Crop** to that yellow area (i.e. excluding background from the photo),
- **Detect and quantify** how much of that area is **covered by non-yellow content** (i.e. insects),
- **Highlight non-yellow regions** in green for visual validation,
- Output a `.csv` file reporting the **proportion of non-yellow content** for each image.

---

## Folder Structure

```
stick-trap-pipeline/
├── photos/
│   ├── reference-clean/                    ← Folder of clean yellow references (used for calibration)
│   └── test-batch/                         ← Folder of target images to process (example)
├── outputs/
│   └── test-output.csv                     ← Generated output CSV file
├── code/
|   └── trap-proportion-colour-grid.py      ← The image processing script
└── README.md
```

---

## Requirements

This project includes a `requirements.txt` file to recreate the relevant virtual environment which is called `sticky`.

```bash
python -m venv sticky
source sticky/bin/activate  # or sticky\Scripts\activate on Windows
pip install -r requirements.txt
```
---

## How It Works

### 1. Calibrate Yellow Detection
The script starts by analyzing all images in the `reference-clean/` folder. It:
- Converts them to HSV color space,
- Detects "yellow" pixels using a default range,
- Refines that range based on the actual hue values detected.

This makes the detection robust to lighting changes and camera variation.

### 2. Process Each Image
For each image in, for example, the `test-batch/` folder (but any folder can be called):
- It finds and crops the largest yellow area,
- Counts how many pixels within it are **not yellow**,
- Highlights non-yellow pixels in green,
- Returns the proportion of non-yellow coverage.

### 3. Save Results
It writes a `CSV` file with two columns:
- `image`: The filename,
- `proportion`: The non-yellow content ratio (from 0 to 1).

---

## 🧪 Running the Script

Make sure your reference and test folders are set correctly inside the script. For example, to use images from the `photos/reference-clean/` folder, target photos from the `photos/test-batch` folder and to make a .csv file with the results called `outputs/test-output.csv`, modify these parts of the script: 

  `code/trap-proportion-colour-grid.py`

```python
reference_dir = "./photos/reference-clean/"
batch_name = "./photos/test-batch"
output_path = "./outputs/test-output.csv"
```

Then run the script via the terminal:

```bash
python code/trap-proportion-colour-grid.py
```

You will see:
- A printed output of each image's proportion,
- Visual pop-ups showing non-yellow areas in green (via `matplotlib`),
- A saved CSV at `./outputs/test-output.csv`.

---

## 📊 Output Example

```csv
image,proportion
image3-colour-scale.jpeg,0.0832
image4-colour-scale.jpeg,0.1165
image5-colour-scale.jpeg,0.0359
```

---

## Tips

- Use **clean, well-lit yellow reference images** in `reference-clean/`.
- Ensure all target images are consistently sized and framed.
- Modify kernel sizes in morphological operations for larger or noisier images.

---




