import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import streamlit as st

@st.cache
def extractor(driver, user_date):
    # Configure Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Create an instance of the ChromeDriver with headless options
    driver = webdriver.Chrome(options=chrome_options)
    # Navigate to the website
    driver.get("https://keyd.gsis.gr/dsae2/iif/faces/pages/static/publicationList.xhtml#")

    # Find the select element
    wait = WebDriverWait(driver, 10)
    select_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'select.ui-paginator-rpp-options')))

    # Create a Select object and select the desired option
    select = Select(select_element)
    select.select_by_value('100')

    # Wait for a brief period for the changes to take effect
    time.sleep(2)

    # Find the table headers
    table_headers = driver.find_elements(By.CSS_SELECTOR, "thead[id='publicationListForm:publicationListDataTable_head'] th")
    header_values = [header.text for header in table_headers]

    # Initialize an empty list to store the table data
    table_data = []

    i = 0
    # Initialize an empty list to store the table data
    table_data = []

    # Counter for consecutive out of range dates
    out_of_range_counter = 0

    # Extract data from each page until reaching the beginning of 2023
    while i < 30:
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"tr[data-ri='{(i * 100)}']")))
        # Find the table element
        table_element = driver.find_element(By.CSS_SELECTOR, "table[role='grid']")

        # Find the table rows
        table_rows = table_element.find_elements(By.TAG_NAME, "tr")

        # Iterate over the rows
        for row in table_rows:
            try:
                # Find the table cells for each row
                table_cells = row.find_elements(By.TAG_NAME, "td")

                # Check if the row has enough cells
                if len(table_cells) > 7:
                    # Process the 8th cell
                    cell8 = table_cells[7]
                    try:
                        # Extract the value directly from the page source
                        div_element = cell8.find_element(By.CSS_SELECTOR, "div.ui-overlaypanel-content")
                        textarea_element = div_element.find_element(By.TAG_NAME, "textarea")
                        cell8_value = textarea_element.get_attribute("value")
                    except NoSuchElementException:
                        cell8_value = "NA"

                    # Extract the date from the 10th column
                    date_str = table_cells[9].get_attribute("innerHTML").strip()
                    date = datetime.strptime(date_str, "%d/%m/%Y").date()

                    # Check if date is within the desired range
                    if date >= user_date:
                        out_of_range_counter = 0  # Reset the counter

                        # Extract the desired data from the row
                        row_data = [cell.text.strip() for cell in table_cells]
                        row_data[7] = cell8_value  # Update the value of the 8th cell

                        # Append the row_data to the table_data list
                        table_data.append(row_data)
                    else:
                        out_of_range_counter += 1  # Increment the counter
                        if out_of_range_counter == 5:  # Check if the counter reached the limit
                            break
            except StaleElementReferenceException:
                # Handle StaleElementReferenceException by re-finding the table element and rows
                table_element = driver.find_element(By.CSS_SELECTOR, "table[role='grid']")
                table_rows = table_element.find_elements(By.TAG_NAME, "tr")

        if out_of_range_counter == 5:  # Check if the counter reached the limit
            break

        # Scroll to the next page element to bring it into view
        next_page_element = driver.find_element(By.CSS_SELECTOR, "a.ui-paginator-next")
        driver.execute_script("arguments[0].scrollIntoView();", next_page_element)

        # Click on the next page element
        driver.execute_script("arguments[0].click();", next_page_element)

        # Wait for a brief period for the next page to load
        time.sleep(2)

        # Scroll to the top of the page
        driver.execute_script("window.scrollTo(0, 0)")
        i += 1

    # Close the browser
    driver.quit()

    return table_data, header_values
