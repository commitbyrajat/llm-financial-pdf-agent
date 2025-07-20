# How a 51x Token Reduction Cut Our LLM Costs by 93% — Without Sacrificing Accuracy

> A sudden spike in GPT-4 usage pushed our LLM agent costs into the danger zone. Here's how token compression saved us — and how you can implement it in under 30 lines of code.

---

## The Backstory: A Cost Spike I Didn’t See Coming

I'm an AI Architect leading GenAI initiatives at my organization, focused on building internal tools that drive insights from large unstructured documents. One of those tools — a financial document Q\&A agent — recently became too successful for its own good.

The agent was designed to read through large PDFs like forensic financial reports or market scam disclosures and answer natural language questions. Users loved it. But then came the spike.

One morning, I noticed our GPT-4 token usage was up 6x overnight. On digging deeper, I realized the agent was processing massive PDFs, sometimes up to 50 pages long. Each query was consuming over **4,000 tokens** in input alone.

At \$0.03 per 1K tokens (input) and \$0.06 per 1K (output), our costs were spiraling out of control — over **\$500/month** projected for a single tool.

I needed a fix. Fast.

---

## Enter LLMLingua: Prompt Compression for Real-World LLM Use

That's when I discovered [LLMLingua](https://github.com/microsoft/LLMLingua), a lightweight prompt compressor from Microsoft. It doesn't summarize, paraphrase, or restructure — it selectively **filters** the most important text based on a given question.

It's a perfect fit for Q\&A tasks that rely on long documents where only 10–20% of the content is relevant to any one question.

---

## Before vs After: Token Stats and Cost Savings

Here’s what compression looked like on a real example:

**Question**: *"Who is the culprit of rigging the stock market?"*
**Document**: *The Saga of the Jane Street Trading Scandal – 50 pages PDF*

| Metric                | Without Compression | With Compression  |
| --------------------- | ------------------- | ----------------- |
| Input Tokens          | 4,047               | 160               |
| Output Tokens         | 103                 | 61                |
| Total Tokens          | 4,150+              | \~221             |
| Compression Factor    | —                   | **51x smaller**   |
| Cost per Query (est.) | \$0.124             | **\$0.0062**      |
| Savings per Query     | —                   | **\~93% cheaper** |

Now multiply that by 1,000 queries — and we’re talking **hundreds of dollars** in monthly savings.

---

## Did It Hallucinate?

Naturally, I was worried. Stripping context can often confuse LLMs, leading to hallucinations or vague replies.

So, I tested each query before and after compression.

**What I found surprised me** — the compressed answers were actually **more accurate** and **better aligned** to the question. Why? Because compression removed irrelevant background noise and focused the model on the most important details.

### Example

**Original Context**:

> "The trading desk at Jane Street executed timed trades to influence index prices..."

**After Compression**:

> "The scandal involved exploiting regulatory gaps to manipulate index settlement values..."

Same meaning. Fewer tokens. Sharper answer.

Every output was verified using a structured flag `is_query_answered = True`, built into our agent schema.

---

## How LLMLingua Works Under the Hood

LLMLingua performs **query-aware compression** in three steps:

1. **Token Scoring**: Uses a small LLM (like GPT-2 or Dolly) to score each sentence or token by relevance.
2. **Dynamic Filtering**: Keeps only the highest-scoring content, up to a target token count.
3. **Final Prompt**: Outputs a compressed version of the document — focused, minimal, and still accurate.

Because it keeps only what's *already there*, the factual consistency is preserved — unlike summarization-based methods that reword or merge concepts.

---

## The Minimal Integration: 10 Lines of Code

Here’s how I integrated it into my agent system:

```python
from llmlingua import PromptCompressor

compressor = PromptCompressor("lgaalves/gpt2-dolly", device_map="mps")

compressed = compressor.compress_prompt(
    [pdf_text],
    question="Who rigged the market?",
    target_token=200
)

print(compressed["compressed_prompt"])
```

In the full system, it lives inside an agent tool like this:

```python
@agent.tool
async def get_financial_news_docs(ctx: RunContext[DataSources]):
    news =  "".join(doc for doc in ctx.deps.retriever.get_docs())
    llm_lingua = PromptCompressor("lgaalves/gpt2-dolly", device_map="mps")
    return llm_lingua.compress_prompt(
        [news], instruction="", question="", target_token=200
    )["compressed_prompt"]
```
---

## Why We Chose `lgaalves/gpt2-dolly` for Compression

A critical part of LLMLingua’s effectiveness is the *compression model* it uses to identify and retain relevant context. For our implementation, we used:

**`lgaalves/gpt2-dolly`** — a fine-tuned GPT-2 model optimized for prompt compression and instruction-following.

### Why Not Use a Larger Model?

We initially considered using more powerful models like `gpt-neo` or `mistral`, but those added significant overhead and latency during compression. The goal was to run this step **locally and quickly** — before even calling the expensive GPT-4 endpoint.

That’s where `lgaalves/gpt2-dolly` shines:

* **Lightweight**: Runs fast on local hardware, even with just `device_map="mps"` on a Mac.
* **Effective**: Accurately identifies relevant text even in dense financial documents.
* **Aligned**: It’s trained to follow instructions and score segments based on their relevance to a question — ideal for LLMLingua’s ranking engine.

### How It Works with LLMLingua

LLMLingua doesn’t just blindly clip the text. It uses the compressor model (`lgaalves/gpt2-dolly`) to:

1. **Embed** each sentence or passage from the document.
2. **Score** each passage based on how well it aligns with the user’s query.
3. **Select** only the top-ranked passages that collectively fit within a target token budget.

That scoring + filtering is where `lgaalves/gpt2-dolly` plays a central role.

---

## Tech Stack Summary

The full stack looks like this:

* **LLM**: `openai/gpt-4o`
* **Agent Framework**: `pydantic-ai` with tool-based orchestration
* **Prompt Compression**: `LLMLingua` with `gpt2-dolly`
* **Retriever**: `pypdf`-based `PdfRetriever` class
* **Async Execution**: `asyncio` with lightweight task runners

All of it is open-source and production-ready.

---

## Full Code on GitHub

You can find the full implementation, including agent logic, retriever, and compression integration, at:

👉 **[github.com/commitbyrajat/llm-financial-pdf-agent](https://github.com/commitbyrajat/llm-financial-pdf-agent)**

Includes:

* Modular agent setup
* PDF ingestion with token counting
* Token-aware prompt compression
* Structured output with validation flags

---

## Final Thoughts: Compress Before You Prompt

If you're working with LLMs and long documents — especially in finance, legal, compliance, or research — **token compression isn’t optional**. It’s your best lever to reduce costs, latency, and context window errors.

What started as a panic-driven fix ended up becoming a best practice. We now compress **all long prompts** before sending them to GPT — and it’s saved us thousands in compute bills.

---

## Want to Try This?

Clone the full agent code here:
**[https://github.com/commitbyrajat/llm-financial-pdf-agent](https://github.com/commitbyrajat/llm-financial-pdf-agent)**

And if you're building something similar, feel free to reach out or fork and experiment.

— *Rajat Nigam, AI Architect*

---
