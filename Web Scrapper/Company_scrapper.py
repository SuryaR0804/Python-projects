from bs4 import BeautifulSoup
import pandas as pd
import requests

#Extract Website
url = "https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue"
headers = {"User-Agent": "MyScraperApp/1.0 (contact@example.com)"}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")
 
table = soup.find_all("table")[0]      #extract necessary table


#Extract Column Headings
header_row = table.find("tr")

world_table_titles = [
    title.text.strip() for title in header_row.find_all("th")
]


#Extract Table Data
column_data = table.find_all("tr")
scraped_data = []

#tracker dictionary for active rowspans
rowspan_tracker = {}

#table rows past the header
for row in column_data[2:]:
  row_cells = row.find_all(["th", "td"])

  if not row_cells:
    continue

  full_row = []
  cell_idx = 0  #Pointer for HTML cells present in this row

  #excluding state owned and refernces column
  for col_idx in range(7):
    #Case A: Check if this column position is currently active in a previous rowspan
    if col_idx in rowspan_tracker:
      value, remaining = rowspan_tracker[col_idx]
      full_row.append(value)

      #Decrement counter or remove if expired
      if remaining - 1 > 0:
        rowspan_tracker[col_idx] = (value, remaining - 1)
      else:
        del rowspan_tracker[col_idx]

    #Case B: Standard cell extraction from HTML
    elif cell_idx < len(row_cells):
      cell = row_cells[cell_idx]
      text = cell.text.strip()
      full_row.append(text)

      #Check if this cell initiates a new rowspan
      rowspan = int(cell.get("rowspan", 1))
      if rowspan > 1:
        rowspan_tracker[col_idx] = (text, rowspan - 1)

      cell_idx += 1

  #Add fully reconstructed row
  if full_row:
    scraped_data.append(full_row)


#Build & Clean Pandas DataFrame
df = pd.DataFrame(scraped_data, columns=world_table_titles[:7])

df = df.rename(
    columns={
        "Revenue": "Revenue (USD Billions)",
        "Profit": "Profit (USD Billions)",
        "Headquarters[note 1]": "Headquarters",
    }
)

#Display result and csv file creation, change your location as per requirement
df.to_csv(r"C:\Users\USER\Documents\8142\data scrapper\Largest_Companies.csv", index=False)
print(df)
