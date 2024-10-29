# Supplain Chain Relationship Web Scrapper
_QuickFS Integrated Supply Chain Relationship Web Scrapper_

## How It Works
Boyko Wealth utlizes https://csimarket.com as a reference for supplier relationships between the comapnies in our database. The relationships are scraped using BeautifulSoup4 and fuzzy matched through SequenceMatcher. Fuzzy matching is completed to convert QuickFS ID's to ticker symbols through matching tickers and names. The output provides a dataframe of all relationships.

## How To Use
Using the predefined main() function, a DataFrame can be created. For individual outputs, utilize the SPLC.output() function.
