import asyncio
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langchain.agents import create_agent

load_dotenv()

async def main():
    client = MultiServerMCPClient({
        "github": {
            "url": "https://api.githubcopilot.com/mcp/",
            "transport": "streamable_http",
            "headers": {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
        }
    })

    tools = await client.get_tools()
    # for tool in tools:
    #     print(tool.name)
    llm = ChatOllama(model="gpt-oss:120b-cloud")
    agent = create_agent(llm, tools)

    result = await agent.ainvoke({
        "messages": [("user", "Using my authenticated GitHub account, give me information about my latest repository enterprise-knowledge-assistant in detail")]
    })

    print(result["messages"][-1].content)

asyncio.run(main())