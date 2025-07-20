import asyncio
from datetime import date

from llm_lingua_pydantic_ai.agent import DataSources, agent
from llm_lingua_pydantic_ai.retriever import PdfRetriever

async def main():
    retriever = PdfRetriever(
        "../docs/The Saga of the Jane Street Trading Scandal - Capitalmind.pdf"
    )
    data_sources = DataSources(retriever=retriever, today_date=date.today())
    result = await agent.run("By what ways the market was rigged?", deps=data_sources)
    print(result.output)

if __name__ == "__main__":
    asyncio.run(main())

