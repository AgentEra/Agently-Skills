# Independent model uses and media composition

Development scope: `feature/model-capabilities` and its 4.2 forward sync.
Check installed API availability; these additions are not a released-version promise.

Configure `llm`, `vlm`, `stt`, `tts`, `embeddings`, and `ocr` independently with
`{"provider": ..., "model": ..., "base_url": ..., "api_key": ...}` or an exclusive
`{"model_key": "pool-alias"}`. ModelPool remains the resolver. Same-provider uses
have independent credentials, headers and options. Explicit request model_key
wins over llm. The 4.1 provider namespace remains a compatibility fallback;
provider protocol configuration itself remains supported for atomic requests.

```python
agent.set_settings("vlm", {"provider": "OpenAICompatible", **vision_connection, "model": vision_model})
agent.set_settings("llm", {"provider": "OpenAICompatible", **text_connection, "model": text_model})
result = await (agent.image("note.png", question="Read the note carefully.")
    .input("Where is Hammond?")
    .output({"location": str, "evidence": str})
    .async_get_data())
```

Image mode defaults to vlm. With both profiles, ordinary image tasks use VLM
visual evidence -> LLM final output; with only one, it produces the final output
directly. input/info/instruct/output do not change this topology. question is local
to one image call, and repeated calls append ordered groups. Multiple images may
need joint comparison; do not split those into unrelated descriptions.
`mode="llm"` passes originals to a vision-capable LLM. `mode="ocr"` requires
an OCR model/service, then LLM for reasoning. The OCR role can reuse
OpenAICompatible for compatible services such as oMLX serving GLM-OCR or
PaddleOCR; MistralOCR adapts a different service protocol. Choose a Requester
by protocol, not by model name. Missing/failed
capabilities never silently switch providers. vision=False rejects original-image
input; unknown model support is determined by the provider, not model-name rules.

Execution `.vlm_only(True)` before start explicitly selects configured VLM as
final producer. It conflicts with llm/ocr image modes. `.async_to_text()` / to_text
select direct image processing, even with two profiles; input/question/output
still apply. get_text is an ordinary result reader. No question/task means
image description plus readable text and explicit uncertainty. Direct OCR only
extracts text and rejects question/input/output reasoning requests.
`async_to_text(max_retries=0)` / `to_text(max_retries=0)` disables shared
Execution repair retries; the default remains 3.

Audio retains AudioModelRequest/AudioCapability ownership. Explicit use_audio
bindings win over stt/tts role configuration. Direct async_stt/async_tts are
independent conversion operations. Keyword input(file=..., type="audio") declares
finite STT input for one Execution; input({"type":"audio", "file":...}) remains
business data. No implicit microphone, download, conversion or playback.

```python
execution = agent.input(file="question.wav", type="audio").instruct("Answer briefly.")
speech = await execution.async_say(scope="final")
text = await execution.async_get_text()  # Same result, no repeated inference
```

say defaults to final; scope=all includes public intermediate natural language
and final text. Raw model deltas, reasoning, tools/JSON fragments are excluded.
Structured final results use the existing text projection, which can be JSON.
stream_say selects complete SpeechResult segments independently of scope; use
`async with execution.stream_say(scope="all") as stream`. Closing an owned
stream cancels unfinished work. Audio already delivered cannot be retracted;
failed/partial delivery is not implicitly replayed. Repeated same-argument say
reads cache within one revision; explicit rework can produce new speech.
Pending audio/bound capabilities require explicit snapshot rebinding and do not
claim built-in save/load support. Rework reuses successful source evidence.

async_embed returns ordered list[list[float]], including one row for one input;
missing indexes, inconsistent dimensions and non-finite values fail. It never
migrates an existing vector index or changes that index's embedding identity.

Every Agent task goes through Execution, even direct. TriggerFlow owns media
stage/retry edges; atomic requesters own protocols. Successful predecessors are
reused and failed stages consume the final-production retry allowance.
get_meta()["media"] records source stages; audio is not unified token billing.
Use protocol fixtures for routing/lifecycle tests and real models plus independent
semantic review for quality. Local-model observations do not prove general OCR,
vision, acoustic quality, latency or model capability.
