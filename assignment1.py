import praw
import pandas as pd
import time
import yfinance as yf
import requests
import os

def fetch_reddit_data(subreddits, keywords, limit=5):
    reddit = praw.Reddit(
        client_id='VanokHdbJugVE2d1vSlIRg',
        client_secret='48k1fnKF7-2x8e0zHxRuz4X6YuaWuw',
        user_agent='EV Data Collector'
    )
    
    posts = []
    for subreddit in subreddits:
        for keyword in keywords:
            for submission in reddit.subreddit(subreddit).search(keyword, limit=limit):
                posts.append([
                    submission.title, submission.selftext, submission.author.name if submission.author else 'N/A',
                    submission.created_utc, submission.score, subreddit
                ])
                time.sleep(1)  
    
    df = pd.DataFrame(posts, columns=['title', 'text', 'author', 'date', 'upvotes', 'subreddit'])
    df['date'] = pd.to_datetime(df['date'], unit='s')
    os.makedirs("datasets/raw", exist_ok=True)
    df.to_csv("datasets/raw/reddit_posts.csv", index=False)
    print("Reddit data saved!")

def fetch_stock_data(tickers, period='1y', interval='1d'):
    stock_data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        df.to_csv(f"datasets/raw/{ticker}_stock.csv")
        stock_data[ticker] = df
        print(f"Stock data for {ticker} saved!")
    return stock_data

def fetch_public_dataset():
    url = "https://datahub.io/core/ev-sales/r/ev-sales.csv"  
    response = requests.get(url)
    if response.status_code == 200:
        os.makedirs("datasets/raw", exist_ok=True)
        with open("datasets/raw/ev_data.csv", 'wb') as f:
            f.write(response.content)
        print("Public dataset saved!")
    else:
        print("Failed to fetch public dataset")
def summarize_dataset(file_path):
    try:
        df = pd.read_csv(file_path)
        print(f"Summary statistics for {file_path}:")
        print(df.describe(include="all"))
        return df.describe(include="all")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
if __name__ == "__main__":
    subreddits = ["ElectricVehicles", "TeslaMotors"]
    keywords = ["electric vehicle", "Tesla", "EV charging"]
    stock_tickers = ["TSLA", "GM", "F", "NIO"] 
    f_stock_path: str = "datasets/raw/TSLA_stock.csv"
    GM_stock_path: str = "datasets/raw/GM_stock.csv"
    NIO_stock_path: str = "datasets/raw/NIO_stock.csv"
    reddit_posts_path: str = "datasets/raw/reddit_posts.csv"
    TSLA_stock_path: str = "datasets/raw/TSLA_stock.csv"
  
    fetch_reddit_data(subreddits, keywords)
    fetch_stock_data(stock_tickers)
    fetch_public_dataset()
    summarize_dataset(f_stock_path)
    summarize_dataset(GM_stock_path)
    summarize_dataset(NIO_stock_path)
    summarize_dataset(reddit_posts_path)
    summarize_dataset(TSLA_stock_path)
