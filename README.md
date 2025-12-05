# Weather Dashboard API

Weather API built with FastAPI. Integrates with OpenWeatherMap and has a simple caching system to avoid hitting their API too much.

## What it does

Gets current weather and 5-day forecasts for any location. The caching was important because OpenWeatherMap has rate limits on the free tier, so I cache responses for 10 minutes to cut down on API calls.

## Features

- Current weather data (temp, humidity, wind, etc.)
- 5-day forecasts
- Location search
- 10-minute caching to reduce API calls
- Error handling for when the API is down
- Auto-generated API docs (Swagger UI)

## Tech Stack

Backend: Python 3.11, FastAPI, HTTPX (async HTTP client), Pydantic  
Frontend: HTML/CSS/JavaScript  
Deployment: Docker, Render

## Setup

1. Get an OpenWeatherMap API key from https://openweathermap.org/api (free tier works fine)

2. Set the API key:
```bash
export OPENWEATHER_API_KEY="your_key_here"
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run it:
```bash
python main.py
```

API runs on `http://localhost:8002`

5. Open `index.html` in your browser or:
```bash
python -m http.server 3000
```

## API Endpoints

Weather:
- `GET /weather/current` - Current weather
- `GET /weather/forecast` - 5-day forecast

Location:
- `GET /locations/search` - Search locations

Other:
- `GET /health` - Health check
- `GET /cache/stats` - Cache statistics
- `GET /docs` - Swagger UI docs

## The Caching Part

I cache weather data for 10 minutes. This means if someone requests weather for "New York" and someone else requests it 5 minutes later, it uses the cached data instead of calling OpenWeatherMap again. Saves API calls and makes responses faster.

You can check cache stats at `/cache/stats` and clear it at `/DELETE /cache/clear` if needed.

## Deployment

Render: Just connect your GitHub repo and set the `OPENWEATHER_API_KEY` environment variable. It'll auto-deploy.

Docker:
```bash
docker build -t weather-dashboard .
docker run -p 8002:8002 -e OPENWEATHER_API_KEY=your_key weather-dashboard
```

## Why This Project

Good practice for:
- Working with external APIs
- Implementing caching
- Error handling when APIs fail
- Building async endpoints

The caching was the interesting part - had to think about when to expire data and how to handle cache misses.

## License

MIT

---

Built by Segni Mekonnen
