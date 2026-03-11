# Source Map

This reference points to the most relevant public Agently sources for output-control work.

## 1. Core implementation files

- [ModelRequest core](https://github.com/AgentEra/Agently/blob/main/agently/core/ModelRequest.py)
  Entry points for `.output(...)`, `get_response()`, `get_data()`, `get_data_object()`, and the generator shortcuts.
- [ModelResponse core](https://github.com/AgentEra/Agently/blob/main/agently/core/ModelResponse.py)
  Creates the response snapshot and starts the model-response pipeline.
- [ModelResponseResult core](https://github.com/AgentEra/Agently/blob/main/agently/core/ModelResponseResult.py)
  Implements `ensure_keys`, retries, response getters, and the post-response result lifecycle.
- [AgentlyResponseParser](https://github.com/AgentEra/Agently/blob/main/agently/builtins/plugins/ResponseParser/AgentlyResponseParser.py)
  Collects `text_result`, `parsed_result`, `meta`, `errors`, and structured streaming events.
- [AgentlyPromptGenerator](https://github.com/AgentEra/Agently/blob/main/agently/builtins/plugins/PromptGenerator/AgentlyPromptGenerator.py)
  Generates the dynamic output model and serializable output schema.
- [Prompt data model](https://github.com/AgentEra/Agently/blob/main/agently/types/data/prompt.py)
  Defines `PromptModel`, `output_format` inference, and prompt-slot validation.
- [Response data model](https://github.com/AgentEra/Agently/blob/main/agently/types/data/response.py)
  Defines response event types and the `StreamingData` model.
- [GeneratorConsumer](https://github.com/AgentEra/Agently/blob/main/agently/utils/GeneratorConsumer.py)
  Powers multiple response consumers with history replay and no second request.
- [FunctionShifter](https://github.com/AgentEra/Agently/blob/main/agently/utils/FunctionShifter.py)
  Wraps async response methods and generators for sync-facing convenience APIs.
- [DataPathBuilder](https://github.com/AgentEra/Agently/blob/main/agently/utils/DataPathBuilder.py)
  Path conversion helpers used by `ensure_keys` and structured streaming.
- [StreamingJSONParser](https://github.com/AgentEra/Agently/blob/main/agently/utils/StreamingJSONParser.py)
  Incrementally parses streamed JSON into `StreamingData` events.

## 2. Example files

- [Output format control example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/03-output_format_control.py)
- [Response result example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/05-response_result.py)
- [Streaming example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/06-streaming.py)
- [Async streaming print example](https://github.com/AgentEra/Agently/blob/main/examples/basic/streaming_print.py)
- [ensure_keys example](https://github.com/AgentEra/Agently/blob/main/examples/basic/ensure_keys_in_output.py)
- [Instant streaming example](https://github.com/AgentEra/Agently/blob/main/examples/basic/instant_for_mutiple_list_items.py)
- [Specific streaming example](https://github.com/AgentEra/Agently/blob/main/examples/basic/specific_streaming.py)
- [Prompt mappings example](https://github.com/AgentEra/Agently/blob/main/examples/basic/prompt_mappings.py)

## 3. Test files

- [Response tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_response.py)
- [Request tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_request.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
- Async support docs: `https://agently.tech/docs/en/async-support.html`
- Output control overview: `https://agently.tech/docs/en/output-control/overview.html`
- Output format docs: `https://agently.tech/docs/en/output-control/format.html`
- ensure_keys docs: `https://agently.tech/docs/en/output-control/ensure-keys.html`
- Order and dependencies docs: `https://agently.tech/docs/en/output-control/order-and-deps.html`
- Instant streaming docs: `https://agently.tech/docs/en/output-control/instant-streaming.html`
- Model response overview: `https://agently.tech/docs/en/model-response/overview.html`
- Result data docs: `https://agently.tech/docs/en/model-response/result-data.html`
- Streaming docs: `https://agently.tech/docs/en/model-response/streaming.html`

## 5. External Industry References

- OpenAI streaming responses guide: `https://platform.openai.com/docs/guides/streaming-responses`
  Useful for the general latency and responsiveness rationale behind streaming.
- Vercel AI SDK `streamObject` reference: `https://ai-sdk.dev/docs/reference/ai-sdk-core/stream-object`
  Useful for partial-object streaming and array-element streaming patterns.
- Vercel AI SDK object-generation docs: `https://ai-sdk.dev/docs/ai-sdk-ui/object-generation`
  Useful for streamed structured UI patterns.
- Vercel AI SDK Next.js stream-object example: `https://ai-sdk.dev/cookbook/next/stream-object`
  Useful for the "large schema or slow object generation should stream to the client" pattern.
- Anthropic fine-grained tool streaming: `https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/fine-grained-tool-streaming`
  Useful for the broader case where large structured or tool-parameter payloads should start flowing before full buffering and validation.
