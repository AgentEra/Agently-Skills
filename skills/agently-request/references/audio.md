# Independent audio capability

Version scope: Agently 4.1.4.8 development; do not recommend these APIs on older
installed releases. Audio is not a text Prompt/ensure/auto_continue mode.

```python
import os
from agently import Agently, AudioInput

audio = Agently.create_audio_request(
    driver="OMLX",
    base_url=os.environ["AUDIO_BASE_URL"],
    api_key=os.getenv("AUDIO_API_KEY", ""),
    tts_model=os.environ["AUDIO_TTS_MODEL"],
    stt_model=os.environ["AUDIO_STT_MODEL"],
)
agent = Agently.create_agent()
agent.use_audio(audio)
# In an async function:
speech = await agent.async_tts("Welcome.", voice=os.getenv("AUDIO_VOICE"))
transcript = await agent.async_stt(AudioInput(speech.data))
```

Use `tts/stt` for sync scripts, `async_tts/async_stt` in async code. The standalone
audio object exposes the same operations; each call dispatches a new request.
STT accepts a path or AudioInput with actual filename/media type. No implicit
recording, playback, remote download, conversion or file writes. Text model
settings, Agent session history and output schemas are not inherited.

SpeechOptions owns response_format/speed/language/instructions; TranscriptionOptions
owns language/prompt. `extra` passes provider-specific options but cannot override
reserved request fields. Model support remains provider-specific. No automatic
retry/fallback, particularly after partial delivery; use application-owned total
deadlines and admission. HTTP timeout is an inactivity limit, not a workflow budget.

## Continuous consumption: auto break selects output

All four methods are also exposed directly on a bound Agent:

| Method | Source | Yield |
|---|---|---|
| stream_tts | str / nonblocking Iterable[str] / AsyncIterable[str] | continuous headerless PCM bytes |
| stream_tts_with_auto_break | same text input/segmentation | independent complete SpeechResult audio segments |
| stream_stt | AsyncIterable[bytes] + explicit PCMFormat | finalized TranscriptBlock per audio window |
| stream_stt_with_auto_break | same audio input | TranscriptSegment split after recognition at text punctuation |

```python
from agently import TextSegmentOptions, PCMFormat, TranscriptionStreamOptions

async with agent.stream_tts(
    text_chunks, segments=TextSegmentOptions(expect_chars=300),
) as stream:
    fmt = stream.audio_format
    async for pcm in stream:
        await configured_pcm_sink.write(pcm)

async with agent.stream_stt_with_auto_break(
    pcm_chunks, audio_format=PCMFormat(sample_rate=16000),
    stream_options=TranscriptionStreamOptions(window_seconds=5, max_pending_chars=1000),
) as stream:
    async for segment in stream:
        print(segment.text, segment.reason)
```

Use async with for scoped cleanup. Do not reuse exhausted iterators. Auto break
does not require pre-segmented input. Both TTS modes greedily group text:
paragraph/newline before sentence before comma, rightmost within the best
priority, configurable length/tolerance and 100-character grace before a
no-punctuation hard cut. EOF flushes a short tail; idle input is not EOF.
TextSegmentOptions defaults to 300 code points, 0.1 tolerance and 100 grace.
A fresh typed TextSegmenter can replace per-stream boundary selection.

Continuous TTS parses complete PCM s16le WAV into samples, or accepts explicitly
declared raw PCM. stream.audio_format is ready on context entry for nonempty
input (entry waits for the first synthesis); empty input has no inferred format.
Later format mismatches fail: no implicit resampling or universal codec support.
chunk_bytes defaults to 8192, aligned to complete frames. Auto break returns
self-contained formats supported by the base driver, such as WAV/MP3, not bare
PCM. Do not concatenate independent WAV files or save headerless PCM as WAV
without explicit container encoding. No gapless playback/prosody guarantee.

STT windows default to 5 seconds and use sample-derived offsets. Arbitrary
transport packets may split frames; incomplete EOF frames fail without padding.
TranscriptBlock has text/index/start_seconds/end_seconds/model/language.
Base TranscriptResult.duration is provider-origin; oMLX currently reports
processing time, not audio duration. Windowed ASR can omit/repeat words or
insert punctuation; do not silently repair it with keyword deduplication.

STT auto break buffers finalized text, not audio pauses or provisional deltas.
TranscriptSegment reasons distinguish sentence_end, limit and input_end; source
block indices are not precise word timestamps. No forced punctuation-restoration
model request. The default structural punctuation rules are not universal
semantic sentence detection; ASCII alphanumeric joins add a display space, not
split-word repair. Preserve source blocks when exact raw transcription matters.

Flow is pull-driven, one model request at a time, without unbounded prefetch.
Per-item input limits and pending-transcript limits are explicit options; errors
do not silently discard data. A capture adapter must handle/report overflow:
backpressure cannot pause a real microphone. No implicit recording/playback,
shared-device close, retries after partial speech, or durable stream recovery.
Do not automatically subscribe to Agent thinking/tool events or text that
validate/retry may replace. Await final text for final guarantees; live playback
is irreversible and must be an explicit caller choice.

## Provider-native interaction remains separate

audio.supported_operations describes composition from base tts/stt;
audio.driver.supported_operations describes native transport support. The generic
OpenAICompatible base endpoints suffice for composed streams. OMLX additionally
supports native WAV output and uploaded-file transcript delta/done SSE:
audio.driver.stream_tts(SpeechRequest(...)) / stream_stt(TranscriptionRequest(...)).
Native done replaces deltas; EOF without done is failure. Bytes are transport
chunks, not independent files. Each scope closes its transport.

Native continuous input remains driver.stream_stt_input(...); built-ins still
report unsupported. Windowed framework consumption is not a native realtime-ASR
session, and installed models/server routes alone do not establish such support.

Register replaceable AudioModelRequester classes through PluginManager; or bind
any complete AudioCapability implementation with use_audio. Registration alone
does not mount an Agent. Missing audio raises; use_audio(None) unbinds future calls.
Execution plugins declare required_agent_capabilities=("audio",) and obtain static
or dynamic dependencies through require_agent_capability before using them.
Already captured bindings do not drift when Agent configuration changes. Whole
custom Execution implementations must honor the same contract. Presence is not
authorization, health, backend operation support or required-Action call evidence.
Extra-capability snapshots/rebinding and text-model budget/telemetry integration
are not supported by this initial slice. Do not invent those guarantees.
