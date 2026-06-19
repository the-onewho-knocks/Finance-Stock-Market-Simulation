INVESTMENT_REPORT_PROMPT = """
Generate a detailed investment report for {symbol}.

Data sources:
- News: {news_data}
- Financials: {financial_data}
- Market: {market_data}
- SEC Filings: {sec_data}

Include sections:
1. Company Overview
2. Financial Analysis
3. Market Position
4. Risk Factors
5. Recommendation

Recommendation: {recommendation}
Confidence Score: {confidence_score}
"""