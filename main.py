## Supply Chain WebScraper Function (SPLC)
## V1.0
## Brayden Boyko

## Import Libraries
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from difflib import SequenceMatcher as SM
import time


## Classes

class SPLC():

    def get(ticker):
        try:
            response = requests.get(f"https://csimarket.com/stocks/suppliers_glance.php?code={ticker}") ## GET HTML from site
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, 'html.parser') ## Display HTML source code
            return soup
        except requests.exceptions.RequestException as e:
            print(f"No Data For {ticker}: {e}")
            return None
        
    def table(ticker):
        tick = ticker  # Define Ticker as Tick (for naming conventions)

        # START - Find Table
        broth = SPLC.get(tick)  # Call get() function to fetch HTML

        # Check if the response was valid
        if broth is None:
            return pd.DataFrame(columns=['TICKER', 'NAME', 'REF'])

        broth = broth.find("table", {"class": "osnovna_tablica_bez_gifa"})
        if broth is None:
            return pd.DataFrame(columns=['TICKER', 'NAME', 'REF'])
        # END - Find Table

        # START - Find Name
        chicken = SPLC.get(tick)  # Call get() function to fetch HTML again
        if chicken is None:
            company_ref = ""
        else:
            chicken = chicken.find("span", {"class": "Naziv"})
            company_ref = chicken.get_text(strip=True) if chicken else ""
        # END - Find Name

        noodles = broth.find_all("a", {"class": "complin"})
        table = []

        # Iterate through each row and extract the data
        for link in noodles:
            company_name = link.get_text(strip=True)  # Get the text (company name)
            company_url = link['href']  # Get the URL
            ticker_code = company_url.split("code=")[1]  # Split the ticker out
            table.append((ticker_code, company_name, company_ref))  # Add Data To The Table

        table = pd.DataFrame(table, columns=['TICKER', 'NAME', 'REF'])
        return table

    def output(ticker):
        tick = ticker
        df_tick = SPLC.table(tick)  # Call table() function
        if df_tick.empty:
            return pd.DataFrame()

        # Read QuickFs Identifiers
        id_qfs = pd.read_feather("https://github.com/boykowealth/splc_webscraper/raw/refs/heads/main/Firm_List.feather")
        id_qfs = pd.DataFrame(id_qfs)

        # Merge scraped data with id_qfs
        merge = pd.merge(df_tick, id_qfs, how='left', on='TICKER')
        merge = merge[['TICKER', 'NAME_x', 'NAME_y', 'QFS ID', 'REF']]

        # Handle 'NA' values
        merge['NAME_x'] = merge['NAME_x'].astype(str).fillna('')
        merge['NAME_y'] = merge['NAME_y'].astype(str).fillna('')

        # Fuzzy match filter based on names
        merge['SCORE'] = merge.apply(lambda row: SM(None, row['NAME_x'], row['NAME_y']).ratio(), axis=1)
        merge = merge[merge['SCORE'] > 0.65]  # Keep rows with score > 0.65

        # Handle reference data
        merge['MATCH'] = ticker.upper()

        # Second merge based on 'MATCH'
        merge1 = pd.merge(merge, id_qfs, left_on='MATCH', right_on='TICKER')

        # Ensure 'NAME' and 'REF' are strings
        merge1['NAME'] = merge1['NAME'].astype(str)
        merge1['REF'] = merge1['REF'].astype(str)

        # Apply fuzzy matching on 'NAME' and 'REF'
        merge1['SCORE1'] = merge1.apply(
            lambda row: SM(None, row['NAME'], row['REF']).ratio() if pd.notnull(row['NAME']) and pd.notnull(row['REF']) else 0, axis=1
        )

        # Filter by second score threshold
        merge1 = merge1[merge1['SCORE1'] > 0.65]

        # Return required columns
        merge1 = merge1[['QFS ID_y', 'QFS ID_x', 'NAME_y']]
        merge1 = merge1.rename(columns={"QFS ID_y": "MATCH", "QFS ID_x": "QFS_ID", "NAME_y": "NAME"})
        print(merge1)

        return merge1


## MAIN
company_list = pd.read_feather('https://github.com/boykowealth/splc_webscraper/raw/refs/heads/main/Firm_List.feather')
company_list = pd.DataFrame(company_list)
# List of exchanges you want to filter by
exchanges = ['NYSE', 'NASDAQ', 'AMEX', 'BATS', 'ARCA', 'TSXV', 'CSE', 'TSX']
company_list = company_list[company_list['EXCHANGE ID'].isin(exchanges)]

def main():
    # TOTAL COUNT: 41611, NA COUNT: 14616 
    count = 0
    main_start_time = time.time()
    while count < 14616:
        start_time = time.time()
        ticker = company_list.iloc[count,1]
        if pd.isnull(ticker) or not isinstance(ticker, str):
            print(f"Skipping invalid ticker at index {count}")
            count += 1
            continue
        ticker = ticker.lower()
        data = SPLC.output(ticker)
        # Concatenate DataFrames
        if count == 0:
            table = data  # First DataFrame
        else:
            table = pd.concat([table, data], ignore_index=True)
        end_time = round(time.time() - start_time,2)
        print(ticker,"---",end_time)
        count = count + 1
    else:
        data_splc = pd.DataFrame(table)
        main_end_time = time.time()
        print("Webscrape Completed In", round((main_end_time-main_start_time)/3600,2),"hours")
        return data_splc

print(main())
