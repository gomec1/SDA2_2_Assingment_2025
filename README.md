# Microkernel Architecture Proof of Concept for Text Processing

# 📌 Project Team (Group B)

This project was created as part of the module Software Architecture at the Berne University of Applied Sciences by:

* Barcikowska Anna
* Stähli Thomas
* Stettler Gil Colin
* Kallioinen Jimi Eemil
* Carlos Gomez

---

# Introduction

This project is a proof-of-concept implementation of a text processing tool based on the Microkernel Architecture. The goal of the assignment is to demonstrate how modularity, extensibility, and separation of concerns can be achieved by organizing the system around a lightweight core and independently developed plugins.

The core module is responsible for performing essential operations such as loading and saving text files, discovering available plugins, and orchestrating the processing workflow. All text transformations are implemented as plugins, which can be added, removed, or extended without modifying the core system. This design highlights the benefits of the microkernel approach, including flexibility, maintainability, and support for agile development.

To showcase extensibility, several plugins have been implemented—each providing a distinct text processing capability, such as word frequency analysis, search-and-replace functionality, and translation using the DeepL API. The system also includes a Streamlit-based user interface that allows users to upload text files, select plugins, configure plugin-specific settings, and download the processed output.

---

# ✅ Prerequisites (one-time setup)

## 1. 🔧 Install Python (version 3.12 or higher)

* Official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* During setup, **enable "Add Python to PATH"**
* Then verify installation in your terminal:

```bash
python --version
```

---

# 🔧 Setup – Step by Step

# !For the following steps use CMD (Windows) / Terminal (Mac)!

## 1. 📁 Clone the Project

```bash
git clone https://github.com/gomec1/SDA2_2_Assingment_2025.git
cd SDA2_2_Assingment_2025/
```

## 2. 🪪 Set Up Virtual Environment 

* **Windows:**

```bash
py -m venv venv
```

* **macOS:**

```bash
python -m venv venv
```

### Then activate:

* **Windows:**

```bash
venv\Scripts\activate.bat
```

* **macOS:**

```bash
source venv/bin/activate
```

---

## 3. 📦 Install Required Dependencies

```bash
pip install -r requirements.txt
```

### `requirements.txt` content:

```text
streamlit
Pillow
requests
```
## 4. ✅ Start Microkernel application

```bash
streamlit run app.py
```

You can now view our Streamlit app in your browser.
    Local URL: http://localhost:8501

---

# 💾 Plugin descriptions
## Find & Replace
Replace all occurrences of a string (or regex pattern) with another string.
Simple select the plugin and write the string you want to find and the string you want it to be replaced with and process. If you want to use a regex pattern, check the "Use regex" checkbox before processing.

## Sentiment Analysis
Analyzes the overall sentiment of the text (positive, negative, neutral)
and prepends a short summary at the top of the text.
This is done by counting the amount of positiv or negativ words in the text, based on provided positiv and negativ word lists. Intensifier like "very" double the count of the word and negations change the sentiment of the following word.

## Top Words (Frequency)
The Top Words (Frequency) plugin analyzes the input text and identifies the most frequently used words.
This plugin:
- Ignores common stopwords (e.g., the, and, or, der, die, das).
- Counts the frequency of remaining words.
- Generates a short report listing the top-occurring words with their frequencies.
- Prepends the report to the processed output while keeping the original text intact.
No additional configuration is required—simply select the plugin and process the text.

## Letter + Word Counter
Counts total words and alphabetic letters (ignores spaces and punctuations), then prepends a short report ahead of your original text. No configuration needed—just select the plugin and process the file to see the counts.

## Translating Plugin with DeepL
The Translating Plugin with DeepL uses the official DeepL API to translate the entire input text into a selected target language.
In the user interface, you can choose the output language (e.g., English, German, French, Italian, etc.). DeepL automatically detects the input language unless a source language is manually specified in the plugin code.
Usage
1. Select Translating Plugin with DeepL in the plugin list.
2. Open the plugin settings panel.
3. Choose the desired target language from the dropdown.
4. Run the processing step.
The resulting text will be fully translated into the selected language.

**Important Note About the DeepL API Key**
The included DeepL API key currently allows up to 500,000 characters of translation.
If a translation request fails and you see an error message, this likely means that the character limit has been exceeded.
You can create your own free DeepL API key here:
https://www.deepl.com/de/products/api
After generating your key, simply replace the existing one in the plugin file:
```bash
API_KEY = "YOUR_NEW_KEY_HERE"
```

## Grammar Checker
The Grammar Checker uses the Gemini API (gemini-2.5-flash) to perform expert-level proofreading. It corrects grammar, typos, and punctuation while strictly preserving the original meaning and structure of the text.

**API Key Required:** 
Ensure your GEMINI_API_KEY is set in your project's .env file like this:
```bash
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```
You can obtain a key from Google AI Studio.

The plugin returns only the corrected text with no extra explanation or formatting. If the API key is missing or the client fails to initialize, it will return an error message.
