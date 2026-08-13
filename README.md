## Dataset

The project uses the Amazon Books Reviews dataset from Kaggle. https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews under CC0: Public Domain license.

Due to dataset size constraints, the raw and processed datasets are not included in this repository.

Place downloaded datasets in:

data/raw/

Then run:

python src/preprocessing/trimmer.py
python src/preprocessing/data_5core_filter.py
python src/preprocessing/dataset_profile.py

## Current Production Model

Model: book-recommender-knn
Version: 1
Stage: Production

Reason:
Outperformed the popularity baseline by producing title-specific recommendations rather than global rankings.
