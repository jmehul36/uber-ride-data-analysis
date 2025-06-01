# # uber_analysis.py

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from datetime import datetime
# from sklearn.preprocessing import OneHotEncoder

# # Load dataset
# dataset = pd.read_csv("UberDataset.csv")

# # Fill missing PURPOSE values
# dataset['PURPOSE'].fillna("NOT", inplace=True)

# # Convert dates
# dataset['START_DATE'] = pd.to_datetime(dataset['START_DATE'], errors='coerce')
# dataset['END_DATE'] = pd.to_datetime(dataset['END_DATE'], errors='coerce')

# # Extract date and time
# dataset['date'] = pd.DatetimeIndex(dataset['START_DATE']).date
# dataset['time'] = pd.DatetimeIndex(dataset['START_DATE']).hour

# # Categorize time of day
# dataset['day-night'] = pd.cut(
#     x=dataset['time'],
#     bins=[0, 10, 15, 19, 24],
#     labels=['Morning', 'Afternoon', 'Evening', 'Night']
# )

# # Clean data
# dataset.dropna(inplace=True)
# dataset.drop_duplicates(inplace=True)

# # Unique values in object columns
# obj = (dataset.dtypes == 'object')
# object_cols = list(obj[obj].index)
# unique_values = {col: dataset[col].nunique() for col in object_cols}
# print("Unique categorical values:\n", unique_values)

# # Countplots
# plt.figure(figsize=(6, 3))
# plt.subplot(1, 2, 1)
# sns.countplot(x='CATEGORY', data=dataset)
# plt.xticks(rotation=90)

# plt.subplot(1, 2, 2)
# sns.countplot(x='PURPOSE', data=dataset)
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.savefig("category_purpose.png")

# sns.countplot(x='day-night', data=dataset)
# plt.xticks(rotation=90)
# plt.savefig("day_night.png")

# plt.figure(figsize=(6, 3))
# sns.countplot(data=dataset, x='PURPOSE', hue='CATEGORY')
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.savefig("purpose_category.png")

# # One-hot encoding
# OH_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
# OH_cols = pd.DataFrame(OH_encoder.fit_transform(dataset[object_cols]))
# OH_cols.index = dataset.index
# OH_cols.columns = OH_encoder.get_feature_names_out()
# dataset = pd.concat([dataset.drop(object_cols, axis=1), OH_cols], axis=1)

# # Correlation heatmap
# plt.figure(figsize=(6, 3))
# sns.heatmap(dataset.select_dtypes(include='number').corr(), cmap='BrBG', annot=True, fmt='.2f')
# plt.tight_layout()
# plt.savefig("correlation.png")

# # Monthly ride analysis
# dataset['MONTH'] = dataset['START_DATE'].dt.month
# month_label = {
#     1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'April',
#     5: 'May', 6: 'June', 7: 'July', 8: 'Aug',
#     9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
# }
# dataset['MONTH'] = dataset['MONTH'].map(month_label)

# mon = dataset['MONTH'].value_counts(sort=False)
# max_miles = dataset.groupby('MONTH', sort=False)['MILES'].max()
# df = pd.DataFrame({"MONTHS": mon.index, "VALUE COUNT": max_miles.values})

# sns.lineplot(data=df, x="MONTHS", y="VALUE COUNT")
# plt.xlabel("MONTHS")
# plt.ylabel("VALUE COUNT")
# plt.savefig("monthly_miles.png")

# # Day of week analysis
# dataset['DAY'] = dataset['START_DATE'].dt.weekday.map({
#     0: 'Mon', 1: 'Tues', 2: 'Wed', 3: 'Thurs', 4: 'Fri', 5: 'Sat', 6: 'Sun'
# })
# sns.barplot(x=dataset['DAY'].value_counts().index, y=dataset['DAY'].value_counts().values)
# plt.xlabel('DAY')
# plt.ylabel('COUNT')
# plt.savefig("day_distribution.png")

# # Boxplots & Distribution
# sns.boxplot(x=dataset['MILES'])
# plt.savefig("miles_boxplot.png")

# sns.boxplot(x=dataset[dataset['MILES'] < 100]['MILES'])
# plt.savefig("miles_under_100_boxplot.png")

# sns.histplot(dataset[dataset['MILES'] < 40]['MILES'], kde=True)
# plt.savefig("miles_under_40_distplot.png")



import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder

st.set_page_config(layout="wide")
st.title("🚕 Uber Rides Data Analysis Dashboard")

