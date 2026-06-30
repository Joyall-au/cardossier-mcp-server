#!/usr/bin/env python3
"""
CarDossier Market API - MCP Server
Allows AI assistants (Claude, Cursor, etc.) to query Polish used car market data.

Usage:
  export CARDOSSIER_API_KEY="your_api_key"
  python mcp-server.py
"""
import os
import sys
import requests
from typing import Optional, Dict, Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Error: 'mcp' package not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

API_KEY = os.environ.get("CARDOSSIER_API_KEY")
if not API_KEY:
    print("Error: CARDOSSIER_API_KEY environment variable not set.", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://api.car-dossier.com/v1"
HEADERS = {"X-API-Key": API_KEY}

mcp = FastMCP("CarDossier")

def make_request(endpoint: str, params: Dict[str, Any]) -> str:
    """Helper to make API requests and format responses."""
    try:
        # Filter out None values
        clean_params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, params=clean_params)
        data = response.json()
        
        if response.status_code != 200 or data.get("status") == "error":
            err = data.get("error", {})
            return f"API Error ({err.get('code')}): {err.get('message', response.text)}"
            
        return str(data.get("data", data))
    except Exception as e:
        return f"Request failed: {str(e)}"

@mcp.tool()
def get_market_valuation(make: str, model: str, year: int, fuel_type: Optional[str] = None, gearbox: Optional[str] = None, mileage: Optional[int] = None) -> str:
    """
    Get average, median, P25, and P75 prices for a specific make/model/year in Poland.
    Optionally filter by fuel_type (Benzyna/Diesel/Hybryda/Elektryczny), gearbox (Manualna/Automatyczna), or mileage.
    """
    return make_request("/market/valuation", {
        "make": make, "model": model, "year": year,
        "fuel_type": fuel_type, "gearbox": gearbox, "mileage": mileage
    })

@mcp.tool()
def get_price_history(make: str, model: str, year: int, months: Optional[int] = 6) -> str:
    """
    Get monthly average price trend for up to 24 months to identify depreciation curves.
    """
    return make_request("/market/price-history", {
        "make": make, "model": model, "year": year, "months": months
    })

@mcp.tool()
def get_market_liquidity(make: str, model: str, year: int) -> str:
    """
    Get estimated days-on-market (DOM) showing how fast this car typically sells.
    """
    return make_request("/market/liquidity", {
        "make": make, "model": model, "year": year
    })

@mcp.tool()
def get_valuation_factors(make: str, model: str, year: int) -> str:
    """
    Quantify the price impact of import status, gearbox type, and fuel type for this car.
    """
    return make_request("/market/valuation-factors", {
        "make": make, "model": model, "year": year
    })

@mcp.tool()
def get_regional_pricing(make: str, model: str, year: int) -> str:
    """
    Compare average prices across Polish voivodeships vs. the national average.
    """
    return make_request("/market/regional", {
        "make": make, "model": model, "year": year
    })

if __name__ == "__main__":
    print("Starting CarDossier MCP Server...", file=sys.stderr)
    mcp.run()
