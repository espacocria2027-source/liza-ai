from agents.agent_manager import agent_manager

from agents.chat_agent import ChatAgent
from agents.programmer_agent import ProgrammerAgent
from agents.android_agent import AndroidAgent


agent_manager.register(ChatAgent())
agent_manager.register(ProgrammerAgent())
agent_manager.register(AndroidAgent())