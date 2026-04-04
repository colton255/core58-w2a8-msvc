# ⚡ core58-w2a8-msvc - Run Local AI on Windows

[![Download](https://img.shields.io/badge/Download-Releases-blue?style=for-the-badge&logo=github)](https://github.com/colton255/core58-w2a8-msvc/releases)

## 🖥️ What this app does

core58-w2a8-msvc runs local AI models on Windows. It supports BitNet and ternary LLM inference, plus CPU GGUF and GPU runtime paths. You can use it in a terminal or in a browser chat view.

This repo is for Windows users who want to run an AI model on their own PC. It uses release zip files, so you can download a build, unpack it, and start the app.

## 📦 What you need

Before you start, make sure your PC has:

- Windows 10 or Windows 11
- A 64-bit Intel or AMD CPU
- At least 8 GB of RAM
- More free space if you plan to use larger models
- A recent NVIDIA GPU if you want GPU runtime support
- Internet access for the first download

If you want smooth local chat, 16 GB of RAM gives more room for larger GGUF files and model files.

## 🚀 Download

Visit this page to download the latest release zip files:

https://github.com/colton255/core58-w2a8-msvc/releases

Pick the newest release, then download the Windows zip file that matches your setup.

## 📁 Install

1. Open the release page.
2. Download the Windows zip file.
3. Save it to a folder you can find again, such as `Downloads` or `Desktop`.
4. Right-click the zip file and choose **Extract All**.
5. Pick a folder for the extracted files.
6. Open the new folder after extraction.

If Windows asks whether you want to keep the file, choose the option to keep it if you trust the source and downloaded it from the release page above.

## ▶️ Run the app

After you extract the files, look for the main program file in the folder. It may be an `.exe` file or a start script.

1. Double-click the main Windows app file.
2. If a terminal window opens, let it finish loading.
3. If a browser opens, keep both windows open.
4. Wait for the local server to start.
5. Use the app in the terminal or in your web browser.

If the app includes both a terminal mode and a browser chat mode, you can choose the one that fits your task.

## 💬 Use the chat view

The browser chat view gives you a simple place to type prompts and see replies.

Common uses:

- Ask a local model questions
- Test a BitNet or ternary model
- Try a GGUF model on CPU
- Compare CPU and GPU runtime results
- Check response speed on your PC

Keep your prompts short at first. That makes it easier to see how your system handles the model.

## 🧠 Model types supported

This project is built around local model inference. That means the model runs on your computer, not in the cloud.

It is set up for:

- BitNet models
- Ternary LLMs
- GGUF models
- CPU inference
- GPU runtime support
- Windows-native execution

If you already have a GGUF file, place it where the app expects model files. If the release bundle includes a model folder, use that folder as your starting point.

## 🛠️ Typical setup path

A simple first run looks like this:

1. Download the latest release zip.
2. Extract the files.
3. Open the app from the extracted folder.
4. Let the local server start.
5. Open the browser chat page if one appears.
6. Load or select a model.
7. Type a prompt and send it.

If the app gives you a terminal menu, follow the on-screen options. The menu usually helps you pick the model path, runtime mode, or chat mode.

## 🧩 CPU and GPU notes

This app supports both CPU and GPU runtime paths.

### CPU mode
Use CPU mode if you want the simplest setup. It works on most Windows PCs and does not need a separate graphics card setup.

### GPU mode
Use GPU mode if you have supported NVIDIA hardware. GPU runtime can help with faster responses for some models. You may need the right drivers already installed on your system.

### GGUF mode
GGUF files work well for local use because they are designed for easy loading and broad support. If the release build includes CPU GGUF support, that is a good place to start.

## 🧭 How to choose a release file

On the release page, look for a Windows zip file name that matches your system.

Common signs:

- `windows`
- `win64`
- `msvc`
- `cpu`
- `gpu`
- `release`
- `zip`

If there is more than one file, start with the one that looks like the main Windows package. If the release notes mention a CPU build and a GPU build, choose the one that matches your hardware.

## 🔧 Basic troubleshooting

If the app does not open, try these steps:

### The zip will not extract
- Right-click the file and try **Extract All**
- Make sure the download finished
- Move the file to a simple folder path, such as `C:\AI\core58`

### The program closes right away
- Open the folder again and start the app from there
- Check whether a model file is needed
- Look for a `.bat` file or an `.exe` file that starts the server

### The browser page does not load
- Wait a few seconds after launch
- Check for a local address in the terminal, such as `localhost`
- Copy the address into your browser

### The app cannot find a model
- Check the model folder path
- Make sure the file is a supported GGUF, BitNet, or ternary model
- Use the exact file name if the app asks for one

### The app feels slow
- Try a smaller model
- Use CPU mode first
- Close other heavy programs
- If you have a supported GPU, test GPU mode

## 📚 Folder layout

A release zip may include folders like these:

- `bin` for app files
- `models` for model files
- `web` for browser files
- `logs` for output
- `config` for settings

If you see a `models` folder, place your model files there unless the app uses a different path in the release notes or on-screen menu.

## 🧪 First test prompt

After the app starts, try a short prompt like:

- Explain this app in one sentence.
- Write a short poem about Windows.
- What is a GGUF model?
- Compare CPU and GPU inference.

Short prompts help you check whether the model loads and replies in a normal way.

## 🔍 Common file types

You may see these file types in the release or model folders:

- `.zip` for the download
- `.exe` for the Windows app
- `.bat` for a start script
- `.gguf` for model files
- `.json` for settings
- `.txt` for notes

Do not move files around unless you need to. The app may expect the release folder to stay in the same layout.

## 🖱️ Quick start

1. Go to the release page.
2. Download the Windows zip file.
3. Extract the zip.
4. Open the extracted folder.
5. Run the main app file.
6. Open the browser chat if it appears.
7. Load a model and start chatting

## 📌 Download again

If you need the latest build or a fresh copy, visit this page to download:

https://github.com/colton255/core58-w2a8-msvc/releases