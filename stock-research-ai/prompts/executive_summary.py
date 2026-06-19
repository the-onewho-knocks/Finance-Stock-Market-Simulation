EXECUTIVE_SUMMARY_PROMPT = """
You are a financial analyst. Write a concise executive summary for {symbol}
based on the following data:

News: {news_summary}
Financial: {financial_summary}
Market: {market_summary}
SEC: {sec_summary}

Keep it under 200 words. Focus on key developments, financial health,
and near-term outlook.
"""