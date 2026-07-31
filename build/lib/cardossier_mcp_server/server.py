#!/usr/bin/env python3
"""
CarDossier Poland Market API - MCP Server
Allows AI assistants (Claude, Cursor, Windsurf, etc.) to query Polish used car market data.

Works WITHOUT an API key out of the box: the API serves 5 keyless demo calls per
IP per day with full real data. Register free (50 credits, no card) at
https://car-dossier.com/en/api for more quota.

Usage:
  export CARDOSSIER_API_KEY="your_api_key"   # optional
  cardossier-mcp
  # or: cardossier-mcp-server / python -m cardossier_mcp_server.server

mcp-name: io.github.Joyall-au/cardossier-market-api
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

BASE_URL = "https://car-dossier.com/api/v1"

mcp = FastMCP("CarDossier Market API")


def _get_headers() -> Dict[str, str]:
    # No key → keyless demo tier (5 real calls per IP per day)
    api_key = os.environ.get("CARDOSSIER_API_KEY")
    return {"X-API-Key": api_key} if api_key else {}


def make_request(endpoint: str, params: Dict[str, Any]) -> str:
    """Helper to make API requests and format responses."""
    try:
        clean_params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(
            f"{BASE_URL}{endpoint}",
            headers=_get_headers(),
            params=clean_params,
            timeout=10,
        )
        data = response.json()
        if response.status_code != 200 or data.get("status") == "error":
            err = data.get("error", {})
            return f"API Error ({err.get('code')}): {err.get('message', response.text)}"
        return str(data.get("data", data))
    except RuntimeError as e:
        return f"Configuration error: {str(e)}"
    except Exception as e:
        return f"Request failed: {str(e)}"


@mcp.tool()
def get_market_valuation(
    make: str,
    model: str,
    year: int,
    fuel_type: Optional[str] = None,
    gearbox: Optional[str] = None,
    mileage: Optional[int] = None,
) -> str:
    """
    Get average, median, P25, and P75 prices for a specific make/model/year in Poland.
    Natural names work: 'VW Golf', 'BMW 3 Series' or '320d', 'Mercedes C-Class', 'Audi A4', 'XC60'.
    Optional filters: fuel_type (petrol/diesel/hybrid/electric/lpg or Polish values),
    gearbox (manual/automatic), mileage (km, matches a ±30% band).
    Costs 8 credits per call; failed calls are auto-refunded.
    """
    return make_request(
        "/market/valuation",
        {"make": make, "model": model, "year": year,
         "fuel_type": fuel_type, "gearbox": gearbox, "mileage": mileage},
    )


@mcp.tool()
def get_price_history(
    make: str,
    model: str,
    year: int,
    months: Optional[int] = 6,
) -> str:
    """
    Get monthly average price trend for up to 24 months to identify depreciation curves.
    Costs 10 credits per call; failed calls are auto-refunded.
    """
    return make_request(
        "/market/price-history",
        {"make": make, "model": model, "year": year, "months": months},
    )


@mcp.tool()
def get_market_liquidity(make: str, model: str, year: int) -> str:
    """
    Get estimated days-on-market (DOM) showing how fast this car typically sells in Poland.
    Costs 6 credits per call; failed calls are auto-refunded.
    """
    return make_request(
        "/market/liquidity",
        {"make": make, "model": model, "year": year},
    )


@mcp.tool()
def get_valuation_factors(make: str, model: str, year: int) -> str:
    """
    Quantify the price impact of import status, gearbox type, and fuel type for this car.
    Costs 12 credits per call; failed calls are auto-refunded.
    """
    return make_request(
        "/market/valuation-factors",
        {"make": make, "model": model, "year": year},
    )


@mcp.tool()
def get_regional_pricing(make: str, model: str, year: int) -> str:
    """
    Compare average prices across Polish voivodeships vs. the national average.
    Costs 8 credits per call; failed calls are auto-refunded.
    """
    return make_request(
        "/market/regional",
        {"make": make, "model": model, "year": year},
    )


def main():
    """Entry point for the cardossier-mcp CLI command."""
    if not os.environ.get("CARDOSSIER_API_KEY"):
        print("No CARDOSSIER_API_KEY set - running in keyless demo mode (5 free calls/day). "
              "Get a free key with 50 credits at https://car-dossier.com/en/api", file=sys.stderr)
    print("Starting CarDossier Market API MCP Server...", file=sys.stderr)
    mcp.run()


if __name__ == "__main__":
    main()
