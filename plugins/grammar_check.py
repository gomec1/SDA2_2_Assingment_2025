import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError
from core.plugin_base import BasePlugin

load_dotenv()

class LLMGrammarCheck(BasePlugin):
    """
    Uses the Gemini API for grammar correction.
    """

    @property
    def name(self) -> str:
        return "Grammar Checker"

    def __init__(self):
        try:
            self.client = genai.Client()
        except Exception as e:
            self.client = None
            
        self.model = 'gemini-2.5-flash'
        self.system_instruction = (
            "You are an expert grammar and style checker. Your task is to ONLY correct "
            "grammatical errors, typos, and punctuation issues in the user-provided text. "
            "CRITICAL: DO NOT alter the core content, structure, or tone of the text. "
            "You must return ONLY the corrected text, with no introductory phrases, "
            "explanations, or markdown formatting (like ```)."
        )

    def process(self, text: str) -> str:
        if not self.client:
            return "--- ERROR ---\nGemini client not initialized. Check your GEMINI_API_KEY environment variable."

        prompt = f"Please proofread and correct the following text: {text}"
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt],
                config=genai.types.GenerateContentConfig(
                    system_instruction=self.system_instruction
                )
            )
            
            corrected_text = response.text.strip()
            
            #report = f"--- LLM Grammar Auto-Correction Status ---\n"
            #report += f"Text corrected using **{self.model}** (Internet required).\n\n"
            
            #return report + corrected_text
            return corrected_text

        except APIError as e:
            return f"--- API Error ---\nCould not process text. Check API Key/Network. Error: {e}"
        except Exception as e:
            return f"--- General Error ---\nAn unexpected error occurred: {e}"