import base64
import pandas as pd
import streamlit as st
from datetime import datetime, date
import streamlit as st
import io

from extractor import extractor

@st.cache_data
def cached_extractor(user_date):
    return extractor(user_date)

def download_dataframe(df):
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    excel_file.seek(0)
    excel_data = excel_file.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data.xlsx">Download Excel file</a>'
    return href

def main():
    # Create two columns
    col1, col2, col3 = st.columns([1, 2, 1])

    # Center-align the title
    col2.markdown("<h1 style='text-align: center;'>MMEA Transformation</h1>", unsafe_allow_html=True)
    selected_date = st.date_input("Select a date", date.today())
    user_date = datetime.combine(selected_date, datetime.min.time()).date()
    run_app(user_date)
    


def run_app(user_date):

    # Call the cached_extractor function to get the table data and header values
    table_data, header_values = cached_extractor(user_date)

    # Convert the table_data list to a DataFrame
    df = pd.DataFrame(table_data, columns=header_values)

    # Display the DataFrame in the app
    st.title("ΕΓΔΙΧ - Scraping Application")
    st.dataframe(df)

    if st.button('Download'):
        download_link = download_dataframe(df)
        st.markdown(download_link, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
