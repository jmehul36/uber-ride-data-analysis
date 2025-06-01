import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder

st.set_page_config(layout="wide")
st.title("🚕 Uber Rides Data Analysis Dashboard")

# Load and clean dataset
@st.cache_data
def load_data():
    dataset = pd.read_csv("UberDataset.csv")
    dataset['PURPOSE'].fillna("NOT", inplace=True)
    dataset['START_DATE'] = pd.to_datetime(dataset['START_DATE'], errors='coerce')
    dataset['END_DATE'] = pd.to_datetime(dataset['END_DATE'], errors='coerce')
    dataset['date'] = pd.DatetimeIndex(dataset['START_DATE']).date
    dataset['time'] = pd.DatetimeIndex(dataset['START_DATE']).hour
    dataset['day-night'] = pd.cut(dataset['time'], bins=[0,10,15,19,24], labels=['Morning','Afternoon','Evening','Night'])
    dataset.dropna(inplace=True)
    dataset.drop_duplicates(inplace=True)
    return dataset

# Show code section
with st.expander("📜 Show Data Processing Code"):
    full_code = '''
        st.code(full_code, language='python')

# Run button
if st.button("▶️ Run Analysis"):
    df = load_data()

    # 1. Category and Purpose Distribution
    st.subheader("📊 Category and Purpose Distribution")
    st.markdown("This chart shows the number of rides by *Category* (Business/Personal) and by *Purpose* (e.g., Meeting, Meals, etc).")

    fig1, ax1 = plt.subplots(1, 2, figsize=(14, 5))
    sns.countplot(data=df, x='CATEGORY', ax=ax1[0])
    ax1[0].set_title("Ride Category")
    sns.countplot(data=df, x='PURPOSE', ax=ax1[1])
    ax1[1].set_title("Ride Purpose")
    for ax in ax1:
        for label in ax.get_xticklabels():
            label.set_rotation(45)
    st.pyplot(fig1)

    # 2. Time of Day
    st.subheader("🕒 Time of Day Distribution")
    st.markdown("This shows how rides are distributed throughout the day—morning, afternoon, evening, and night.")
    fig2, ax2 = plt.subplots()
    sns.countplot(data=df, x='day-night', ax=ax2)
    st.pyplot(fig2)

    # 3. Purpose vs Category
    st.subheader("📌 Purpose vs Category")
    st.markdown("This shows how ride purposes vary across business and personal categories.")
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    sns.countplot(data=df, x='PURPOSE', hue='CATEGORY', ax=ax3)
    ax3.set_title("Purpose Breakdown by Category")
    ax3.tick_params(axis='x', rotation=90)
    st.pyplot(fig3)

    # 4. Monthly Trends
    st.subheader("📆 Monthly Ride Trends")
    st.markdown("Maximum miles traveled per month and how frequently rides occur each month.")
    df['MONTH'] = df['START_DATE'].dt.month.map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'Aug',
        9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })
    monthly_counts = df['MONTH'].value_counts().sort_index()
    monthly_max_miles = df.groupby('MONTH')['MILES'].max()

    fig4, ax4 = plt.subplots()
    sns.lineplot(x=monthly_counts.index, y=monthly_max_miles.values, marker="o", ax=ax4)
    ax4.set_xlabel("Month")
    ax4.set_ylabel("Max Miles")
    st.pyplot(fig4)

    # 5. Day of Week Analysis
    st.subheader("📅 Day of the Week Analysis")
    st.markdown("Analyzing how Uber rides are distributed across different days of the week.")
    df['DAY'] = df['START_DATE'].dt.weekday.map({
        0: 'Mon', 1: 'Tues', 2: 'Wed', 3: 'Thurs', 4: 'Fri', 5: 'Sat', 6: 'Sun'
    })
    fig5, ax5 = plt.subplots()
    sns.barplot(x=df['DAY'].value_counts().index, y=df['DAY'].value_counts().values, ax=ax5)
    ax5.set_ylabel("Ride Count")
    st.pyplot(fig5)

    # 6. Miles Distribution
    st.subheader("📐 Ride Distance Analysis")
    st.markdown("Boxplot and distribution of miles. Useful to detect outliers or common trip distances.")
    
    fig6, ax6 = plt.subplots()
    sns.boxplot(x=df['MILES'], ax=ax6)
    ax6.set_title("Boxplot of Miles")
    st.pyplot(fig6)

    fig7, ax7 = plt.subplots()
    sns.histplot(df[df['MILES'] < 40]['MILES'], kde=True, ax=ax7)
    ax7.set_title("Distribution of Rides < 40 Miles")
    st.pyplot(fig7)

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
