import base64
import pandas as pd
import streamlit as st
from datetime import datetime
import asyncio
import streamlit as st

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
    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")
    if st.button("Authenticate"):
        if authenticate(username, password):
            st.success("Authentication successful!")
            run_app()
        else:
            st.error("Authentication failed!")

def run_app():
    # Set the desired date for extraction
    user_date = datetime.strptime('12/05/2023', '%d/%m/%Y').date()

    # Call the extractor function to get the table data and header values
    table_data, header_values = extractor(user_date)

    # Convert the table_data list to a DataFrame
    df = pd.DataFrame(table_data, columns=header_values)

    # Display the DataFrame in the app
    st.title("ΕΓΔΙΧ - scraping app")
    st.dataframe(df)

    if st.button('Download'):
        st.markdown(download_dataframe(df), unsafe_allow_html=True)

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()  # I modified this from run_app to main
