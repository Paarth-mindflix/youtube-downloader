# 🎯 Stage-0: Dynamic Keyword Generation & YouTube URL Extraction

This stage generates **dynamic keywords** targeting Indian YouTube videos (interviews, podcasts, news, etc.) and extracts **video URLs** from those keywords, playlists, or channels.  
It forms the **first stage** of the *Indian Talking Faces Dataset Pipeline*, similar to VoxCeleb and LRS-2/3 dataset collection workflows.

---

## 🧩 Overview

| Functionality | Description |
|:---------------|:------------|
| Keyword generation | Dynamically expand or generate topic-specific keywords for scraping |
| Channel/playlist link extraction | Extract all video links from given channel or playlist URLs |
| Trending fetcher | Retrieve trending or region-specific videos (India-focused) |
| YouTube API support | Optionally integrates with YouTube Data API for metadata filtering |

---

## ⚙️ Environment Setup

### 1️⃣ Create a new Conda environment
```bash
conda create -n stage0_env python=3.10
conda activate stage0_env
```
### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Install Google Chrome and ChromeDriver
This project uses Selenium for scraping YouTube when API quota is limited.
You must install Chrome and a matching ChromeDriver version.

Step 1. Check your Chrome version
Open Chrome and go to:
chrome://settings/help

Step 2. Download the matching ChromeDriver
Go to the [ChromeDriver Downloads](https://developer.chrome.com/docs/chromedriver/downloads) page and download the version matching your Chrome.

Step 3. Extract and place the driver
1. Extract the ZIP file → you’ll get chromedriver.exe.
2. Move it to a location accessible by the system. Recommended paths:
```bash
C:\Windows\System32
```
or
```bash
C:\Program Files\Google\ChromeDriver
```

3. Copy this full path — you’ll need to pass it to <mark>main.py<mark/>.

Step 4. Verify installation

Open PowerShell or Command Prompt:
```bash
chromedriver --version
```
If installed correctly, you’ll see something like:
```bash
ChromeDriver 127.0.6533.89
```

### 4️⃣ Run main.py with chromedriver path as argument
```bash
python main.py
    --chromedriver_path "C:\Windows\System32\chromedriver.exe"
```
