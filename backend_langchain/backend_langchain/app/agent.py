from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

from app.llm import llm
from app.rag import rag_search
from app.services.aws_tools import (
    list_s3_buckets,
    describe_ec2_instances,
    get_ecs_service_status,
    list_eks_clusters,
    describe_eks_cluster,
)
from app.services.codepipeline_tools import get_pipeline_status, list_pipelines
from app.services.ssm_tools import get_ssm_parameter, list_ssm_parameters, put_ssm_parameter

# ─────────────────────────────────────────────
# All tools the agent can use
# ─────────────────────────────────────────────
tools = [
    # RAG
    rag_search,

    # S3
    list_s3_buckets,

    # EC2
    describe_ec2_instances,

    # ECS
    get_ecs_service_status,

    # EKS
    list_eks_clusters,
    describe_eks_cluster,

    # CodePipeline
    get_pipeline_status,
    list_pipelines,

    # SSM / Environment Variables
    get_ssm_parameter,
    list_ssm_parameters,
    put_ssm_parameter,
]

# ─────────────────────────────────────────────
# System prompt — tells the agent who it is
# and how to behave
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are a helpful DevOps assistant for an engineering team.
You help developers check deployment status, pipeline status, environment variables,
and answer questions about the AWS infrastructure.

You have access to the following tools:
{tools}

Rules:
- Always use a tool to get live data rather than guessing
- For questions about internal docs, runbooks, or service ownership → use rag_search
- For pipeline status questions → use get_pipeline_status (if you know the name) or list_pipelines first
- For ECS questions → use get_ecs_service_status
- For EKS questions → use list_eks_clusters then describe_eks_cluster
- For environment variables → use get_ssm_parameter or list_ssm_parameters
- NEVER apply production changes without showing the approval message
- If you don't know a pipeline/service name, ask the user or list available ones
- Always give a clear, human-friendly response — not raw JSON

Use this format strictly:

Question: the input question you must answer
Thought: think about what to do
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)

CRITICAL: When you are ready to respond to the user, you MUST use this exact format:
Thought: I now know the final answer
Final Answer: the final answer to the original question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(SYSTEM_PROMPT)

# ─────────────────────────────────────────────
# ReAct agent — thinks in a loop, picks tools
# ─────────────────────────────────────────────
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

# Memory — remembers last 10 messages per session
memory = ConversationBufferWindowMemory(
    k=10,
    memory_key="chat_history",
    return_messages=True
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=False,           # Disable verbose to stop the StdOutCallback warning
    handle_parsing_errors=True,
    max_iterations=25,       # prevent infinite loops (increased from 8 because local mistral takes many steps)
    return_intermediate_steps=False,
)


from app.context import current_account_id

def run_agent(user_query: str, account_id: str = None) -> str:
    """Main entry point — takes a user question, returns a string answer."""
    # Set the current account in a contextvar for tools to read
    if account_id:
        current_account_id.set(account_id)
    else:
        current_account_id.set("default")
        
    try:
        result = agent_executor.invoke({"input": user_query})
        return result.get("output", "I was unable to process that request.")
    except Exception as e:
        return f"Agent error: {str(e)}"
