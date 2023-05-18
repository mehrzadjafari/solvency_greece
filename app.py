import base64
import pandas as pd
import streamlit as st

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
    st.title("ΕΓΔΙΧ - Authentication")
    auth_flag = False  # Flag to track authentication state

    if st.button("Show Authentication"):
        auth_flag = True

    if auth_flag:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Authenticate"):
            if authenticate(username, password):
                st.success("Authentication successful!")
                run_app()
            else:
                st.error("Authentication failed!")

def run_app():
    st.title("ΕΓΔΙΧ - Scraping App")

    # read df from github
    github_data_path = "https://raw.githubusercontent.com/mehrzadjafari/solvency_greece/main/table_data.csv"
    df = pd.read_csv(github_data_path)

    # show df in app
    st.dataframe(df)

    if st.button('Download'):
        st.markdown(download_dataframe(df), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
