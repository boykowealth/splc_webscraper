# Supplain Chain Relationship Web Scrapper
_QuickFS Integrated Supply Chain Relationship Web Scrapper_

## How It Works
Boyko Wealth utlizes https://csimarket.com as a reference for supplier relationships between the comapnies in our database. The relationships are scraped using BeautifulSoup4 and fuzzy matched through SequenceMatcher. Fuzzy matching is completed to convert QuickFS ID's to ticker symbols through matching tickers and names. The output provides a dataframe of all relationships.

## Boyko Wealth Supply Chain WebScraper (SPLC) V1.0

The *Supply Chain WebScraper Function (SPLC)* is a custom Python script developed by Boyko Wealth to automate the extraction and matching of supplier information for various companies listed on major exchanges. By leveraging web scraping techniques, Boyko Wealth aims to provide deeper supply chain insights, enhancing investment analysis through a better understanding of corporate supply networks.

### Key Features of SPLC V1.0
- **Automated Data Retrieval**: Pulls supplier data directly from *csimarket.com* based on a company's stock ticker symbol, providing up-to-date supply chain visibility.
- **Fuzzy Matching for Data Accuracy**: Uses advanced fuzzy matching techniques to merge and verify supplier data against internal reference datasets, ensuring high accuracy in matching suppliers to specific companies.
- **Customizable Exchange Filtering**: Filters company lists by chosen exchanges (e.g., NYSE, NASDAQ), allowing Boyko Wealth to target data extraction based on preferred market segments.
- **Optimized Performance**: Built to handle large datasets efficiently, this script incorporates error handling and time tracking to monitor performance, ideal for Boyko Wealth’s high-throughput data needs.

### About Boyko Wealth
At Boyko Wealth, we recognize that understanding supply chain dynamics is essential for robust investment strategies. This SPLC web scraper is one of our key tools for enriching financial models with supply chain insights, reinforcing our commitment to high-quality data integration and advanced analytics.

For more information, visit [boykowealth.com](https://boykowealth.com).

