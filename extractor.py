import asyncio
from pyppeteer import launch
from datetime import datetime

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

# Run the async function
table_data, header_values = asyncio.get_event_loop().run_until_complete(extractor(datetime.strptime('12/05/2023', '%d/%m/%Y').date()))
