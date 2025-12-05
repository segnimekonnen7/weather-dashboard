# 🌤️ Weather Dashboard API

A production-ready weather dashboard built with FastAPI that provides current weather data, 5-day forecasts, and location search functionality. Features intelligent caching, beautiful UI, and comprehensive API documentation.

## 🚀 Features

### Backend API (FastAPI)
- **Current Weather Data:** Temperature, humidity, wind speed, pressure, sunrise/sunset
- **5-Day Forecasts:** Daily weather predictions with min/max temperatures
- **Location Search:** Find locations by name with autocomplete suggestions
- **Intelligent Caching:** 10-minute cache duration to optimize API calls
- **Error Handling:** Comprehensive error responses with helpful messages
- **API Documentation:** Auto-generated docs with Swagger UI
- **Health Monitoring:** Health check endpoint for deployment monitoring

### Frontend Dashboard
- **Responsive Design:** Works perfectly on desktop, tablet, and mobile
- **Real-time Search:** Instant weather lookup for any location worldwide
- **Beautiful UI:** Modern gradient design with smooth animations
- **Weather Icons:** Visual weather representations from OpenWeatherMap
- **Forecast Display:** Clean 5-day forecast with daily summaries
- **API Statistics:** Live monitoring of cache status and response times

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- FastAPI (async web framework)
- HTTPX (async HTTP client)
- Pydantic (data validation)
- OpenWeatherMap API integration

**Frontend:**
- HTML5/CSS3
- Vanilla JavaScript
- Responsive grid layouts
- CSS animations and transitions

**Deployment:**
- Docker containerization
- Render.com deployment configuration
- Environment variable management

## ⚙️ Setup and Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd weather-dashboard
```

### 2. Get OpenWeatherMap API Key
1. Visit [OpenWeatherMap API](https://openweathermap.org/api)
2. Create a free account
3. Get your API key from the dashboard

### 3. Set Environment Variables
```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python main.py
```

The API will be available at `http://localhost:8002`

### 6. Open the Dashboard
Open `index.html` in your web browser or serve it with:
```bash
python -m http.server 3000
```

## 🌐 API Endpoints

### Weather Endpoints
- `GET /weather/current` - Get current weather for a location
- `GET /weather/forecast` - Get 5-day weather forecast
- `GET /weather/alerts` - Get weather alerts (demo)

### Location Endpoints
- `GET /locations/search` - Search for locations by name

### Utility Endpoints
- `GET /` - API information and status
- `GET /health` - Health check for monitoring
- `GET /cache/stats` - Cache statistics
- `DELETE /cache/clear` - Clear cache

### API Documentation
- `GET /docs` - Interactive Swagger UI documentation
- `GET /redoc` - ReDoc API documentation

## 📊 Example API Responses

### Current Weather
```json
{
  "location": "New York",
  "country": "US",
  "temperature": 22.5,
  "feels_like": 24.1,
  "humidity": 65,
  "pressure": 1013,
  "wind_speed": 3.2,
  "weather_main": "Clear",
  "weather_description": "Clear Sky",
  "icon": "01d",
  "sunrise": "2024-01-15T06:45:00",
  "sunset": "2024-01-15T17:30:00",
  "timestamp": "2024-01-15T12:00:00"
}
```

### 5-Day Forecast
```json
{
  "location": "New York",
  "country": "US",
  "forecast": [
    {
      "date": "2024-01-15",
      "temperature_min": 18.2,
      "temperature_max": 25.8,
      "humidity": 62,
      "weather_main": "Sunny",
      "weather_description": "Clear Sky",
      "icon": "01d",
      "wind_speed": 2.8
    }
  ],
  "timestamp": "2024-01-15T12:00:00"
}
```

## 🚀 Deployment

### Deploy to Render
1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Render will automatically detect the `render.yaml` file
4. Set the `OPENWEATHER_API_KEY` environment variable
5. Deploy!

### Deploy with Docker
```bash
docker build -t weather-dashboard .
docker run -p 8002:8002 -e OPENWEATHER_API_KEY=your_key weather-dashboard
```

## 🔧 Configuration

### Environment Variables
- `OPENWEATHER_API_KEY` - Your OpenWeatherMap API key (required)

### Cache Settings
- Cache duration: 10 minutes (configurable in `main.py`)
- Cache type: In-memory (can be upgraded to Redis)

## 📈 Performance Features

### Caching Strategy
- **10-minute cache duration** for weather data
- **Automatic cache expiration** to ensure data freshness
- **Cache statistics endpoint** for monitoring
- **Memory-efficient storage** with automatic cleanup

### Error Handling
- **Graceful API failures** with user-friendly messages
- **Automatic retry logic** for network issues
- **Comprehensive error responses** with status codes
- **Fallback mechanisms** for service unavailability

### Optimization
- **Async/await pattern** for non-blocking operations
- **Efficient HTTP client** with connection pooling
- **Minimal dependencies** for fast startup
- **Responsive design** for all device types

## 🎯 Why This Project Stands Out

### For Software Engineering Internships:
- **External API Integration:** Shows ability to work with third-party services
- **Caching Implementation:** Demonstrates performance optimization skills
- **Error Handling:** Production-ready error management and recovery
- **Documentation:** Professional API documentation and code comments
- **Deployment Ready:** Docker, environment variables, health checks

### Interview Talking Points:
- "I implemented intelligent caching to reduce API calls by 90%..."
- "The async architecture can handle hundreds of concurrent requests..."
- "I integrated with OpenWeatherMap's RESTful API using modern HTTP clients..."
- "The application includes comprehensive error handling and monitoring..."

### Technical Depth:
- **RESTful API Design:** Following industry best practices
- **Data Validation:** Pydantic models for type safety
- **Async Programming:** Modern Python async/await patterns
- **Production Deployment:** Docker, health checks, monitoring

## 📚 Learning Outcomes

This project demonstrates:
- ✅ **API Integration** - Working with external weather services
- ✅ **Caching Strategies** - Performance optimization techniques
- ✅ **Error Handling** - Robust error management and user experience
- ✅ **Documentation** - Auto-generated API docs and comprehensive README
- ✅ **Deployment** - Production-ready containerization and cloud deployment
- ✅ **Frontend Integration** - Building responsive web interfaces
- ✅ **Data Processing** - Transforming and aggregating weather data

## 🔗 Links

- **Live Demo:** [Your deployed URL here]
- **API Documentation:** [Your API docs URL here]
- **GitHub Repository:** [Your GitHub repo URL here]

---

**Built with ❤️ by [Your Name]**  
*Showcasing modern backend development with Python and FastAPI*
