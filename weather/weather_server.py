import os
import requests
from typing import Literal
from loguru import logger
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

class OutfitAdvisorServer:
    def __init__(self, name: str = "Outfit Advisor Server"):
        self.mcp = FastMCP(name)
        logger.info(f"Initializing MCP server: {name}")
        self.register_tools()

    def register_tools(self):
        @self.mcp.tool()
        def suggest_outfit(temperature_c: float, weather: Literal["sunny", "rainy", "cloudy", "snowy"]) -> str:
            """
            Suggest an outfit based on temperature and weather condition.
            """
            logger.info(f"Received request with temperature={temperature_c}°C and weather='{weather}'")

            if temperature_c > 30:
                outfit = "wear shorts and a tank top"
            elif 20 < temperature_c <= 30:
                outfit = "wear a t-shirt and jeans"
            elif 10 < temperature_c <= 20:
                outfit = "wear a long-sleeve shirt and jacket"
            elif 0 < temperature_c <= 10:
                outfit = "wear a coat, scarf, and warm pants"
            else:
                outfit = "wear thermal layers, gloves, and a heavy winter coat"

            if weather == "rainy":
                outfit += " with a waterproof jacket and umbrella"
            elif weather == "snowy":
                outfit += " with snow boots and gloves"

            recommendation = f"Based on the weather, you should {outfit}."
            logger.info(f"Outfit recommendation: {recommendation}")
            return recommendation

        @self.mcp.tool()
        def weather_tool(location: str) -> str:
            """
            Provides current weather information for a given location using OpenWeatherMap API.
            """
            logger.info(f"Fetching weather for location: {location}")
            api_key = os.getenv("OPENWEATHERMAP_API_KEY")
            if not api_key:
                logger.error("OPENWEATHERMAP_API_KEY is not set in environment.")
                return "API key is missing. Cannot fetch weather."

            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()

                if data.get("cod") == 200:
                    temp = data["main"]["temp"]
                    description = data["weather"][0]["description"]
                    # result = f"The weather in {location} is currently {description} with a temperature of {temp}°C."
                    result = f"The weather in {location} is currently {description} with a temperature of {temp}F."
                    logger.info(result)
                    return result
                else:
                    error_msg = data.get("message", "unknown error")
                    logger.warning(f"Weather API error for {location}: {error_msg}")
                    return f"Sorry, I couldn't find weather information for {location}."
            except requests.RequestException as e:
                logger.error(f"Network error: {e}")
                return f"Failed to retrieve weather data: {str(e)}"

    def run(self, transport: str = "stdio"):
        logger.info(f"Starting MCP server with transport: {transport}")
        self.mcp.run(transport=transport)


if __name__ == "__main__":
    server = OutfitAdvisorServer()
    server.run()