@st.cache_data
def load_data():
    dataset = pd.read_csv("UberDataset.csv")
    dataset['PURPOSE'].fillna("NOT", inplace=True)
    dataset['START_DATE'] = pd.to_datetime(dataset['START_DATE'], errors='coerce')
    dataset['END_DATE'] = pd.to_datetime(dataset['END_DATE'], errors='coerce')
    dataset['date'] = pd.DatetimeIndex(dataset['START_DATE']).date
    dataset['time'] = pd.DatetimeIndex(dataset['START_DATE']).hour
    dataset['day-night'] = pd.cut(
        x=dataset['time'],
        bins=[0, 10, 15, 19, 24],
        labels=['Morning', 'Afternoon', 'Evening', 'Night']
    )
    dataset.dropna(inplace=True)
    dataset.drop_duplicates(inplace=True)

    # One-hot encoding for correlation
    obj = (dataset.dtypes == 'object')
    object_cols = list(obj[obj].index)
    OH_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    OH_cols = pd.DataFrame(OH_encoder.fit_transform(dataset[object_cols]))
    OH_cols.index = dataset.index
    OH_cols.columns = OH_encoder.get_feature_names_out()
    dataset = pd.concat([dataset.drop(object_cols, axis=1), OH_cols], axis=1)

    return dataset

df = load_data()

st.markdown("### 📊 Category & Purpose Distribution")
fig1, ax = plt.subplots(1, 2, figsize=(10, 3.5))
sns.countplot(x='CATEGORY', data=df, ax=ax[0])
ax[0].set_title("CATEGORY")
sns.countplot(x='PURPOSE_NOT', data=df, ax=ax[1])
ax[1].set_title("PURPOSE")
for a in ax:
    a.tick_params(axis='x', rotation=45)
st.pyplot(fig1)

st.markdown("### 🕒 Day-Night Distribution")
fig2, ax2 = plt.subplots(figsize=(6, 3))
sns.countplot(x='day-night_Afternoon', data=df, ax=ax2)
ax2.set_title("Day vs Night")
st.pyplot(fig2)

st.markdown("### 🔄 Purpose by Category")
fig3, ax3 = plt.subplots(figsize=(8, 3))
sns.countplot(x='PURPOSE_NOT', hue='CATEGORY_Business', data=df, ax=ax3)
ax3.tick_params(axis='x', rotation=45)
st.pyplot(fig3)

st.markdown("### 📈 Monthly Ride Analysis")
df['MONTH'] = pd.to_datetime(df['START_DATE']).dt.month
month_label = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}
df['MONTH'] = df['MONTH'].map(month_label)
monthly = df['MONTH'].value_counts(sort=False)
max_miles = df.groupby('MONTH')['MILES'].max()
mon_df = pd.DataFrame({"MONTHS": monthly.index, "MAX_MILES": max_miles.values})
fig4, ax4 = plt.subplots(figsize=(7, 3))
sns.lineplot(data=mon_df, x="MONTHS", y="MAX_MILES", ax=ax4, marker="o")
ax4.set_ylabel("Max Miles")
st.pyplot(fig4)

st.markdown("### 📅 Rides by Day of Week")
df['DAY'] = pd.to_datetime(df['START_DATE']).dt.weekday.map({
    0: 'Mon', 1: 'Tues', 2: 'Wed', 3: 'Thurs', 4: 'Fri', 5: 'Sat', 6: 'Sun'
})
fig5, ax5 = plt.subplots(figsize=(7, 3))
sns.barplot(x=df['DAY'].value_counts().index, y=df['DAY'].value_counts().values, ax=ax5)
ax5.set_ylabel("Ride Count")
st.pyplot(fig5)

st.markdown("### 📐 Ride Distance Boxplot")
fig6, ax6 = plt.subplots(figsize=(7, 3))
sns.boxplot(x=df['MILES'], ax=ax6)
st.pyplot(fig6)

st.markdown("### 🚗 Rides < 100 Miles Boxplot")
fig7, ax7 = plt.subplots(figsize=(7, 3))
sns.boxplot(x=df[df['MILES'] < 100]['MILES'], ax=ax7)
st.pyplot(fig7)

st.markdown("### 🚘 Rides < 40 Miles Distribution")
fig8, ax8 = plt.subplots(figsize=(7, 3))
sns.histplot(df[df['MILES'] < 40]['MILES'], kde=True, ax=ax8, bins=20)
st.pyplot(fig8)

# Footer
st.markdown("---")
footer_html = """
<div style="text-align: center; color: gray; font-size: 14px; margin-top: 20px;">
    <p>Made with ❤️ using <a href="https://streamlit.io/" target="_blank" style="text-decoration:none; color:gray;">Streamlit</a> by <strong>Mehul Jain</strong></p>
    <p>© 2025 Mehul Jain. All rights reserved.</p>
    <p>
        <a href="https://www.linkedin.com/in/mehul-jain-368020193" target="_blank" style="text-decoration:none;">
            <img src="https://cdn-icons-png.flaticon.com/24/174/174857.png" alt="LinkedIn" style="vertical-align:middle;"/>
        </a>
    </p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
