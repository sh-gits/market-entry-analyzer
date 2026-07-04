from flask import Flask, request, jsonify, send_from_directory
import anthropic
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

app = Flask(__name__)

anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    mode = data.get('mode', 'real')
    target_country = data.get('target_country', '')

    if mode == 'real':
        company_name = data.get('company_name', '')
        search_query = f"{company_name} market entry {target_country} business environment regulations competition"
        company_context = f"Company: {company_name}"
    else:
        description = data.get('description', '')
        industry = data.get('industry', '')
        search_query = f"{industry} market {target_country} business environment regulations competition opportunities"
        company_context = f"New Venture Description: {description}\nIndustry: {industry}"

    search_results = tavily_client.search(
        query=search_query,
        search_depth="advanced",
        max_results=8,
        include_raw_content=False
    )

    sources = []
    search_context = ""
    for result in search_results.get('results', []):
        sources.append({
            'title': result.get('title', ''),
            'url': result.get('url', ''),
        })
        search_context += f"\nSource: {result.get('title')}\n{result.get('content')}\n"

    prompt = f"""You are a senior strategy consultant. Using the research below, produce a structured market entry analysis report.

{company_context}
Target Market: {target_country}

LIVE RESEARCH DATA:
{search_context}

Write the report in this exact structure:

## Market Overview
[Market size, growth trends, key dynamics]

## Competitive Landscape
[Key players, market share, competitive intensity]

## Regulatory Environment
[Key regulations, barriers to entry, compliance requirements]

## Cultural & Operational Considerations
[Business culture, consumer behaviour, operational factors]

## Recommended Entry Mode
[Export / Joint Venture / Acquisition / Greenfield — with clear reasoning]

## Key Risks & Mitigations
[Top 3-5 risks with mitigation strategies]

## Verdict
[One paragraph executive summary and go/no-go recommendation]

Be specific, cite data where available from the research, and write like a McKinsey analyst."""

    message = anthropic_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=6000,
        messages=[{"role": "user", "content": prompt}]
    )

    report = message.content[0].text

    return jsonify({
        'report': report,
        'sources': sources
    })

if __name__ == '__main__':
    app.run(debug=True)