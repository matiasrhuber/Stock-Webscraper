SEC Webscraper README
=======================================================================================

Overview

The SEC Webscraper is a Python-based tool designed to extract financial and regulatory information from SEC filings. It automates the process of retrieving and parsing filings to facilitate financial analysis and compliance monitoring.

Features

Scrapes SEC EDGAR database for filings

Extracts key financial and regulatory information

Supports multiple filing types (e.g., 10-K, 10-Q, 8-K)

Outputs data in structured formats (CSV, JSON)

Configurable filters for specific companies and filing dates

Requirements

Python 3.x

requests

BeautifulSoup4

pandas

Install dependencies using:

pip install requests beautifulsoup4 pandas

Usage

Run the script with:

python sec_webscraper.py --ticker AAPL --filing 10-K --year 2023

Command-line Arguments

--ticker : Stock ticker symbol (e.g., AAPL, MSFT)

--filing : Filing type (e.g., 10-K, 10-Q)

--year : Year of the filing

Output

The extracted data is saved as a structured JSON or CSV file in the output/ directory.

License

This project is licensed under the MIT License.

Contributing

Pull requests and feature suggestions are welcome!



        make html
        make latexpdf
