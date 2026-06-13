# Provider Layer

These module files are your **provider layer**. Think of them as adapters that know how to talk to external APIs. The rest of your application should not care whether data comes from Finnhub, FMP, Polygon, or SEC.

---

# Finnhub Client

## Purpose

The Finnhub client is responsible for fetching:

- Company news
- Live stock quotes
- Company profile information

This provider supplies real-time market information and company metadata.

---

## Functions

### `get_company_news()`

Fetches recent news articles related to a stock symbol.

#### Usage

Used by:

- News Agent
- Sentiment Agent
- Research Agent

#### Returns

- Headlines
- Summaries
- Article URLs
- Publication Dates

---

### `get_quote()`

Fetches the latest stock quote.

#### Returns

- Current Price
- Day High
- Day Low
- Previous Close

#### Usage

Used when generating:

- Market reports
- Live stock snapshots
- Price summaries

---

### `get_company_profile()`

Fetches company metadata.

#### Returns

- Company Name
- Industry
- Country
- Exchange
- Website

#### Usage

Useful for:

- Company overview sections
- Research reports
- Stock summaries

---

## Role in the System

```text
User Request
      |
      v
 Finnhub Client
      |
      +--> Company News
      +--> Live Quotes
      +--> Company Profile
      |
      v
 Research Agents
```

---

# FMP Client (Financial Modeling Prep)

## Purpose

The FMP client is responsible for fetching company fundamentals and financial statements.

This provider supplies the data required for fundamental analysis.

---

## Functions

### `get_income_statement()`

Fetches company income statements.

#### Returns

- Revenue
- Gross Profit
- Operating Income
- Net Income
- Earnings Per Share

#### Usage

Used for:

- Revenue Growth Analysis
- Profitability Analysis
- Financial Trend Analysis

---

### `get_balance_sheet()`

Fetches company balance sheets.

#### Returns

- Total Assets
- Total Liabilities
- Total Debt
- Cash
- Shareholder Equity

#### Usage

Used for:

- Debt Analysis
- Liquidity Analysis
- Financial Health Assessment

---

### `get_ratios()`

Fetches financial ratios.

#### Returns

- PE Ratio
- ROE
- ROA
- Debt-to-Equity
- Current Ratio

#### Usage

Used for:

- Company Valuation
- Quality Analysis
- Fundamental Scoring

---

### `get_price_history()`

Fetches historical stock prices.

#### Returns

Historical OHLC market data.

#### Usage

Used for:

- Trend Analysis
- Performance Analysis
- Historical Research

---

## Role in the System

```text
User Request
      |
      v
   FMP Client
      |
      +--> Income Statements
      +--> Balance Sheets
      +--> Ratios
      +--> Historical Prices
      |
      v
 Fundamental Analysis Agent
```

---

# Polygon Client

## Purpose

The Polygon client is responsible for fetching market data and trading information.

This provider supplies high-quality historical and aggregated market data.

---

## Functions

### `get_aggregates()`

Fetches aggregated OHLC candle data.

#### Returns

- Open Price
- High Price
- Low Price
- Close Price
- Trading Volume

#### Usage

Used for:

- Technical Analysis
- Moving Averages
- Volatility Analysis
- Price Charts

---

### `get_ticker_details()`

Fetches detailed ticker metadata.

#### Returns

- Company Name
- Market
- Exchange
- Industry
- Sector

#### Usage

Used for:

- Company Information
- Market Classification
- Security Metadata

---

## Role in the System

```text
User Request
      |
      v
 Polygon Client
      |
      +--> OHLC Data
      +--> Market Data
      +--> Ticker Details
      |
      v
 Technical Analysis Agent
```

---

# SEC Client

## Purpose

The SEC client is responsible for retrieving official SEC filings directly from EDGAR.

This provider supplies the highest quality regulatory information available.

---

## Functions

### `search_filings()`

Searches SEC EDGAR filings.

#### Returns

Filing metadata such as:

- Company Name
- Filing Type
- Filing Date
- Filing URL

#### Usage

Used to locate:

- 10-K Reports
- 10-Q Reports
- 8-K Reports

---

### `get_filing_document()`

Downloads filing content.

#### Returns

The complete filing document.

#### Usage

Used for extracting:

- Business Overview
- Risk Factors
- Management Discussion & Analysis (MD&A)
- Financial Disclosures

---

## Role in the System

```text
User Request
      |
      v
   SEC Client
      |
      +--> 10-K Reports
      +--> 10-Q Reports
      +--> 8-K Reports
      |
      v
 Filing Analysis Agent
```

---

# Provider Responsibilities Summary

| Provider | Responsibilities |
|-----------|------------------|
| Finnhub | News, Quotes, Company Profiles |
| FMP | Financial Statements, Ratios, Fundamentals |
| Polygon | Market Data, OHLC Candles, Technical Analysis Data |
| SEC | Regulatory Filings, Annual Reports, Quarterly Reports |

---

# Complete Data Flow

```text
                    User Request
                          |
                          v
                  Research Service
                          |
       ----------------------------------------
       |                 |            |       |
       v                 v            v       v
   Finnhub             FMP        Polygon    SEC
       |                 |            |       |
       |                 |            |       |
       ----------------------------------------
                          |
                          v
                 Research Agents
                          |
                          v
                AI Investment Report
```

The provider layer acts as the external data gateway for the entire Stock Research AI platform. Each provider specializes in a specific type of financial information and together they create a complete research ecosystem.