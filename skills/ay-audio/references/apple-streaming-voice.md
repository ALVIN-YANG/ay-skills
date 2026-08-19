# Apple streaming voice reference

Use this reference after the main workflow identifies an Apple TTS playback or audio-graph problem.

## Boundary matrix

| Evidence | Likely boundary | Next check |
|---|---|---|
| Saved provider audio is already noisy | Provider request, voice, model, or service | Compare a fixed phrase, another voice, and provider metadata |
| Saved provider audio is clean; captured mixer is noisy | Parser, decoder, converter, buffer scheduling | Compare packet/sample boundaries and decode the same bytes independently |
| Provider and mixer are clean; app output is noisy | Output graph, route, lifecycle, competing engines | Play the artifact with a system player; stop capture/output engines one at a time |
| First turn works; later turn fails | Cancellation, stale callback, queue disposal, request ownership | Add turn IDs and log open/start/finish/stop for each owner |
| Noise appears at network chunk boundaries | Chunk-as-buffer scheduling or wrong framing | Coalesce chunks; confirm chunks are not independent files |

## Known-good PCM path

Prefer raw signed 16-bit little-endian PCM when the provider offers it. For a live-tested MiniMax WebSocket path, the request used `format: "pcm"`, `sample_rate: 32000`, and `channel: 1`; provider contracts can change, so verify a current live response before copying these values.

For 32 kHz mono PCM, use this contract:

```swift
AudioStreamBasicDescription(
    mSampleRate: 32_000,
    mFormatID: kAudioFormatLinearPCM,
    mFormatFlags: kLinearPCMFormatFlagIsSignedInteger | kLinearPCMFormatFlagIsPacked,
    mBytesPerPacket: 2,
    mFramesPerPacket: 1,
    mBytesPerFrame: 2,
    mChannelsPerFrame: 1,
    mBitsPerChannel: 16,
    mReserved: 0
)
```

Validate every chunk after transport decoding:

- Total bytes and every committed buffer must be divisible by `bytesPerFrame`.
- Expected duration is `bytes / (sampleRate × channels × bytesPerSample)`.
- Raw PCM has no WAV header. Do not prepend a header per chunk.
- Hex responses contain ASCII transport data; convert hex pairs to bytes once before playback.

## AudioQueue lifecycle

Allocate several reusable buffers once per utterance. Accumulate network fragments into a FIFO, fill whole buffers, and enqueue them. Begin playback only after roughly 0.4–0.8 seconds is queued, or when a shorter stream ends. The output callback returns a buffer for reuse; it must not allocate a new buffer for every fragment.

Track `inputFinished`, `buffersInFlight`, available buffers, pending bytes, started state, turn ID, and one completion continuation. Finish only when input is closed, pending bytes are empty, and all queued buffers have returned. Stop, dispose, and resume continuations exactly once.

Apple documents Audio Queue Services as the hardware and buffer manager, and its output callback as the point where a consumed buffer becomes reusable:

- [Audio Queue Services](https://developer.apple.com/documentation/audiotoolbox/audio-queue-services)
- [AudioQueueNewOutput](https://developer.apple.com/documentation/audiotoolbox/audioqueuenewoutput%28_%3A_%3A_%3A_%3A_%3A_%3A_%3A%29)
- [AudioQueueOutputCallback](https://developer.apple.com/documentation/audiotoolbox/audioqueueoutputcallback)

## Compressed fallback

If PCM is unavailable, use Audio File Stream Services or another proven incremental system parser and preserve packet descriptions, decoder state, and magic cookies when required. Do not concatenate independent MP3 files and assume they form one stream. Do not make a handwritten frame sanitizer the default repair; first prove malformed frames exist and that decoder-state continuity is preserved.

Current provider behavior should be checked against its official endpoint documentation, such as [MiniMax T2A WebSocket](https://platform.minimax.io/docs/api-reference/speech-t2a-websocket).

## Audio graph ownership

An inactive microphone handler does not mean its `AVAudioEngine` stopped owning the device. For half-duplex coaching, stop or suspend capture before TTS playback and restart it after playback completion. Do not keep multiple output engines alive for convenience.

Full-duplex barge-in is a separate product and architecture choice. It needs echo cancellation, route handling, interruption policy, and explicit mixing; do not accidentally create it by leaving capture and playback graphs running together.

## Required verification

1. Save one fixed provider artifact without secrets and validate format, byte alignment, duration, and decoder errors.
2. Compare provider and mixer artifacts numerically or by independent playback.
3. Test the installed Release app on the user's actual speaker or headset.
4. Run two consecutive TTS turns, replay, stop during speech, and resume ASR capture.
5. Confirm logs have one open/start/finish sequence per successful turn and no underrun or stale completion.
6. Obtain human confirmation for crackle, clipping, timing, and voice quality.

Remove temporary audio captures and diagnostic taps after diagnosis. Preserve them in a recoverable private location only when further comparison is required.
