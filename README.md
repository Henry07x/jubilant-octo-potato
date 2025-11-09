# Stock and Market Economics Data Scraper

A comprehensive Python scraper for stocks, market economics, and alternative data sources. This tool provides access to:

- **Real-time and historical stock price data**
- **Fundamental data** (revenue, profits, valuation ratios)
- **Company news, SEC filings, and management commentary**
- **Economic data** via FRED API (interest rates, GDP, unemployment, etc.)
- **Alternative data** (short interest, institutional holdings, etc.)

## Features

### Stock Data
- Real-time quotes
- Historical price data (OHLCV)
- Intraday data
- Options chain data
- Multiple stock comparison

### Fundamental Data
- Income statements (annual and quarterly)
- Balance sheets
- Cash flow statements
- Valuation ratios (P/E, P/B, EV/EBITDA, etc.)
- Revenue and profit trends
- Key financial metrics

### News & SEC Filings
- Company news articles
- SEC filings (10-K, 10-Q, 8-K, etc.)
- Earnings call information
- Analyst recommendations

### Economic Data (FRED)
- GDP, unemployment, inflation
- Interest rates (Fed Funds, Treasury yields)
- Money supply, industrial production
- Custom series search
- Release observations (supports pagination with next_cursor)

### Alternative Data
- Short interest data
- Institutional holdings
- Major shareholders
- Web traffic estimates (placeholder for API integration)
- Social media sentiment (placeholder for API integration)

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up API keys in a `.env` file:
```
FRED_API_KEY=your_fred_api_key_here
```

You can get a free FRED API key at: https://fred.stlouisfed.org/docs/api/api_key.html

## Usage

### Command Line Interface

#### Stock Price Data
```bash
# Get real-time quote
python main.py stock --symbol AAPL --quote

# Get historical data (1 year)
python main.py stock --symbol AAPL --period 1y

# Get historical data with date range
python main.py stock --symbol AAPL --start-date 2023-01-01 --end-date 2023-12-31

# Get intraday data
python main.py stock --symbol AAPL --intraday

# Save to CSV
python main.py stock --symbol AAPL --period 1y --output aapl_data.csv
```

#### FRED Economic Data
```bash
# Get GDP data
python main.py fred --series GDP --start-date 2020-01-01

# Get unemployment rate
python main.py fred --series UNEMPLOYMENT --start-date 2020-01-01

# Get release observations (e.g., release ID 52)
python main.py fred --release-id 52

# Search for series
python main.py fred --search "interest rate"

# Save to CSV
python main.py fred --series GDP --output gdp_data.csv
```

#### Fundamental Data
```bash
# Get all financial statements
python main.py fundamental --symbol AAPL

# Get valuation ratios
python main.py fundamental --symbol AAPL --ratios

# Get key metrics
python main.py fundamental --symbol AAPL --metrics

# Get revenue/profit trend
python main.py fundamental --symbol AAPL --trend
```

#### News
```bash
# Get company news
python main.py news --symbol AAPL --limit 10

# Save to CSV
python main.py news --symbol AAPL --output aapl_news.csv
```

#### SEC Filings
```bash
# Get all SEC filings
python main.py sec --symbol AAPL --limit 10

# Get specific filing type
python main.py sec --symbol AAPL --filing-type 10-K --limit 5
```

#### Alternative Data
```bash
# Get short interest
python main.py alternative --symbol AAPL --short-interest

# Get institutional holdings
python main.py alternative --symbol AAPL --institutional
```

### Python API

You can also use the scrapers programmatically:

```python
from scraper import StockScraper, FREDClient, FundamentalScraper, NewsScraper

# Stock data
stock_scraper = StockScraper()
quote = stock_scraper.get_real_time_quote('AAPL')
historical = stock_scraper.get_historical_data('AAPL', period='1y')

# Economic data
fred = FREDClient(api_key='your_key')
gdp = fred.get_series('GDP', start_date='2020-01-01')

# Get release observations with pagination
release_data = fred.get_release_observations(release_id=52)
# Use next_cursor for pagination
if 'next_cursor' in release_data:
    next_page = fred.get_release_observations(release_id=52, next_cursor=release_data['next_cursor'])

# Fundamental data
fundamental = FundamentalScraper()
ratios = fundamental.get_valuation_ratios('AAPL')
metrics = fundamental.get_key_metrics('AAPL')

# News
news = NewsScraper()
articles = news.get_company_news('AAPL', limit=10)
filings = news.get_sec_filings('AAPL', limit=5)
```

## Available FRED Series

The scraper includes common FRED series IDs:
- `GDP` - Gross Domestic Product
- `UNEMPLOYMENT` - Unemployment Rate
- `FED_FUNDS_RATE` - Federal Funds Rate
- `CPI` - Consumer Price Index
- `DOW_JONES` - Dow Jones Industrial Average
- `S_P_500` - S&P 500
- `TREASURY_10Y` - 10-Year Treasury Rate
- `TREASURY_2Y` - 2-Year Treasury Rate
- `MONEY_SUPPLY_M2` - M2 Money Supply
- `INDUSTRIAL_PRODUCTION` - Industrial Production Index

## FRED API Pagination

The FRED client supports pagination for release observations using the `next_cursor` parameter:

```python
fred = FREDClient(api_key='your_key')

# Get first page
data = fred.get_release_observations(release_id=52)

# Get next page using cursor from previous response
# The cursor format is like: "ABSITCMDODFS,1995-01-01"
next_data = fred.get_release_observations(release_id=52, next_cursor="ABSITCMDODFS,1995-01-01")
```

## Data Sources

- **Stock Data**: Yahoo Finance (via yfinance)
- **Economic Data**: FRED API (Federal Reserve Economic Data)
- **News**: Yahoo Finance news feed
- **SEC Filings**: SEC EDGAR database
- **Fundamental Data**: Yahoo Finance

## Notes

- Some features (web traffic, social sentiment) require additional API integrations
- Rate limits may apply to free APIs
- SEC filings scraping may be rate-limited; use responsibly
- Always verify data accuracy before making investment decisions
- FRED API supports pagination via `next_cursor` for large datasets

## Requirements

- Python 3.7+
- See `requirements.txt` for full list of dependencies

## License

This project is provided as-is for educational and research purposes.

## Disclaimer

This tool is for informational purposes only. It does not provide financial advice. Always do your own research and consult with financial professionals before making investment decisions.

