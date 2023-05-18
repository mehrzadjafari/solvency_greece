import base64
import pandas as pd
import streamlit as st

def authenticate(username, password):
    # Add your authentication logic here
    # Return True if authentication is successful, False otherwise
    return (username == "admin" and password == "admin")

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
    st.write("""
    # govgr web scraping app
    """)

    # read df from github
    df = pd.read_csv("https://raw.githubusercontent.com/mehrzadjafari/solvency_greece/main/table_data.csv?token=GHSAT0AAAAAACCI2H2RFTMHM3U4WLAI2MOWZDF6GNQ")

    # show df in app
    st.dataframe(df)

    if st.button('Download'):
        st.markdown(download_dataframe(df), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
