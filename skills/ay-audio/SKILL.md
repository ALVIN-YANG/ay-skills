---
name: ay-audio
description: Build, diagnose, and repair streaming voice audio on Apple platforms with evidence from provider bytes through hardware output. Use when Swift, macOS, or iOS TTS/voice playback is silent, crackles, pops, clips, re-buffers, fails on later turns, or mixes badly with ASR, VAD, AVAudioEngine, AudioQueue, PCM, MP3, or WebSocket streams. Do not use for generic UI sound design or offline media editing.
---

# AY Audio

Deliver continuous voice playback by proving each audio boundary instead of patching symptoms.

## Approval contract

<!-- ay-contract:start -->
- Read the full request and investigate discoverable facts before asking the user.
- Treat review, diagnosis, explanation, and planning as read-only unless the user also requests change.
- Treat a precise instruction as approval when target, observable result, and acceptance boundary are clear.
- A broad outcome authorizes investigation, not file or artifact changes based on choices the agent must invent.
- For a materially underspecified change, present one recommended proposal and wait for approval.
- After approval, execute autonomously inside the approved boundary; do not ask about ordinary implementation details.
- Reopen approval only when new evidence changes behavior, architecture, data contracts, dependencies, scope, risk, cost, rollback, or external actions.
- Perform external actions only when the request or approved proposal includes them. Confirm the exact target before an irreversible action.
- Preserve unrelated and user-authored work. Verify the real requested outcome before claiming completion.
<!-- ay-contract:end -->

## Establish the audio contract

Inspect provider documentation and a live response. Record transport, encoding, sample rate, channels, bit depth, endianness, framing, and whether chunks are raw audio or complete files. Decode wrappers such as hex exactly once. Never infer format from a filename or old implementation.

Map `provider → transport → parser/decoder → mixer → device`. Reproduce with a fixed sentence and the user's actual output route.

## Isolate the failing boundary

Capture provider bytes and, when applicable, digital mixer output from the same turn. Decode or play each through an independent path.

- Bad provider artifact points to request, contract, voice, or service.
- Clean provider bytes but bad mixer output points to parsing, conversion, scheduling, or buffering.
- Clean mixer output but bad audible output points to routing, competing engines, lifecycle, or hardware.

Run the smallest check that separates competing hypotheses. Do not hand-write MP3 frame repair or repeatedly tune buffers before locating the bad boundary.

## Implement the narrow path

Prefer provider-native linear PCM for simple streaming speech. Use an incremental system parser only when compressed transport is required.

Keep one explicit ownership state for listening, speaking, interruption, and cancellation. Design full-duplex deliberately. Tag turns so stopped streams cannot finish into later turns, and dispose queues only after callbacks settle.

Read [Apple streaming voice](references/apple-streaming-voice.md) before changing an Apple pipeline; it contains PCM, queue lifecycle, compressed fallback, graph ownership, and device-verification details.

## Prove the audible result

Verify request payload and playback format, then run the real app through consecutive turns, interruption, replay, and capture resume. Check byte counts, start, finish, cancellation, underrun, and errors.

Builds and digital tests do not prove clean sound. Keep implementation, automated checks, installed runtime, and human listening as separate evidence. Ask the user for the final perceptual verdict when the symptom is audible.
