"""
Main CLI interface for the Stock and Market Economics Data Scraper
"""
import argparse
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from scraper import (
    FREDClient, FRED_SERIES,
    StockScraper,
    FundamentalScraper,
    NewsScraper,
    AlternativeDataScraper
)

load_dotenv()


def print_dataframe(df: pd.DataFrame, title: str = ""):
    """Pretty print a DataFrame"""
    if title:
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"{'='*60}")
    
    if df.empty:
        print("No data available.")
        return
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    print(df.to_string(index=False))
    print(f"\nRows: {len(df)}")


def main():
    parser = argparse.ArgumentParser(
        description='Stock and Market Economics Data Scraper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get stock price data
  python main.py stock --symbol AAPL --period 1y
  
  # Get real-time quote
  python main.py stock --symbol AAPL --quote
  
  # Get economic data from FRED
  python main.py fred --series GDP --start-date 2020-01-01
  
  # Get fundamental data
  python main.py fundamental --symbol AAPL
  
  # Get company news
  python main.py news --symbol AAPL --limit 10
  
  # Get SEC filings
  python main.py sec --symbol AAPL --limit 5
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Stock price data
    stock_parser = subparsers.add_parser('stock', help='Get stock price data')
    stock_parser.add_argument('--symbol', required=True, help='Stock ticker symbol')
    stock_parser.add_argument('--quote', action='store_true', help='Get real-time quote')
    stock_parser.add_argument('--period', default='1y', help='Period for historical data')
    stock_parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    stock_parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    stock_parser.add_argument('--intraday', action='store_true', help='Get intraday data')
    stock_parser.add_argument('--output', help='Output file path (CSV)')
    
    # FRED economic data
    fred_parser = subparsers.add_parser('fred', help='Get FRED economic data')
    fred_parser.add_argument('--series', help='FRED series ID (e.g., GDP, UNRATE)')
    fred_parser.add_argument('--release-id', type=int, help='FRED release ID')
    fred_parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    fred_parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    fred_parser.add_argument('--search', help='Search for series')
    fred_parser.add_argument('--output', help='Output file path (CSV)')
    
    # Fundamental data
    fundamental_parser = subparsers.add_parser('fundamental', help='Get fundamental data')
    fundamental_parser.add_argument('--symbol', required=True, help='Stock ticker symbol')
    fundamental_parser.add_argument('--ratios', action='store_true', help='Get valuation ratios')
    fundamental_parser.add_argument('--metrics', action='store_true', help='Get key metrics')
    fundamental_parser.add_argument('--trend', action='store_true', help='Get revenue/profit trend')
    fundamental_parser.add_argument('--output', help='Output file path (CSV)')
    
    # News and SEC filings
    news_parser = subparsers.add_parser('news', help='Get company news')
    news_parser.add_argument('--symbol', required=True, help='Stock ticker symbol')
    news_parser.add_argument('--limit', type=int, default=20, help='Number of articles')
    news_parser.add_argument('--output', help='Output file path (CSV)')
    
    sec_parser = subparsers.add_parser('sec', help='Get SEC filings')
    sec_parser.add_argument('--symbol', required=True, help='Stock ticker symbol')
    sec_parser.add_argument('--filing-type', help='Filing type (10-K, 10-Q, 8-K, etc.)')
    sec_parser.add_argument('--limit', type=int, default=20, help='Number of filings')
    sec_parser.add_argument('--output', help='Output file path (CSV)')
    
    # Alternative data
    alt_parser = subparsers.add_parser('alternative', help='Get alternative data')
    alt_parser.add_argument('--symbol', required=True, help='Stock ticker symbol')
    alt_parser.add_argument('--short-interest', action='store_true', help='Get short interest')
    alt_parser.add_argument('--institutional', action='store_true', help='Get institutional holdings')
    alt_parser.add_argument('--output', help='Output file path (CSV)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Stock price data
        if args.command == 'stock':
            scraper = StockScraper()
            
            if args.quote:
                quote = scraper.get_real_time_quote(args.symbol)
                print_dataframe(pd.DataFrame([quote]), f"Real-time Quote: {args.symbol}")
                data = pd.DataFrame([quote])
            elif args.intraday:
                data = scraper.get_intraday_data(args.symbol)
                print_dataframe(data, f"Intraday Data: {args.symbol}")
            else:
                data = scraper.get_historical_data(
                    args.symbol,
                    args.start_date,
                    args.end_date,
                    args.period
                )
                print_dataframe(data, f"Historical Data: {args.symbol}")
            
            if args.output:
                data.to_csv(args.output, index=False)
                print(f"\nData saved to {args.output}")
        
        # FRED economic data
        elif args.command == 'fred':
            api_key = os.getenv('FRED_API_KEY')
            fred = FREDClient(api_key=api_key)
            
            if args.search:
                data = fred.search_series(args.search)
                print_dataframe(data, f"FRED Series Search: {args.search}")
            elif args.release_id:
                data = fred.get_release_observations(args.release_id)
                print_dataframe(data, f"FRED Release {args.release_id}")
            elif args.series:
                series_id = FRED_SERIES.get(args.series.upper(), args.series)
                data = fred.get_series(series_id, args.start_date, args.end_date)
                print_dataframe(data, f"FRED Series: {series_id}")
            else:
                print("Please specify --series, --release-id, or --search")
                return
            
            if args.output and not data.empty:
                data.to_csv(args.output, index=False)
                print(f"\nData saved to {args.output}")
        
        # Fundamental data
        elif args.command == 'fundamental':
            scraper = FundamentalScraper()
            
            if args.ratios:
                ratios = scraper.get_valuation_ratios(args.symbol)
                print_dataframe(pd.DataFrame([ratios]), f"Valuation Ratios: {args.symbol}")
                if args.output:
                    pd.DataFrame([ratios]).to_csv(args.output, index=False)
            elif args.metrics:
                metrics = scraper.get_key_metrics(args.symbol)
                print_dataframe(pd.DataFrame([metrics]), f"Key Metrics: {args.symbol}")
                if args.output:
                    pd.DataFrame([metrics]).to_csv(args.output, index=False)
            elif args.trend:
                trend = scraper.get_revenue_profit_trend(args.symbol)
                print_dataframe(trend, f"Revenue/Profit Trend: {args.symbol}")
                if args.output:
                    trend.to_csv(args.output, index=False)
            else:
                financials = scraper.get_financials(args.symbol)
                print(f"\n{'='*60}")
                print(f"Financial Statements: {args.symbol}")
                print(f"{'='*60}")
                for key, value in financials.items():
                    if isinstance(value, pd.DataFrame) and not value.empty:
                        print(f"\n{key.upper().replace('_', ' ')}:")
                        print(value.to_string())
        
        # News
        elif args.command == 'news':
            scraper = NewsScraper()
            news = scraper.get_company_news(args.symbol, args.limit)
            print_dataframe(news, f"Company News: {args.symbol}")
            
            if args.output:
                news.to_csv(args.output, index=False)
                print(f"\nData saved to {args.output}")
        
        # SEC filings
        elif args.command == 'sec':
            scraper = NewsScraper()
            filings = scraper.get_sec_filings(args.symbol, args.filing_type, args.limit)
            print_dataframe(filings, f"SEC Filings: {args.symbol}")
            
            if args.output:
                filings.to_csv(args.output, index=False)
                print(f"\nData saved to {args.output}")
        
        # Alternative data
        elif args.command == 'alternative':
            scraper = AlternativeDataScraper()
            
            if args.short_interest:
                data = scraper.get_short_interest(args.symbol)
                print_dataframe(pd.DataFrame([data]), f"Short Interest: {args.symbol}")
                if args.output:
                    pd.DataFrame([data]).to_csv(args.output, index=False)
            elif args.institutional:
                data = scraper.get_institutional_holdings(args.symbol)
                print_dataframe(data, f"Institutional Holdings: {args.symbol}")
                if args.output:
                    data.to_csv(args.output, index=False)
            else:
                print("Please specify --short-interest or --institutional")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

