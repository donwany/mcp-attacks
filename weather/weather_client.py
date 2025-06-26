import asyncio
import os
import json
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import List, Dict, Any
import anthropic
from dotenv import load_dotenv
import subprocess

load_dotenv()


class LLMClientClaude:
    def __init__(self, model: str = "claude-sonnet-4-20250514", temperature: float = 0.2, max_tokens: int = 250):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def send_message(self, system_message: str, user_message: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            system=system_message,
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.content[0].text.strip()


class PromptBuilder:
    @staticmethod
    def build_tool_prompt(query: str, tools: List[Any]) -> str:
        tools_description = "\n".join(
            [f"- {tool.name}, {tool.description}, {tool.inputSchema}" for tool in tools]
        )
        return (
            "You are a helpful assistant with access to these tools:\n\n"
            f"{tools_description}\n"
            "Choose the appropriate tool based on the user's question.\n"
            f"User's Question: {query}\n"
            "If no tool is needed, reply directly.\n\n"
            "IMPORTANT: When you need to use a tool, you must ONLY respond with "
            "the exact JSON object format below, nothing else:\n"
            "{\n"
            '  "tool": "tool-name",\n'
            '  "arguments": {\n'
            '    "argument-name": "value"\n'
            "  }\n"
            "}\n"
        )


class MCPToolExecutor:
    def __init__(self, command: str = "python", args: List[str] = None):
        if args is None:
            args = ["/home/ts75080/Desktop/MCP_research_paper/mcp/paper_code/weather_server.py"]
        self.server_params = StdioServerParameters(command=command, args=args)

    async def execute(self, query: str, llm_client: LLMClientClaude):
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                print(f"Available tools: {tools}")

                prompt = PromptBuilder.build_tool_prompt(query, tools.tools)
                llm_response = llm_client.send_message(
                    "You are an intelligent assistant. You will execute tasks as prompted.",
                    prompt
                )

                print(f"LLM Response:\n{llm_response}\n")

                try:
                    tool_call = json.loads(llm_response)
                    result = await session.call_tool(tool_call["tool"], arguments=tool_call["arguments"])
                    print(f"Suggested outfit: {result.content[0].text}")
                except Exception as e:
                    print(f"Error parsing or executing tool call: {e}")


async def main():
    queries = ["What should I wear today if it's 8°C and snowy?", "What is the temperature in Dallas?"]

    llm_client = LLMClientClaude()
    executor = MCPToolExecutor()
    for query in queries:
        await executor.execute(query, llm_client)


if __name__ == "__main__":
    asyncio.run(main())
