"""
Weather Dashboard API
A production-ready weather API with caching, location search, and forecast data.
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import httpx
import asyncio
from datetime import datetime, timedelta
import json
import os
from functools import lru_cache
import hashlib

# Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY", "demo-api-key-for-showcase-purposes")
BASE_URL = "http://api.openweathermap.org/data/2.5"
GEO_URL = "http://api.openweathermap.org/geo/1.0"

# Simple in-memory cache (in production, use Redis)
weather_cache = {}
CACHE_DURATION = 600  # 10 minutes

app = FastAPI(
    title="Weather Dashboard API",
    description="Professional weather API with location search, forecasts, and caching",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class WeatherResponse(BaseModel):
    location: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    visibility: int
    wind_speed: float
    wind_direction: int
    weather_main: str
    weather_description: str
    icon: str
    sunrise: datetime
    sunset: datetime
    timezone: int
    timestamp: datetime

class ForecastItem(BaseModel):
    date: str
    temperature_min: float
    temperature_max: float
    humidity: int
    weather_main: str
    weather_description: str
    icon: str
    wind_speed: float

class ForecastResponse(BaseModel):
    location: str
    country: str
    forecast: List[ForecastItem]
    timestamp: datetime

class LocationResult(BaseModel):
    name: str
    country: str
    state: Optional[str]
    lat: float
    lon: float

class WeatherAlert(BaseModel):
    location: str
    alert_type: str
    message: str
    severity: str
    timestamp: datetime

# Cache utilities
def get_cache_key(endpoint: str, params: Dict[str, Any]) -> str:
    """Generate a cache key from endpoint and parameters."""
    param_str = json.dumps(params, sort_keys=True)
    return hashlib.md5(f"{endpoint}:{param_str}".encode()).hexdigest()

def is_cache_valid(timestamp: datetime) -> bool:
    """Check if cached data is still valid."""
    return datetime.now() - timestamp < timedelta(seconds=CACHE_DURATION)

def cache_data(key: str, data: Any) -> None:
    """Cache data with timestamp."""
    weather_cache[key] = {
        "data": data,
        "timestamp": datetime.now()
    }

def get_cached_data(key: str) -> Optional[Any]:
    """Get cached data if valid."""
    if key in weather_cache:
        cached = weather_cache[key]
        if is_cache_valid(cached["timestamp"]):
            return cached["data"]
        else:
            del weather_cache[key]  # Remove expired cache
    return None

# HTTP client
async def get_http_client():
    """Get async HTTP client."""
    return httpx.AsyncClient()

# API endpoints
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Weather Dashboard API",
        "version": "1.0.0",
        "endpoints": {
            "/weather/current": "Get current weather for a location",
            "/weather/forecast": "Get 5-day weather forecast",
            "/locations/search": "Search for locations",
            "/weather/alerts": "Get weather alerts (demo)",
            "/health": "Health check endpoint",
            "/docs": "API documentation"
        },
        "status": "operational",
        "cache_status": f"{len(weather_cache)} items cached"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cache_items": len(weather_cache),
        "api_key_configured": API_KEY != "demo_key_get_real_one_from_openweathermap"
    }

@app.get("/weather/current", response_model=WeatherResponse)
async def get_current_weather(
    location: str = Query(..., description="City name or 'lat,lon' coordinates"),
    units: str = Query("metric", description="Units: metric, imperial, kelvin")
):
    """Get current weather for a location."""
    
    # Check cache first
    cache_key = get_cache_key("current", {"location": location, "units": units})
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        async with httpx.AsyncClient() as client:
            # Determine if location is coordinates or city name
            if "," in location and len(location.split(",")) == 2:
                try:
                    lat, lon = map(float, location.split(","))
                    url = f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={units}"
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid coordinates format")
            else:
                url = f"{BASE_URL}/weather?q={location}&appid={API_KEY}&units={units}"
            
            response = await client.get(url)
            
            if response.status_code == 401:
                raise HTTPException(status_code=503, detail="Weather service unavailable - API key required")
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Location '{location}' not found")
            elif response.status_code != 200:
                raise HTTPException(status_code=503, detail="Weather service temporarily unavailable")
            
            data = response.json()
            
            # Transform API response to our model
            weather_data = WeatherResponse(
                location=data["name"],
                country=data["sys"]["country"],
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                humidity=data["main"]["humidity"],
                pressure=data["main"]["pressure"],
                visibility=data.get("visibility", 0),
                wind_speed=data.get("wind", {}).get("speed", 0),
                wind_direction=data.get("wind", {}).get("deg", 0),
                weather_main=data["weather"][0]["main"],
                weather_description=data["weather"][0]["description"].title(),
                icon=data["weather"][0]["icon"],
                sunrise=datetime.fromtimestamp(data["sys"]["sunrise"]),
                sunset=datetime.fromtimestamp(data["sys"]["sunset"]),
                timezone=data["timezone"],
                timestamp=datetime.now()
            )
            
            # Cache the result
            cache_data(cache_key, weather_data)
            
            return weather_data
            
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Unable to connect to weather service")

@app.get("/weather/forecast", response_model=ForecastResponse)
async def get_weather_forecast(
    location: str = Query(..., description="City name or 'lat,lon' coordinates"),
    units: str = Query("metric", description="Units: metric, imperial, kelvin"),
    days: int = Query(5, ge=1, le=5, description="Number of forecast days (1-5)")
):
    """Get weather forecast for a location."""
    
    # Check cache first
    cache_key = get_cache_key("forecast", {"location": location, "units": units, "days": days})
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        async with httpx.AsyncClient() as client:
            # Determine if location is coordinates or city name
            if "," in location and len(location.split(",")) == 2:
                try:
                    lat, lon = map(float, location.split(","))
                    url = f"{BASE_URL}/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units={units}"
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid coordinates format")
            else:
                url = f"{BASE_URL}/forecast?q={location}&appid={API_KEY}&units={units}"
            
            response = await client.get(url)
            
            if response.status_code == 401:
                raise HTTPException(status_code=503, detail="Weather service unavailable - API key required")
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Location '{location}' not found")
            elif response.status_code != 200:
                raise HTTPException(status_code=503, detail="Weather service temporarily unavailable")
            
            data = response.json()
            
            # Process forecast data (group by day)
            daily_forecasts = {}
            for item in data["list"][:days * 8]:  # 8 forecasts per day (3-hour intervals)
                date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
                
                if date not in daily_forecasts:
                    daily_forecasts[date] = {
                        "temps": [],
                        "humidity": [],
                        "weather": item["weather"][0],
                        "wind_speed": item["wind"]["speed"]
                    }
                
                daily_forecasts[date]["temps"].append(item["main"]["temp"])
                daily_forecasts[date]["humidity"].append(item["main"]["humidity"])
            
            # Create forecast items
            forecast_items = []
            for date, day_data in list(daily_forecasts.items())[:days]:
                forecast_items.append(ForecastItem(
                    date=date,
                    temperature_min=min(day_data["temps"]),
                    temperature_max=max(day_data["temps"]),
                    humidity=int(sum(day_data["humidity"]) / len(day_data["humidity"])),
                    weather_main=day_data["weather"]["main"],
                    weather_description=day_data["weather"]["description"].title(),
                    icon=day_data["weather"]["icon"],
                    wind_speed=day_data["wind_speed"]
                ))
            
            forecast_data = ForecastResponse(
                location=data["city"]["name"],
                country=data["city"]["country"],
                forecast=forecast_items,
                timestamp=datetime.now()
            )
            
            # Cache the result
            cache_data(cache_key, forecast_data)
            
            return forecast_data
            
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Unable to connect to weather service")

@app.get("/locations/search", response_model=List[LocationResult])
async def search_locations(
    query: str = Query(..., min_length=2, description="Location name to search"),
    limit: int = Query(5, ge=1, le=10, description="Maximum number of results")
):
    """Search for locations by name."""
    
    # Check cache first
    cache_key = get_cache_key("locations", {"query": query, "limit": limit})
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        async with httpx.AsyncClient() as client:
            url = f"{GEO_URL}/direct?q={query}&limit={limit}&appid={API_KEY}"
            response = await client.get(url)
            
            if response.status_code == 401:
                raise HTTPException(status_code=503, detail="Location service unavailable - API key required")
            elif response.status_code != 200:
                raise HTTPException(status_code=503, detail="Location service temporarily unavailable")
            
            data = response.json()
            
            locations = [
                LocationResult(
                    name=item["name"],
                    country=item["country"],
                    state=item.get("state"),
                    lat=item["lat"],
                    lon=item["lon"]
                )
                for item in data
            ]
            
            # Cache the result
            cache_data(cache_key, locations)
            
            return locations
            
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Unable to connect to location service")

@app.get("/weather/alerts", response_model=List[WeatherAlert])
async def get_weather_alerts(
    location: str = Query(..., description="Location to get alerts for")
):
    """Get weather alerts for a location (demo implementation)."""
    
    # This is a demo implementation - in production, integrate with weather alert APIs
    demo_alerts = [
        WeatherAlert(
            location=location,
            alert_type="Temperature",
            message=f"High temperature expected in {location} today",
            severity="moderate",
            timestamp=datetime.now()
        )
    ]
    
    return demo_alerts

@app.get("/cache/stats")
async def get_cache_stats():
    """Get cache statistics (for monitoring)."""
    valid_cache = 0
    expired_cache = 0
    
    for key, cached in weather_cache.items():
        if is_cache_valid(cached["timestamp"]):
            valid_cache += 1
        else:
            expired_cache += 1
    
    return {
        "total_cache_items": len(weather_cache),
        "valid_cache_items": valid_cache,
        "expired_cache_items": expired_cache,
        "cache_duration_seconds": CACHE_DURATION,
        "cache_keys": list(weather_cache.keys())[:10]  # Show first 10 keys
    }

@app.delete("/cache/clear")
async def clear_cache():
    """Clear all cached data."""
    global weather_cache
    cache_count = len(weather_cache)
    weather_cache = {}
    
    return {
        "message": f"Cache cleared successfully",
        "items_removed": cache_count,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("🌤️  Starting Weather Dashboard API...")
    print("📡 CORS: Allowing all origins for development")
    print("🔍 API Documentation: http://localhost:8002/docs")
    print("💾 Cache: In-memory caching enabled (10-minute duration)")
    print("🗝️  API Key: Get your free key from https://openweathermap.org/api")
    uvicorn.run(app, host="0.0.0.0", port=8002)
