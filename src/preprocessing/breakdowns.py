import pandas as pd

df = pd.read_csv(
    "Books_rating_trimmed.csv",
    usecols=["User_id", "Title"]
)

print("\nReviews per User")
print(df.groupby("User_id").size().describe())

print("\nReviews per Book")
print(df.groupby("Title").size().describe())
