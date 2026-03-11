# Source Map

This reference points to the most relevant public Agently sources for embeddings work.

## 1. Core implementation files

- [OpenAICompatible requester](https://github.com/AgentEra/Agently/blob/main/agently/builtins/plugins/ModelRequester/OpenAICompatible.py)
  The `embeddings` request shape, `path_mapping`, `stream` default, input sanitization, request-body merging, and final payload mapping live here.
- [AgentlyResponseParser](https://github.com/AgentEra/Agently/blob/main/agently/builtins/plugins/ResponseParser/AgentlyResponseParser.py)
  Converts the embedding provider payload into parsed vector data.
- [ModelRequest core](https://github.com/AgentEra/Agently/blob/main/agently/core/ModelRequest.py)
  Entry points for `start()`, `async_start()`, `get_data()`, and `get_response()`.
- [Agent core](https://github.com/AgentEra/Agently/blob/main/agently/core/Agent.py)
  Agent-level aliases for sync and async embeddings calls live here.
- [DataFormatter](https://github.com/AgentEra/Agently/blob/main/agently/utils/DataFormatter.py)
  Sanitization and serializable request-data conversion live here.
- [Chroma integration](https://github.com/AgentEra/Agently/blob/main/agently/integrations/chromadb.py)
  Shows how an embedding agent is turned into a vector-store embedding function.

## 2. Example files

- [Knowledge base step-by-step example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/09-knowledge_base.py)
  This example shows the common split between document indexing and later query-time retrieval.
- [Simple Agently Chroma example](https://github.com/AgentEra/Agently/blob/main/examples/chromadb/agently_chromadb.py)
- [Ollama embeddings + Chroma example](https://github.com/AgentEra/Agently/blob/main/examples/chromadb/agently_ollama_embedding_chromadb.py)
- [Auto-loop example with embeddings handoff](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/12-auto_loop.py)

## 3. Test files

- [OpenAICompatible requester test](https://github.com/AgentEra/Agently/blob/main/tests/test_plugins/test_model_requester/test_openai_compatible.py)
- [Request core tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_request.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
- Model settings docs: `https://agently.tech/docs/en/model-settings.html`
- OpenAI API format docs: `https://agently.tech/docs/en/openai-api-format.html`
- Model response overview: `https://agently.tech/docs/en/model-response/overview.html`
