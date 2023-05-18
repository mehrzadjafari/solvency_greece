import pandas as pd
from datetime import datetime
from extractor2 import extractor
import asyncio

# Call the extractor function with the provided user date
user_date = '12/05/2023'
user_date = datetime.strptime(user_date, '%d/%m/%Y').date()

# Run the extractor function and get the table data
table_data, header_values = asyncio.get_event_loop().run_until_complete(extractor(user_date))

# Convert the table_data list to a DataFrame
data = pd.DataFrame(table_data, columns=header_values)

# Save the data to a CSV file
data.to_csv("table_data2.csv", index=False)
