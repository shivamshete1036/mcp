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
            "headers": {
                "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"
            }
        }
    })

    tools = await client.get_tools()

    # print("\nAvailable MCP Tools:")
    # for tool in tools:
    #     print(f"- {tool.name}")

    llm = ChatOllama(
        model="gpt-oss:120b-cloud"
    )

    agent = create_agent(
        llm,
        tools
    )

    prompt = (
    """
    Using my authenticated GitHub account, the owner is shivamshete1036,
   give me the content of app.py file of mcp repository and also summarize me the code in simple language of that file"

    """
        
    )

    result = await agent.ainvoke({
        "messages": [
            ("user", prompt)
        ]
    })

    print("\n" + "=" * 60)
    print("TOOL CALLS")
    print("=" * 60)

    for message in result["messages"]:

        # Check whether this message contains tool calls
        if hasattr(message, "tool_calls") and message.tool_calls:

            for tool_call in message.tool_calls:

                print("\nTool called:")
                print(f"Name: {tool_call['name']}")
                
                print("\nArguments:")
                print(tool_call["args"])


    # -----------------------------
    # Final Answer
    # -----------------------------
    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)

    print(result["messages"][-1].content)
    


if __name__ == "__main__":
    asyncio.run(main())