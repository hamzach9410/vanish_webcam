#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Auto-detect v4l2loopback device if loaded
DEVICE_OPT=""
if [ -e /dev/video10 ]; then
    DEVICE_OPT="--virtual-backend v4l2loopback --virtual-device /dev/video10"
fi

source .venv/bin/activate
python vanish_cam.py $DEVICE_OPT "$@"

