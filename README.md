# 🎬 Whisper Subtitle Automation

A simple shell script to **automate the generation of subtitles for videos** using [Whisper AI](https://github.com/openai/whisper) and **embed them into `.mp4` files using FFmpeg**.

🚀 **Features:**
- Automatically **generates English subtitles** for all `.mp4` files in the directory.
- **Embeds the subtitles** into the videos using **FFmpeg**.
- Converts filenames to **snake-case with hyphens**.
- **Removes temporary files** (`.srt`, `.tsv`, `.txt`, `.vtt`, `.json`) after processing.
- **Checks for required dependencies** (`python3`, `ffmpeg`, `iconv`, `whisper`) before running.

---

## 📌 **Requirements**
Before running the script, make sure you have the following dependencies installed:

| Dependency  | Description |
|-------------|------------|
| **Python 3**  | Required for running Whisper AI |
| **Whisper AI** | AI model for generating subtitles |
| **FFmpeg** | Used to embed subtitles into the `.mp4` file |
| **iconv** | Ensures correct encoding for subtitles |

### 🔹 **Installing Dependencies**
If you don't have them installed, run the following commands:

```bash
# Install Python3 (if not installed)
sudo apt install python3 -y  # Debian/Ubuntu
brew install python3         # macOS
choco install python         # Windows (with Chocolatey)

# Install FFmpeg
sudo apt install ffmpeg -y  # Debian/Ubuntu
brew install ffmpeg         # macOS
choco install ffmpeg        # Windows (with Chocolatey)

# Install iconv (already included in most Unix-based OS)
sudo apt install iconv -y  # Debian/Ubuntu

# Install Whisper AI via pip
pip install openai-whisper
```

---

## 🚀 **Usage**
1️⃣ **Clone the repository**
```bash
git clone https://github.com/your-username/whisper-subtitle-automation.git
cd whisper-subtitle-automation
```

2️⃣ **Make the script executable**
```bash
chmod +x batch_whisper_subtitles.sh
```

3️⃣ **Place your `.mp4` files inside the folder**

4️⃣ **Run the script**
```bash
./batch_whisper_subtitles.sh
```

5️⃣ **Wait for processing**
- The script will **automatically generate English subtitles** and embed them in the video.
- The **output video will have subtitles embedded** and will be saved in the format:
  ```
  original_file.mp4  →  original-file_subtitled_en_us.mp4
  ```

6️⃣ **Temporary files are automatically deleted** after processing.
- The script removes all Whisper-generated files (`.srt`, `.tsv`, `.txt`, `.vtt`, `.json`).
- It keeps only the final `.mp4` files.

---

## 📌 **Example**
### **Before running the script**
```
/videos/
 ├── my_video.mp4
 ├── another_video.mp4
 ├── batch_whisper_subtitles.sh
```

### **After running the script**
```
/videos/
 ├── my-video_subtitled_en_us.mp4
 ├── another-video_subtitled_en_us.mp4
 ├── batch_whisper_subtitles.sh  # The script remains
```
🚀 **The script automatically renames files and deletes temporary subtitle files!**

---

## 🔧 **Customization**
- To change the subtitle **language**, edit this line inside the script:
  ```bash
  WHISPER_LANG="English"
  ```
  For other languages, check the full list here: [Whisper Supported Languages](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py#L10).

- To use a **different Whisper model**, change this line:
  ```bash
  MODEL="base"  # Options: tiny, base, small, medium, large
  ```

---

## ❓ **FAQ**
#### **1. Can I process multiple videos at once?**
Yes! The script will automatically process all `.mp4` files in the directory.

#### **2. What if a video already has subtitles?**
The script will **embed new AI-generated subtitles** into the video.

#### **3. How do I change the output format?**
By default, the output file is named:  
`original-file_subtitled_en_us.mp4`.  
You can modify the naming format inside the script.

#### **4. The script removed some files. Is that normal?**
Yes! The script automatically **deletes temporary Whisper files** (`.srt`, `.tsv`, `.txt`, `.vtt`, `.json`).  
It **never deletes your original videos or the script itself**.

---

## 🛠 **Contributing**
Feel free to open an issue or submit a pull request if you have improvements or suggestions!

---

## 📜 **License**
GNU License © 2025 Your Name
