# BillinAutoPoster
Advanced Billin Instagram Reels Auto Poster - IOS/ANDROID

---

## 1. Prerequisites

- **Windows 10+**  
- **Python 3.8+**  
- **BlueStacks 5** (Performance: OnePlus 10 Pro, 2 GB RAM, 2 CPU cores, 1280×720)  
- **Android SDK Platform-Tools** (so `adb` works)

---

## 2. Setup BlueStacks

1. **Settings → Performance**  
   - Profile: **OnePlus 10 Pro**  
   - RAM: **2048 MB**  
   - CPU: **2 cores**  
   - Resolution: **800x2160**  

2. **Settings → Preferences**  
   - Enable **ADB** (toggle ON)  
   - Media Folder → choose or create a Windows folder, e.g. `C:\BlueStacksShared`  
   - Restart BlueStacks when asked  

---

## 3. Install & Prep

```bash
# clone & enter project
git clone https://github.com/you/billin-pipeline.git
cd billin-pipeline

# create venv & install
python -m venv .venv
.venv\Scripts\activate
pip install yt-dlp pyautogui keyboard


