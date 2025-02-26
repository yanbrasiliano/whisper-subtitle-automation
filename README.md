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
sudo apt install ffmpeg -y   # Debian/Ubuntu
brew install ffmpeg          # macOS
choco install ffmpeg         # Windows (with Chocolatey)

# Install iconv (already included in most Unix-based OS)
sudo apt install iconv -y    # Debian/Ubuntu

# Install Whisper AI via pip
pip install openai-whisper
```

---

## 🚀 **Usage**
1️⃣ **Clone the repository**
```bash
git clone https://github.com/yanbrasiliano/whisper-subtitle-automation.git
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

## 🐍 **Python Alternative**

In addition to the shell script, we provide a **Python version** that offers better performance through **parallelism and asynchronous processing**.

### 🔹 **Advantages of the Python Script**
- **Parallelism and Asynchronous Execution:** Uses asynchronous processing to **speed up performance**, allowing multiple videos to be processed simultaneously.
- **Flexibility:** Easier to modify and extend for future improvements.

### 🔹 **Considerations**
- **Resource Consumption:** The Python script **requires more RAM and CPU power** due to parallel processing.
- **Additional Dependencies:** Requires Python libraries like `tqdm`, `aiofiles`, and `concurrent.futures`.

### 🔹 **Installing and Running the Python Script**
1️⃣ **Install the necessary dependencies:**
```bash
pip install openai-whisper aiofiles tqdm
```

2️⃣ **Place your `.mp4` files inside the script folder.**

3️⃣ **Run the Python script:**
```bash
python batch_whisper_subtitles.py
```

4️⃣ **Wait for processing:**
- The script will **generate and embed subtitles** automatically.
- The processed videos will be saved with the suffix `_subtitled_en_us.mp4`.

5️⃣ **Temporary Files Cleanup:**
- The script **automatically deletes** the generated temporary files (`.srt`, `.tsv`, `.txt`, `.vtt`, `.json`).

---

## ❓ **FAQ**
#### **1. Can I process multiple videos at once?**
Yes! Both scripts will automatically process all `.mp4` files in the directory.

#### **2. What happens if a video already has subtitles?**
The scripts will **embed new AI-generated subtitles** into the video.

#### **3. How do I change the output format?**
By default, the output file is named:  
`original-file_subtitled_en_us.mp4`.  
You can modify the naming format inside the script.

#### **4. The script removed some files. Is that normal?**
Yes! Both scripts **automatically delete temporary Whisper files** (`.srt`, `.tsv`, `.txt`, `.vtt`, `.json`).  
They **never delete your original videos or the script itself**.

---

## 🛠 **Contributing**
Feel free to open an issue or submit a pull request if you have improvements or suggestions!

---

## 📜 **License**
GNU License © 2025 Yan Brasiliano Silva Penalva
