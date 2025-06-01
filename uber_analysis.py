# uber_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder

# Load dataset
dataset = pd.read_csv("UberDataset.csv")

# Fill missing PURPOSE values
dataset['PURPOSE'].fillna("NOT", inplace=True)

# Convert dates
dataset['START_DATE'] = pd.to_datetime(dataset['START_DATE'], errors='coerce')
dataset['END_DATE'] = pd.to_datetime(dataset['END_DATE'], errors='coerce')

# Extract date and time
dataset['date'] = pd.DatetimeIndex(dataset['START_DATE']).date
dataset['time'] = pd.DatetimeIndex(dataset['START_DATE']).hour

# Categorize time of day
dataset['day-night'] = pd.cut(
    x=dataset['time'],
    bins=[0, 10, 15, 19, 24],
    labels=['Morning', 'Afternoon', 'Evening', 'Night']
)

# Clean data
dataset.dropna(inplace=True)
dataset.drop_duplicates(inplace=True)

# Unique values in object columns
obj = (dataset.dtypes == 'object')
object_cols = list(obj[obj].index)
unique_values = {col: dataset[col].nunique() for col in object_cols}
print("Unique categorical values:\n", unique_values)

# Countplots
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
sns.countplot(x='CATEGORY', data=dataset)
plt.xticks(rotation=90)

plt.subplot(1, 2, 2)
sns.countplot(x='PURPOSE', data=dataset)
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("category_purpose.png")

sns.countplot(x='day-night', data=dataset)
plt.xticks(rotation=90)
plt.savefig("day_night.png")

plt.figure(figsize=(15, 5))
sns.countplot(data=dataset, x='PURPOSE', hue='CATEGORY')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("purpose_category.png")

# One-hot encoding
OH_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
OH_cols = pd.DataFrame(OH_encoder.fit_transform(dataset[object_cols]))
OH_cols.index = dataset.index
OH_cols.columns = OH_encoder.get_feature_names_out()
dataset = pd.concat([dataset.drop(object_cols, axis=1), OH_cols], axis=1)

# Correlation heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(dataset.select_dtypes(include='number').corr(), cmap='BrBG', annot=True, fmt='.2f')
plt.tight_layout()
plt.savefig("correlation.png")

# Monthly ride analysis
dataset['MONTH'] = dataset['START_DATE'].dt.month
month_label = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'Aug',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}
dataset['MONTH'] = dataset['MONTH'].map(month_label)

mon = dataset['MONTH'].value_counts(sort=False)
max_miles = dataset.groupby('MONTH', sort=False)['MILES'].max()
df = pd.DataFrame({"MONTHS": mon.index, "VALUE COUNT": max_miles.values})

sns.lineplot(data=df, x="MONTHS", y="VALUE COUNT")
plt.xlabel("MONTHS")
plt.ylabel("VALUE COUNT")
plt.savefig("monthly_miles.png")

# Day of week analysis
dataset['DAY'] = dataset['START_DATE'].dt.weekday.map({
    0: 'Mon', 1: 'Tues', 2: 'Wed', 3: 'Thurs', 4: 'Fri', 5: 'Sat', 6: 'Sun'
})
sns.barplot(x=dataset['DAY'].value_counts().index, y=dataset['DAY'].value_counts().values)
plt.xlabel('DAY')
plt.ylabel('COUNT')
plt.savefig("day_distribution.png")

# Boxplots & Distribution
sns.boxplot(x=dataset['MILES'])
plt.savefig("miles_boxplot.png")

sns.boxplot(x=dataset[dataset['MILES'] < 100]['MILES'])
plt.savefig("miles_under_100_boxplot.png")

sns.histplot(dataset[dataset['MILES'] < 40]['MILES'], kde=True)
plt.savefig("miles_under_40_distplot.png")
