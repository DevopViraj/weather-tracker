# Weather Tracker Application

A Flask-based application that tracks and displays weather information.

## Features

- Real-time weather data for cities
- Search for cities and view current weather
- Save search results for later reference
- View historical weather data
- Dark mode UI with animations
- Personalized recommendations based on weather conditions

## Docker Setup

### Prerequisites

- Docker and Docker Compose installed on your system
- OpenWeather API key (get one at [OpenWeatherMap](https://openweathermap.org/api))

### Quick Start

1. Clone this repository:
   ```
   git clone <repository-url>
   cd weather-tracker
   ```

2. Create a `.env` file from the template:
   ```
   cp .env.example .env
   ```

3. Edit the `.env` file and add your OpenWeather API key:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

4. Build and start the Docker container:
   ```
   docker-compose up -d
   ```

5. Access the application:
   ```
   http://localhost:5000
   ```

### Stopping the Container

To stop the container:
```
docker-compose down
```

### Viewing Logs

To view logs:
```
docker-compose logs -f
```

## Development Without Docker

If you want to run the application without Docker:

1. Navigate to the app directory:
   ```
   cd app
   ```

2. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Access the application:
   ```
   http://localhost:5000
   ```

## Accessing from Mobile Devices

To access from mobile devices on the same network:

1. Find your computer's IP address
2. Access the application using:
   ```
   http://your-computer-ip:5000
   ```

## License

[MIT License](LICENSE)
