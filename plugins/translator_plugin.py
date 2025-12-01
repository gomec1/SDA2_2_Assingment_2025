import requests
from core.plugin_base import BasePlugin


class DeepLTranslatingPlugin(BasePlugin):
    # Hardcoded API key for demonstration purposes only.
    API_KEY = "49056327-eb06-4243-9d5f-e7f187c709a2:fx"
    ENDPOINT = "https://api-free.deepl.com/v2/translate"

    # Supported target languages
    SUPPORTED_TARGET_LANGS = {
        "English": "EN",
        "German": "DE",
        "French": "FR",
        "Italian": "IT",
        "Spanish": "ES",
        "Dutch": "NL",
        "Polish": "PL",
        "Portuguese": "PT",
        "Russian": "RU",
    }

    def __init__(self) -> None:
        # Default target language
        self.target_lang: str = "EN"

        # Source language = None → DeepL auto-detects it
        self.source_lang: str | None = None

    @property
    def name(self) -> str:
        return "Translating Plugin with DeepL"

    @property
    def description(self) -> str:
        return (
            "Translates the input text using the DeepL API. "
            "The target language can be selected in the UI."
        )

    def process(self, text: str) -> str:
       # Prepare payload for DeepL API request
        payload = {
            "auth_key": self.API_KEY,
            "text": text,
            "target_lang": self.target_lang,
        }

        # Only include source_lang if explicitly set
        if self.source_lang:
            payload["source_lang"] = self.source_lang

        try:
            response = requests.post(self.ENDPOINT, data=payload)
            response.raise_for_status()

            data = response.json()
            translated_text = data["translations"][0]["text"]
            return translated_text

        except Exception as e:
            return f"[DeepL Translation Error: {e}]\n\nOriginal Text:\n{text}"
