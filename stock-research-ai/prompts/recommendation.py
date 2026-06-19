RECOMMENDATION_PROMPT = """
Based on the following analysis, provide a BUY/SELL/HOLD recommendation
for {symbol}.

Strengths: {strengths}
Risks: {risks}
Opportunities: {opportunities}
Red Flags: {red_flags}
News Sentiment: {sentiment}

Current Recommendation: {current_recommendation}
Confidence: {confidence_score}

Output in JSON format with keys: recommendation, rationale, confidence_score.
"""