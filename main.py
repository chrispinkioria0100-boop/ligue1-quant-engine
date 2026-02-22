import requests
import pandas as pd
import numpy as np
import os
from requests.auth import HTTPBasicAuth

# ==============================
# CONFIGURATION
# ==============================

API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
WP_SITE = os.getenv("WP_SITE")

LEAGUE_ID = 61  # Ligue 1
SEASON = 2026

# ==============================
# FETCH FIXTURES
# ==============================

def get_upcoming_fixtures():
    url = f"https://v3.football.api-sports.io/fixtures?league={LEAGUE_ID}&season={SEASON}&next=5"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data["response"]

# ==============================
# SIMPLE MODEL (PLACEHOLDER)
# ==============================

def model_probability():
    return np.random.uniform(0.55, 0.70)

# ==============================
# EDGE CALCULATION
# ==============================

def calculate_edge(model_prob, odds):
    implied_prob = 1 / odds
    return model_prob - implied_prob

# ==============================
# POST TO WORDPRESS
# ==============================

def post_to_wordpress(title, content):
    url = f"{WP_SITE}/wp-json/wp/v2/posts"
    auth = HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD)
    post = {
        "title": title,
        "content": content,
        "status": "publish"
    }
    response = requests.post(url, json=post, auth=auth)
    print(response.status_code, response.text)

# ==============================
# MAIN ENGINE
# ==============================

def run_engine():
    fixtures = get_upcoming_fixtures()

    for match in fixtures:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        odds = 1.90  # Placeholder odds
        model_prob = model_probability()
        edge = calculate_edge(model_prob, odds)

        if edge >= 0.07:
            title = f"Position – {home} vs {away}"
            content = f"""
            Market: Over 2.5 Goals  
            Odds: {odds}  
            Model Probability: {round(model_prob,2)}  
            Edge: {round(edge,2)}  
            Capital Allocation: 1%  
            Status: Pending
            """
            post_to_wordpress(title, content)

if __name__ == "__main__":
    run_engine()
