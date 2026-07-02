# CarDossier Poland Market API — MCP Server

mcp-name: io.github.Joyall-au/cardossier-market-api

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

An **MCP (Model Context Protocol) server** that gives AI assistants — Claude, Cursor, Windsurf, and any MCP-compatible agent — real-time access to Polish used car market data via the [CarDossier Market API](https://car-dossier.com/en/api/).

## What It Does

This server exposes 5 tools that AI agents can call to answer questions like:

- *"What is a 2019 Toyota Corolla worth in Poland right now?"*
- *"Has the price of diesel BMWs been rising or falling over the past 6 months?"*
- *"How quickly do used Volkswagen Golfs sell in Poland?"*
- *"Is a 2020 Audi A4 cheaper in Mazowieckie or Śląskie?"*
- *"How much more does an automatic gearbox add to the price of a 2018 Ford Focus?"*

## Available Tools

| Tool | Description | Credits |
|------|-------------|---------|
| `get_market_valuation` | Average, median, P25 & P75 prices for any make/model/year | 8 |
| `get_price_history` | Monthly price trend for up to 24 months | 10 |
| `get_market_liquidity` | Estimated days-on-market (how fast a car sells) | 6 |
| `get_valuation_factors` | Price impact of gearbox type, fuel type, import status | 12 |
| `get_regional_prices` | Price comparison across all 16 Polish voivodeships | 8 |

Data source: 2M+ active listings from Poland's leading car marketplaces, updated daily.

## Prerequisites

- Python 3.9+
- A CarDossier API key — [register for free](https://car-dossier.com/en/api/pricing) to get **50 free credits** (no credit card required), or purchase a paid package starting at $49 for 5,000 credits

## Installation

```bash
# Clone the repository
git clone https://github.com/Joyall-au/cardossier-mcp-server.git
cd cardossier-mcp-server

# Install dependencies
pip install mcp requests
```

## Usage

### 1. Set your API key

```bash
export CARDOSSIER_API_KEY="your_api_key_here"
```

### 2. Run the server

```bash
python mcp_server.py
```

### 3. Connect to Claude Desktop

Add the following to your Claude Desktop config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "cardossier": {
      "command": "python",
      "args": ["/path/to/cardossier-mcp-server/mcp_server.py"],
      "env": {
        "CARDOSSIER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 4. Connect to Cursor or Windsurf

Add to your MCP settings:

```json
{
  "cardossier": {
    "command": "python",
    "args": ["/path/to/mcp_server.py"],
    "env": {
      "CARDOSSIER_API_KEY": "your_api_key_here"
    }
  }
}
```

## Example Interactions

Once connected, you can ask your AI assistant:

> **"What's the current market value of a 2020 BMW 3 Series diesel in Poland?"**

The agent will call `get_market_valuation` with `make=BMW, model=3 Series, year=2020, fuel_type=diesel` and return the statistical distribution of prices.

> **"Show me how Toyota Corolla prices have changed over the last year"**

The agent will call `get_price_history` with `months=12` and return a monthly price trend.

> **"Compare used Skoda Octavia prices across Polish regions"**

The agent will call `get_regional_prices` and return a breakdown by voivodeship.

## API Reference

Full API documentation: [car-dossier.com/en/api/docs](https://car-dossier.com/en/api/docs)  
OpenAPI 3.1 spec: [car-dossier.com/openapi.yaml](https://car-dossier.com/openapi.yaml)  
FAQ: [car-dossier.com/en/api/faq/](https://car-dossier.com/en/api/faq/)

## Pricing

The CarDossier Market API uses a pay-as-you-go credit system. Credits never expire.

> **Free Trial:** Register at [car-dossier.com/en/api/pricing](https://car-dossier.com/en/api/pricing) to receive **50 free credits** instantly — no credit card required. Enough for ~6 market valuation calls.

| Package      | Price | Credits  | ~Valuation calls |
|--------------|-------|----------|------------------|
| **Free Trial** | **$0** | **50** | **~6** |
| Starter      | $49   | 5,000    | ~625             |
| Growth       | $129  | 15,000   | ~1,875           |
| Pro          | $299  | 40,000   | ~5,000           |
| Business     | $699  | 100,000  | ~12,500          |

[Start for free — get 50 credits →](https://car-dossier.com/en/api/pricing)

## License

MIT License — see [LICENSE](LICENSE) for details.

## About

Built by [CarDossier](https://car-dossier.com) — Poland's leading vehicle history and market data platform.
