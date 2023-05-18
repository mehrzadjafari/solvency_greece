import base64
import pandas as pd
import streamlit as st
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Specify the path to the ChromeDriver executable
    driver_path = "https://raw.githubusercontent.com/mehrzadjafari/solvency_greece/main/chromedriver.exe"

    # Create an instance of the ChromeDriver with headless options
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

    # Call the extractor function with the provided driver and user date
    user_date = '12/05/2023'
    user_date = datetime.strptime(user_date, '%d/%m/%Y').date()
    table_data, header_values = extractor(driver, user_date)

    # Close the browser
    driver.quit()

    # Convert the table_data list to a DataFrame
    df = pd.DataFrame(table_data, columns=header_values)

    st.title("ΕΓΔΙΧ - scraping app")

    # show df in app
    st.dataframe(df)

    if st.button('Download'):
        st.markdown(download_dataframe(df), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
