# Camera Lab

RigSight AI 1.0 keeps camera support optional, local, and disabled by default.

## Behavior

- `GET /camera/status` always returns a safe status payload.
- The default status is `disabled`.
- `GET /camera/snapshot` returns `503` unless camera capture is enabled and a local device is available.
- Camera capture is never required for telemetry, alerts, review, reports, or the main demo.

## Configuration

Set these environment variables only for local experimentation:

```bash
CAMERA_ENABLED=true
CAMERA_DEVICE_INDEX=0
```

OpenCV is treated as an optional local dependency. If camera capture is enabled but OpenCV is missing, the API reports `unavailable`.

## Clean-Room Constraint

Only use personally controlled local devices. Do not capture private workplace footage, proprietary rigs, internal lab spaces, or identifiable people for portfolio screenshots.
