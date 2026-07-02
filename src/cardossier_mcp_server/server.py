#!/usr/bin/env python3
"""
CarDossier Market API - MCP Server
Allows AI assistants (Claude, Cursor, Windsurf, etc.) to query Polish used car market data.

Usage:
  export CARDOSSIER_API_KEY="your_api_key"
  cardossier-mcp
  # or: python -m cardossier_mcp_server.server

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

BASE_URL = "https://api.car-dossier.com/v1"

mcp = FastMCP("CarDossier Market API")


def _get_headers() -> Dict[str, str]:
    api_key = os.environ.get("CARDOSSIER_API_KEY")
    if not api_key:
        raise RuntimeError("CARDOSSIER_API_KEY environment variable not set.")
    return {"X-API-Key": api_key}


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
    Optionally filter by fuel_type (Benzyna/Diesel/Hybryda/Elektryczny),
    gearbox (Manualna/Automatyczna), or mileage.
    Costs 8 credits per call.
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
    Costs 5 credits per call.
    """
    return make_request(
        "/market/price-history",
        {"make": make, "model": model, "year": year, "months": months},
    )


@mcp.tool()
def get_market_liquidity(make: str, model: str, year: int) -> str:
    """
    Get estimated days-on-market (DOM) showing how fast this car typically sells in Poland.
    Costs 5 credits per call.
    """
    return make_request(
        "/market/liquidity",
        {"make": make, "model": model, "year": year},
    )


@mcp.tool()
def get_valuation_factors(make: str, model: str, year: int) -> str:
    """
    Quantify the price impact of import status, gearbox type, and fuel type for this car.
    Costs 8 credits per call.
    """
    return make_request(
        "/market/valuation-factors",
        {"make": make, "model": model, "year": year},
    )


@mcp.tool()
def get_regional_pricing(make: str, model: str, year: int) -> str:
    """
    Compare average prices across Polish voivodeships vs. the national average.
    Costs 5 credits per call.
    """
    return make_request(
        "/market/regional",
        {"make": make, "model": model, "year": year},
    )


def main():
    """Entry point for the cardossier-mcp CLI command."""
    print("Starting CarDossier Market API MCP Server...", file=sys.stderr)
    mcp.run()


if __name__ == "__main__":
    main()
