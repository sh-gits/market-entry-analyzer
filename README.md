# Global Market Entry Analyzer

An AI-powered strategy tool that generates consulting-grade market entry reports using live web research.

## What it does
- Analyzes real companies or new ventures entering any global market
- Pulls live data via Tavily search API
- Generates structured reports covering market overview, competitive landscape, regulatory environment, entry mode recommendation, and key risks
- Lists all sources used

## Built with
- Python + Flask
- Claude API (Anthropic)
- Tavily Search API

## How to run locally
1. Clone the repo
2. Add your API keys to a `.env` file
3. Run `pip install -r requirements.txt`
4. Run `python3 app.py`
5. Open `http://127.0.0.1:5000`
