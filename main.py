import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from extractor import extractor

# Configure Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Create an instance of the ChromeDriver with headless options
driver = webdriver.Chrome(options=chrome_options)

# Call the extractor function with the provided driver and user date
user_date = input('Enter the date:\nExample: 01/05/2023\n\n->  ')
user_date = datetime.strptime(user_date, '%d/%m/%Y').date()
table_data, header_values = extractor(driver, user_date)

# Close the browser
driver.quit()

# Convert the table_data list to a DataFrame
data = pd.DataFrame(table_data, columns=header_values)
# print(data)

# Save the data to a CSV file
data.to_csv("C:/Users/engme/pyenv/my_notebooks/VS Code/AZTrade/table_data.csv", index=False)