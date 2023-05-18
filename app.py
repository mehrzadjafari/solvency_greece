import base64
import pandas as pd
import streamlit as st
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

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
    # Configure Chrome options for headless browsing
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")

    # Create a ChromeDriver instance with webdriver_manager
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # Call the extractor function with the provided driver and user date
    user_date = '12/05/2023'
    user_date = datetime.strptime(user_date, '%d/%m/%Y').date()
    table_data, header_values = extractor(driver, user_date)

    # Close the browser and stop the ChromeDriver service
    driver.quit()

    # Convert the table_data list to a DataFrame
    df = pd.DataFrame(table_data, columns=header_values)

    st.title("ΕΓΔΙΧ - scraping app")

    # show df in app
    st.dataframe(df)

    if st.button('Download'):
        st.markdown(download_dataframe(df), unsafe_allow_html=True)

if __name__ == "__main__":
    run_app()
