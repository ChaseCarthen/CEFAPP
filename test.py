import asyncio
from dotenv import load_dotenv
load_dotenv()
from browser_use import Agent
from browser_use.llm import ChatOllama
from browser_use.browser import BrowserProfile, BrowserSession
import pathlib
import os

SCRIPT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
agent_dir = SCRIPT_DIR / 'test_no_thinking'
agent_dir.mkdir(exist_ok=True)

browser_profile = BrowserProfile(headless=False)
browser_session = BrowserSession(browser_profile=browser_profile)

async def main():
    agent = Agent(
        task="find information on one close ended funds on google. Save your results to a file. Then you are done.",
        llm=ChatOllama(model="gemma3n:e4b"),
        file_system_path=str(agent_dir / 'fs'),
        #browser_session=browser_session
    )
    await agent.run()

asyncio.run(main())
