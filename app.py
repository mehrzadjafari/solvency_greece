import base64
import pandas as pd
import streamlit as st

# Create a button to download the DataFrame
def download_dataframe(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV file</a>'
    return href





st.write("""
# govgr web scraping app
""")

# read df from github
github_data_path = "https://raw.githubusercontent.com/mehrzadjafari/solvency_greece/main/"
df = pd.read_csv(github_data_path + 'table_data.csv')

# show df in app
st.dataframe(df)

if st.button('Download'):
    st.markdown(download_dataframe(df), unsafe_allow_html=True)