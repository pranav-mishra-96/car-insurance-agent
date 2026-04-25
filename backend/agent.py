import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage

from tools import (
    calculate_premium_estimate,
    check_coverage_requirements,
    explain_claim_process,
    compare_coverage_types,
)
from prompts import SYSTEM_PROMPT


def build_agent() -> AgentExecutor:
    """Build and return the LangChain agent executor.

    Wires together:
    - ChatOpenAI (the LLM)
    - Tools (the 4 insurance tools)
    - ConversationBufferMemory (remembers chat history)
    - ChatPromptTemplate (structures the prompt)
    - AgentExecutor (runs the ReAct loop)
    """

    # The LLM
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.3,
        streaming=True,
    )

    # All 4 tools
    tools = [
        calculate_premium_estimate,
        check_coverage_requirements,
        explain_claim_process,
        compare_coverage_types,
    ]

    # Memory — keeps track of conversation history across turns
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )

    # Prompt template — structures how messages are sent to the LLM
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create the agent — uses OpenAI function calling to pick tools
    agent = create_openai_functions_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

    # AgentExecutor — runs the ReAct loop
    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        return_intermediate_steps=True,
    )