# Model Types

For this skill, model classification should start from the user task and then map to the Agently implementation:

- plain text chat or generation -> usually maps to `chat`
- traditional completions endpoint -> maps to `completions`
- image understanding / visual Q&A / OCR -> belongs to the VLM scenario, but in Agently it is implemented as `chat + attachment()`

The most important boundary is: **VLM is a user-facing scenario classification, not a separate `model_type` in Agently.**

## 1. Chat LLM

In `OpenAICompatible.generate_request_data()`:

- when `model_type == "chat"`, the primary request field is `messages`
- message content comes from `Prompt.to_messages(...)`

Good fit for:

- conversation
- instruction following
- structured generation
- tool calling
- most modern OpenAI-compatible models

## 2. Completions LLM

In `OpenAICompatible.generate_request_data()`:

- when `model_type == "completions"`, the primary request field is `prompt`

Good fit for:

- services that explicitly require an old-style completion endpoint
- compatibility with older completion-oriented APIs

Default advice:

- if the provider does not explicitly require `/completions`, try `chat` first

## 3. VLM

If the user is asking for any of these tasks, it should usually be treated as a VLM scenario:

- image recognition
- visual question answering
- OCR
- mixed text-and-image understanding

In Agently, the implementation pattern is:

- there is no `vlm` requester `model_type`
- when `attachment` is present, `OpenAICompatible.__init__()` automatically turns on `rich_content`
- `PromptGenerator.to_messages(..., rich_content=True)` merges attachments into the message payload

This means:

- VLM is not a separate endpoint model family in Agently
- you do not set `model_type="vlm"`
- VLM success usually depends on:
  - whether the selected model actually supports vision
  - whether the provider accepts the attachment format
  - whether the image URL is reachable

## 4. Attachment Forms

From `prompt.py`:

- `attachment()` accepts a dict, a list, or values that can be converted into text content
- common VLM forms include:
  - `{"type": "text", "text": "..."}`
  - `{"type": "image_url", "image_url": {"url": "https://..."}}`

## 5. Why Embeddings Are Not Included Here

Although the requester also supports `model_type == "embeddings"`, it does not belong in this skill because the workflow is too different:

- the primary field is `input`
- it defaults to non-streaming
- the result is primarily vectors, not text generation
- it is mainly used for knowledge base, retrieval, and similarity workflows

Embeddings should therefore stay in a separate skill.

## 6. Default Decision Rules

- text generation only: usually map to `chat`
- explicit completion endpoint requirement: map to `completions`
- image understanding, OCR, or similar: treat as a VLM scenario, then implement as `chat + attachment()`
- vector generation: out of scope here
