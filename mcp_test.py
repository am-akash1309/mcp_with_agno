from agno.models.google import Gemini
from dotenv import load_dotenv  
import os

load_dotenv(override=True)
google_api_key = os.getenv("GOOGLE_API_KEY")

gemini_15 = Gemini(id="gemini-1.5-flash", api_key=google_api_key)
gemini_20 = Gemini(id="gemini-2.0-flash", api_key=google_api_key)
gemini_25 = Gemini(id="gemini-2.5-pro", api_key=google_api_key)

import asyncio

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.mcp import MCPTools
from agno.utils.pprint import apprint_run_response


async def run_agent(message: str) -> None:
    async with MCPTools(
        "npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt"
    ) as mcp_tools:
        agent = Agent(
            model=gemini_15,
            tools=[mcp_tools],
            markdown=True,
            debug_mode=True,
        )

        response_stream = await agent.arun(message, stream=True)
        await apprint_run_response(response_stream, markdown=True)


if __name__ == "__main__":
    asyncio.run(
        run_agent(
            "What listings are available in Coimbatore for 1 person for 2 nights from 14 to 17 August 2025?"
        )
    )