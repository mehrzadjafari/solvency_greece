import base64
import pandas as pd
import streamlit as st
from datetime import datetime, date
import streamlit as st
import io

from extractor import extractor, download_dataframe

def creds_entered():
    if st.session_state['user'].strip() == st.secrets["USERNAME"] and st.session_state["passwd"].strip() == st.secrets["PASSWORD"]:
        st.session_state['authenticated'] = True
    else:
        st.session_state['authenticated'] = False
        st.error("Invalid Username/Password!👀")


def authenticate_user():
    if 'authenticated' not in st.session_state:
        st.text_input(label="Username", value="", key="user", on_change=creds_entered)
        st.text_input(label="Password", type="password", key="passwd", on_change=creds_entered)
        return False
    else:
        if st.session_state['authenticated']:
            return True
        else:
            st.text_input(label="Username", value="", key="user", on_change=creds_entered)
            st.text_input(label="Password", type="password", key="passwd", on_change=creds_entered)
            return False


if authenticate_user():
    st.title("MMEA Transformation")
    selected_date = st.date_input("From date", date.today())
    user_date = datetime.combine(selected_date, datetime.min.time()).date()
    run_app(user_date)
    


def run_app(user_date):

    # Call the cached_extractor function to get the table data and header values
    table_data, header_values = extractor(user_date)

    # Convert the table_data list to a DataFrame
    df = pd.DataFrame(table_data, columns=header_values)

    # Display the DataFrame in the app
    st.title("ΕΓΔΙΧ - Scraping Application")
    st.dataframe(df)

    if st.button('Download'):
        download_link = download_dataframe(df, user_date)
        st.markdown(download_link, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
