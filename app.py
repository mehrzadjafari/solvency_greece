import base64
import pandas as pd
import streamlit as st
from datetime import datetime, date
import streamlit as st
import io

from extractor import extractor, download_dataframe

def main():
    # Create two columns
    col1, col2, col3 = st.columns([1, 2, 1])

    # Center-align the title
    col2.markdown("<h1 style='text-align: center;'>MMEA Transformation</h1>", unsafe_allow_html=True)
    selected_date = st.date_input("From this date", date.today())
    user_date = datetime.combine(selected_date, datetime.min.time()).date()
#     username = st.text_input("Username", key="username_input")
#     password = st.text_input("Password", type="password", key="password_input")
#     if st.button("Authenticate"):
#         if authenticate(username, password):
#             st.success("Authentication successful!")
    run_app(user_date)
#         else:
#             st.error("Authentication failed!")
    


def run_app(user_date):

    # Call the cached_extractor function to get the table data and header values
    table_data, header_values = extractor(user_date)

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
