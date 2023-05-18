import base64
import pandas as pd
import streamlit as st
from datetime import datetime
import asyncio
from pyppeteer import launch
import nest_asyncio
nest_asyncio.apply()

async def extractor(user_date):

    browser = await launch()
    page = await browser.newPage()
    await page.goto("https://keyd.gsis.gr/dsae2/iif/faces/pages/static/publicationList.xhtml#")

    await page.select('select.ui-paginator-rpp-options', '100')
    await asyncio.sleep(2)

    table_headers = await page.querySelectorAll("thead[id='publicationListForm:publicationListDataTable_head'] th")
    header_values = [await page.evaluate('(element) => element.textContent', header) for header in table_headers]

    table_data = []
    i = 0
    out_of_range_counter = 0

    while i < 30:
        rows = await page.querySelectorAll("table[role='grid'] tr")
        for row in rows:
            try:
                cells = await row.querySelectorAll('td')
                if len(cells) > 7:
                    try:
                        cell8 = await cells[7].querySelector('div.ui-overlaypanel-content textarea')
                        cell8_value = await page.evaluate('(element) => element.value', cell8)
                    except:
                        cell8_value = "NA"

                    date_str = await page.evaluate('(element) => element.innerHTML', cells[9])
                    date_str = date_str.strip()
                    date = datetime.strptime(date_str, "%d/%m/%Y").date()

                    if date >= user_date:
                        out_of_range_counter = 0
                        row_data = [await page.evaluate('(element) => element.textContent', cell) for cell in cells]
                        row_data[7] = cell8_value
                        table_data.append(row_data)
                    else:
                        out_of_range_counter += 1
                        if out_of_range_counter == 5:
                            break
            except Exception as e:
                print(f"Error: {e}")

        if out_of_range_counter == 5:
            break

        next_page = await page.querySelector('a.ui-paginator-next')
        await next_page.click()
        await asyncio.sleep(2)
        i += 1

    await browser.close()
    return table_data, header_values

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
    table_data, header_values = asyncio.get_event_loop().run_until_complete(extractor(user_date))

    # Convert the table_data list to a DataFrame
    df = pd.DataFrame(table_data, columns=header_values)

    st.title("ΕΓΔΙΧ - scraping app")

    # show df in app
    st.dataframe(df)

    if st.button('Download'):
        st.markdown(download_dataframe(df), unsafe_allow_html=True)

if __name__ == "__main__":
    main()  # I modified this from run_app to main
