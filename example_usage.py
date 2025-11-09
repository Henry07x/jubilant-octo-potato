"""
Example usage of the Stock and Market Economics Data Scraper
"""
from dotenv import load_dotenv
from scraper import (
    FREDClient, FRED_SERIES,
    StockScraper,
    FundamentalScraper,
    NewsScraper,
    AlternativeDataScraper
)

load_dotenv()


def example_stock_data():
    """Example: Get stock price data"""
    print("\n" + "="*60)
    print("STOCK DATA EXAMPLE")
    print("="*60)
    
    scraper = StockScraper()
    
    # Get real-time quote
    print("\n1. Real-time Quote for AAPL:")
    quote = scraper.get_real_time_quote('AAPL')
    print(f"   Current Price: ${quote['current_price']}")
    print(f"   Market Cap: ${quote['market_cap']:,}")
    
    # Get historical data
    print("\n2. Historical Data (last 5 days):")
    historical = scraper.get_historical_data('AAPL', period='5d')
    print(historical[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].tail())


def example_fred_data():
    """Example: Get FRED economic data"""
    print("\n" + "="*60)
    print("FRED ECONOMIC DATA EXAMPLE")
    print("="*60)
    
    # API key is automatically loaded from .env file or environment variable
    fred = FREDClient()  # Will use FRED_API_KEY from .env if available
    
    # Get GDP data
    print("\n1. GDP Data (last 5 years):")
    gdp = fred.get_series('GDP', start_date='2019-01-01')
    if not gdp.empty:
        print(gdp.tail())
    
    # Get release observations (example with release_id=52)
    print("\n2. Release Observations (Release ID 52):")
    release_data = fred.get_release_observations(release_id=52, limit=10)
    if not release_data.empty:
        print(release_data.head(10))
    
    # Example with pagination
    print("\n3. Pagination Example:")
    print("   First page:")
    page1 = fred.get_release_observations(release_id=52, limit=5)
    if not page1.empty:
        print(f"   Retrieved {len(page1)} observations")
        print("   To get next page, use:")
        print("   page2 = fred.get_release_observations(release_id=52, next_cursor='ABSITCMDODFS,1995-01-01')")


def example_fundamental_data():
    """Example: Get fundamental data"""
    print("\n" + "="*60)
    print("FUNDAMENTAL DATA EXAMPLE")
    print("="*60)
    
    scraper = FundamentalScraper()
    
    # Get valuation ratios
    print("\n1. Valuation Ratios for AAPL:")
    ratios = scraper.get_valuation_ratios('AAPL')
    print(f"   P/E Ratio: {ratios.get('pe_ratio')}")
    print(f"   Price to Book: {ratios.get('price_to_book')}")
    print(f"   Market Cap: ${ratios.get('market_cap'):,}")
    
    # Get key metrics
    print("\n2. Key Metrics for AAPL:")
    metrics = scraper.get_key_metrics('AAPL')
    print(f"   Revenue: ${metrics.get('revenue'):,}")
    print(f"   Profit Margin: {metrics.get('profit_margin')}%")
    print(f"   ROE: {metrics.get('return_on_equity')}")


def example_news_data():
    """Example: Get news and SEC filings"""
    print("\n" + "="*60)
    print("NEWS AND SEC FILINGS EXAMPLE")
    print("="*60)
    
    scraper = NewsScraper()
    
    # Get company news
    print("\n1. Recent News for AAPL (first 3 articles):")
    news = scraper.get_company_news('AAPL', limit=3)
    if not news.empty:
        for idx, row in news.iterrows():
            print(f"   {idx+1}. {row['title']}")
            print(f"      Published: {row['published_date']}")
            print(f"      Link: {row['link']}\n")
    
    # Get SEC filings
    print("\n2. Recent SEC Filings for AAPL:")
    filings = scraper.get_sec_filings('AAPL', limit=3)
    if not filings.empty:
        for idx, row in filings.iterrows():
            print(f"   {idx+1}. {row['filing_type']}: {row['title']}")
            print(f"      Published: {row['published']}\n")


def example_alternative_data():
    """Example: Get alternative data"""
    print("\n" + "="*60)
    print("ALTERNATIVE DATA EXAMPLE")
    print("="*60)
    
    scraper = AlternativeDataScraper()
    
    # Get short interest
    print("\n1. Short Interest for AAPL:")
    short_interest = scraper.get_short_interest('AAPL')
    print(f"   Short Ratio: {short_interest.get('short_ratio')}")
    print(f"   Short % of Float: {short_interest.get('short_percent_of_float')}")
    
    # Get institutional holdings
    print("\n2. Top Institutional Holders for AAPL:")
    institutional = scraper.get_institutional_holdings('AAPL')
    if not institutional.empty:
        print(institutional.head(5))


if __name__ == '__main__':
    print("\n" + "="*60)
    print("STOCK AND MARKET ECONOMICS DATA SCRAPER")
    print("EXAMPLE USAGE")
    print("="*60)
    
    try:
        example_stock_data()
        example_fred_data()
        example_fundamental_data()
        example_news_data()
        example_alternative_data()
        
        print("\n" + "="*60)
        print("Examples completed successfully!")
        print("="*60)
        print("\nFor more information, see README.md")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()

