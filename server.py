from mcp.server.fastmcp import FastMCP
from loguru import logger
from typing import Union


class BMIServer:
    def __init__(self, name: str = "BMI Server"):
        self.mcp = FastMCP(name)
        logger.info(f"Initializing MCP server: {name}")
        self.register_tools()

    def register_tools(self):
        @self.mcp.tool()
        def calculate_bmi(weight_kg: float, height_m: float) -> str:
            """
            Calculate BMI given weight in kg and height in meters.
            """
            logger.info(f"Received request to calculate BMI with weight={weight_kg}kg and height={height_m}m")
            if height_m <= 0:
                logger.error("Invalid height provided: must be greater than zero.")
                raise ValueError("Height must be greater than zero.")
            bmi = weight_kg / (height_m ** 2)
            result = f"The BMI is {bmi:.2f}"
            logger.info(f"Computed BMI: {result}")
            return result

    def run(self, transport: str = "stdio"):
        logger.info(f"Starting MCP server with transport: {transport}")
        self.mcp.run(transport=transport)


if __name__ == "__main__":
    server = BMIServer()
    server.run()
