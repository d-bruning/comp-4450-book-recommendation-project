import pandas as pd

chunksize = 100000

cols = [
    "Id",
    "Title",
    "User_id",
    "review/score",
    "review/summary",
    "review/text"
]

first = True

for chunk in pd.read_csv(
    "Books_rating.csv",
    usecols=cols,
    chunksize=chunksize
):
    chunk.to_csv(
        "Books_rating_trimmed.csv",
        mode="w" if first else "a",
        header=first,
        index=False
    )
    first = False
