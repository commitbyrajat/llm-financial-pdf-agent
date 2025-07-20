from dataclasses import dataclass
from datetime import date

from llmlingua import PromptCompressor
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from llm_lingua_pydantic_ai.retriever import PdfRetriever


class Answer(BaseModel):
    """
    Schema representing the structured response returned by the agent.
    """
    answer: str = Field(
        description="The generated answer in response to the user's query."
    )
    input_token_count: int = Field(
        description="Total number of tokens present in the input prompt."
    )
    output_token_count: int = Field(
        description="Total number of tokens used in generating the answer."
    )
    is_query_answered: bool = Field(
        description="True if the generated answer accurately satisfies the query; False otherwise."
    )
    explanation:str = Field(
        description="Explain the numerical calculation of identifying input and output tokens by using numbers"
    )


@dataclass
class DataSources:
    """
    Data sources and runtime dependencies available to the agent.
    """
    retriever: PdfRetriever
    today_date: date


# Initialize agent with specific system instructions
agent = Agent(
    "openai:gpt-4o",
    deps_type=DataSources,
    output_type=Answer,
    system_prompt=(
        "You are a financial investigation assistant trained to answer queries with precision. "
        "Provide fact-based, well-structured responses derived from relevant financial documents. "
        "Always verify the factual consistency of your answer to avoid hallucinations."
    )
)


@agent.instructions
async def add_today_date(ctx: RunContext[DataSources]) -> str:
    """
    Injects the current date into the system prompt for contextual awareness.
    """
    today_date = ctx.deps.today_date
    return f"Today's date is {today_date}."


@agent.tool
async def get_financial_news_docs(ctx: RunContext[DataSources]):
    """
    Retrieves the latest financial news documents from the configured PDF retriever.

    Returns:
        str: Concatenated string of all retrieved financial documents.
    """
    news =  "".join(doc for doc in ctx.deps.retriever.get_docs())
    # return news
    llm_lingua = PromptCompressor("lgaalves/gpt2-dolly", device_map="mps")
    compressed_prompt = llm_lingua.compress_prompt([news], instruction="", question="", target_token=200)
    return compressed_prompt["compressed_prompt"]
