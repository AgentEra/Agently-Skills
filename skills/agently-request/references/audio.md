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

Use `async with audio.stream_tts(...) as chunks` or
`async with audio.stream_stt(...) as events` for scoped output consumption.
OMLX supports WAV output streaming and uploaded-file transcript delta/done SSE.
Bytes chunks are not independent WAV files; done text replaces the accumulated
transcript rather than being appended. Early exit/cancellation closes transport;
STT EOF without done is failure. A clean byte-stream end is not semantic quality proof.
The generic OpenAICompatible audio driver declares complete TTS/STT only.

Continuous audio input is a different capability: `stream_stt_input` accepts an
async byte source plus PCMFormat. Custom drivers can implement it; bundled drivers
currently report unsupported before reading input. Do not simulate realtime by
buffering the whole source. An installed ASR model or available server WebSocket
route does not establish an implemented/accepted client-model combination.

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
