# Run notes
- Base first attempt stalled ~16 minutes and was terminated. User requested continuation.
- Base retry succeeded with actual RGBA transparency; preserve alpha.
- Idle, directional runs, waving, jumping, failed, running and review structural checks pass.
- Running-left derived by approved framewise mirror, preserving frame timing.
- Jumping common per-frame fit caused size pulse and removed vertical travel; skill stable-slots extraction corrected it. Independent standard QA confirms clear arc and no clipping.
- Pending waiting generation is a service-latency blocker; other outputs retained.
- Built-in imagegen used throughout; no CLI fallback.
