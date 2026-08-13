## Dataset

The project uses the Amazon Books Reviews dataset from Kaggle.

Due to dataset size constraints, the raw and processed datasets are not included in this repository.

Place downloaded datasets in:

data/raw/

Then run:

python src/preprocessing/trimmer.py
python src/preprocessing/data_5core_filter.py
python src/preprocessing/dataset_profile.py
