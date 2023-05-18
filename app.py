import base64
import pandas as pd
import streamlit as st
from datetime import datetime
import asyncio
from extractor import extractor

def authenticate(username, password):
    # Return True if authentication is successful, False otherwise
    return (username == st.secrets["USERNAME"] and password == st.secrets["PASSWORD"])

def download_dataframe(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV file</a>'
    return href

def main():
    # Authentication
    st.title("Authentication")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Authenticate"):
        if authenticate(username, password):
            st.success("Authentication successful!")
            run_app()
        else:
            st.error("Authentication failed!")

def run_app():
    # Call the extractor function with the user date
    user_date = '12/05/2023'
    user_date = datetime.strptime(user_date, '%d/%m/%Y').date()
    table_data, header_values = asyncio.run(extractor(user_date))

    # Convert the table_data list to a DataFrame
    df = pd.DataFrame(table_data, columns=header_values)

    st.title("ΕΓΔΙΧ - scraping app")

    # show df in app
    st.dataframe(df)

    if st.button('Download'):
        st.markdown(download_dataframe(df), unsafe_allow_html=True)

if __name__ == "__main__":
    main()  # I modified this from run_app to main
