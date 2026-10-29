# VanishCam 🥷✨

> The coolest way to conclude meetings and say goodbye. Real-time AI webcam disappearance effects for Google Meet, Zoom, Microsoft Teams, and OBS. Powered by MediaPipe, OpenCV, and Python.

**100% on-device & private:** Video processing runs locally on your machine at 30+ FPS. No video is ever recorded or transmitted to external servers.

---

### 👋 The Coolest Way to Say Goodbye & End Video Calls
Instead of the awkward "bye everyone..." wave while frantically searching for the red "Leave" button:
- Clasp your hands into a ninja prayer seal $\rightarrow$ explode into smoke and leave a wooden log in your chair.
- Raise a peace sign $\rightarrow$ dissolve out of existence.
- Show an open palm $\rightarrow$ shatter into wind-blown pixels.
- Give a thumbs up $\rightarrow$ glitch out like a sci-fi hologram.

Give your team the most memorable meeting sign-off in remote work history!

---

## ✨ Features

- **4 Disappearance Effects:**
  1. **Naruto Substitution (Kawarimi no Jutsu):** Clasp your hands in a ninja prayer seal — vanish instantly in a cloud of smoke with authentic sound as a wooden log drops in your place.
  2. **Normal Dissolve:** Raise a peace sign (V-sign) to dissolve your silhouette into glowing cyan particle mist.
  3. **Wind Particles:** Show an open palm to shatter your body into colored particles that get blown away by the wind.
  4. **Cyber Glitch:** Give a thumbs up to trigger chromatic aberration (RGB split), digital scanline tearing, and flicker out like a sci-fi hologram.
- **All-in-One Gesture Mode:** All 4 hand gestures are recognized in real time during the same session without restarting.
- **Instant Reappearance:** Press `R` to bring yourself back on camera instantly.
- **Virtual Camera Support:** Streams directly to Google Meet, Zoom, Teams, Discord, or OBS via `v4l2loopback` (Linux) or `OBS Virtual Camera`.
- **Keyboard Shortcuts:** Trigger any effect manually with number keys if you don't want to use hand gestures.

---

## 🎮 Gestures & Key Controls

| Effect | Hand Gesture | Hotkey | Description |
|---|---|:---:|---|
| **All-in-One** | *Any of the below* | `V` | All gestures enabled simultaneously |
| **Normal Dissolve** | **V / Peace Sign** ✌️ | `1` | Smooth energy dissolve into background |
| **Naruto Vanish** | **Prayer Hands** 🙏 | `2` | Smoke explosion, audio sound, falling wooden log |
| **Wind Particles** | **Open Palm** ✋ | `3` | Silhouette breaks into wind-blown floating particles |
| **Cyber Glitch** | **Thumbs Up** 👍 | `4` | RGB split, scanlines, holographic flicker out |

### General Controls
- **`R`**: Reappear immediately.
- **`SPACE`**: Recalibrate background (step out of camera view for 4 seconds).
- **`F`**: Toggle fullscreen preview.
- **`Q`** or **`ESC`**: Quit and release all camera devices.

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/hamzach9410/vanish_webcam.git
cd vanish_webcam
```

### 2. Setup environment

#### Linux (Ubuntu / Debian / Fedora)
```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup virtual camera loopback (for Google Meet / Zoom)
sudo apt install -y v4l2loopback-dkms
sudo modprobe v4l2loopback devices=1 video_nr=10 card_label="VanishCam" exclusive_caps=1
```

#### Windows
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🎥 Running VanishCam

### On Linux:
```bash
./run_linux.sh --mode all
```
*Or run directly with python:*
```bash
python vanish_cam.py --mode all --virtual-backend v4l2loopback --virtual-device /dev/video10
```

### On Windows:
```powershell
python vanish_cam.py --mode all
```

---

## 💼 Using in Google Meet, Zoom, or Teams

### Method A: Direct Virtual Camera (Linux)
1. Run `sudo modprobe v4l2loopback devices=1 video_nr=10 card_label="VanishCam" exclusive_caps=1`
2. Start VanishCam: `./run_linux.sh --mode all`
3. Step out of frame for 4 seconds during countdown, then step back in.
4. Open **Google Meet** $\rightarrow$ **Settings** $\rightarrow$ **Video**.
5. Under **Camera**, select **VanishCam** (or `/dev/video10`).

### Method B: Via OBS Studio (All Platforms)
1. Run VanishCam in preview mode:
   ```bash
   python vanish_cam.py --no-virtual-camera --mode all
   ```
2. Open **OBS Studio**.
3. Under **Sources**, add **Window Capture** $\rightarrow$ select **Webcam - Anteprima**.
4. Click **Start Virtual Camera** in OBS (bottom right).
5. In Google Meet / Zoom / Teams, select **OBS Virtual Camera**.

---

## 📁 Project Structure

```
vanish_webcam/
├── assets/
│   ├── substitution_log.png    # High-resolution substitution log illustration
│   ├── vanish.MP3              # Authentic substitution sound effect
│   └── vanish_icon.ico         # App icon
├── extra_effects.py            # Wind particle system, cyber glitch, & custom gesture math
├── naruto_effect.py            # Real-time procedural smoke & physics-based log drop
├── vanish_cam.py               # Main application, MediaPipe pipelines, & camera loop
├── vanish_sound.py             # Asynchronous low-latency audio playback
├── run_linux.sh                # Automated Linux launcher with device auto-detection
├── requirements.txt            # Python dependencies
└── LICENSE                     # MIT License
```

---

## 🛠️ Tech Stack

- **[MediaPipe](https://github.com/google-ai-edge/mediapipe):** High-performance selfie segmentation and 21-point hand landmark tracking.
- **[OpenCV](https://opencv.org/):** Frame acquisition, color space transformations, and graphical compositing.
- **[NumPy](https://numpy.org/):** Vectorized image processing, particle simulation, and geometric calculations.
- **[pyvirtualcam](https://github.com/letmaik/pyvirtualcam):** Cross-platform virtual video output for conferencing apps.
- **[Pygame](https://www.pygame.org/):** Zero-latency audio playback.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — see the LICENSE file for details.

Developed with ❤️ by [hamzach9410](https://github.com/hamzach9410).
