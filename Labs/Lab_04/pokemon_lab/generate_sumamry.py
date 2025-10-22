
#!/usr/bin/env python3
import os
import sys
import pandas as pd

def generate_summary(portfolio_file: str) -> None:
    if not os.path.exists(portfolio_file):
        print(f"Error: File '{portfolio_file}' not found.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(portfolio_file)

    if df.empty:
        print("The portfolio file is empty. Nothing to summarize.")
        return
    total_portfolio_value = df["card_market_value"].sum()
    most_valuable_card = df.loc[df["card_market_value"].idxmax()]
    print(f"Total Value: ${total_portfolio_value:.2f} | Most Valuable Card: {most_valuable_card['card_name']} (${most_valuable_card['card_market_value']:.2f})")
def main():
    generate_summary("card_portfolio.csv")
def test():
    generate_summary("test_card_portfolio.csv")
if __name__ == "__main__":
    print("Running summary repoort", file=sys.stderr)
    test()
