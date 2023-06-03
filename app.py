import pandas as pd
import streamlit as st
from datetime import datetime, date
import jwt
from extractor import extractor, download_dataframe

def authenticate(username, password):
    # Return True if authentication is successful, False otherwise
    return (username == st.secrets["USERNAME"] and password == st.secrets["PASSWORD"])

@st.cache
def cached_extractor(user_date):
    # Call the extractor function to get the table data and header values
    return extractor(user_date)

def login():
    st.title("Login Page")
    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")

    if st.button("Authenticate"):
        if authenticate(username, password):
            token = jwt.encode({"username": username}, st.secrets["SECRET_KEY"], algorithm="HS256")
            st.experimental_set_query_params(token=token)
            st.experimental_rerun()
        else:
            st.error("Authentication failed!")

def content_page():
    st.title("MMEA Transofrmation")
    selected_date = st.date_input("Select a date", date.today())
    user_date = datetime.combine(selected_date, datetime.min.time()).date()
    
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

def main():
    # Get the current page from the query parameters
    query_params = st.experimental_get_query_params()
    token = query_params.get("token", [""])[0]
    decoded_token = None

    try:
        decoded_token = jwt.decode(token, st.secrets["SECRET_KEY"], algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        pass

    if decoded_token:
        content_page()
    else:
        login()

if __name__ == "__main__":
    main()
