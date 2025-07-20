# LLM Financial PDF Agent

This project demonstrates an intelligent document analysis agent built using:
- [Pydantic AI](https://github.com/pydantic/pydantic-ai) for agent orchestration
- [LLMLingua](https://github.com/microsoft/LLMLingua) for context compression
- PDF parsing for financial news and investigative reports

The agent can extract and reason over complex financial events from PDFs, compress them intelligently using LLMLingua, and provide structured, fact-checked responses via an OpenAI GPT-4o backend.

## Features

- Retrieve and parse financial PDFs
- Compress long context using LLMLingua's GPT2-Dolly model
- Answer user questions with structured, explainable outputs
- Inject contextual instructions like today's date for dynamic prompts

## Use Case

Ideal for financial analysts, auditors, or journalists looking to investigate large volumes of financial documents and extract relevant insights quickly.

## Project Structure

```

.
├── main.py                  # Entry point for running the agent
├── agent.py                 # Agent orchestration and system instructions
├── retriever.py             # PDF text extractor
├── docs/                    # Place your PDF documents here
└── requirements.txt         # Python dependencies

````

## Quickstart

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/llm-financial-pdf-agent.git
   cd llm-financial-pdf-agent
    ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Add a financial PDF**
   Place your PDF inside the `docs/` folder. Example used in the code:

   ```
   docs/The Saga of the Jane Street Trading Scandal - Capitalmind.pdf
   ```

4. **Run the agent**

   ```bash
   python main.py
   ```

## Sample Query

```
By what ways the market was rigged?
```

## Output Schema

The response contains:

* `answer`: Natural language response to the query
* `input_token_count`: Tokens used in the prompt
* `output_token_count`: Tokens used in the answer
* `is_query_answered`: Whether the answer is complete and accurate
* `explanation`: Rationale for token usage

