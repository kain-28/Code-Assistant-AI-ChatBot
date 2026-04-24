import os

import google.generativeai as genai

from env_config import get_clean_env, get_gemini_api_key, load_backend_env

load_backend_env()


class LLMService:
    def __init__(self):
        self.system_instruction = """
        You are KAIN, a professional and helpful coding assistant.
        Your tone is professional, clear, and focused on helping the user solve technical problems.

        Rules:
        1. Only provide answers based on provided knowledge or general coding best practices.
        2. If you are unsure, admit it. Do not hallucinate.
        3. Use Markdown for formatting code blocks.
        4. Be concise but thorough in explanations.
        """
        self.api_key = None
        self.mock_mode = False
        self.model = None
        self.model_name = get_clean_env("GEMINI_MODEL", "gemini-2.5-flash")

        self._configure_model()

    def _configure_model(self):
        load_backend_env()
        self.api_key = get_gemini_api_key()

        if not self.api_key:
            print("Warning: No Gemini API Key found. Entering Mock Mode for testing.")
            self.mock_mode = True
            return

        # The Gemini SDK can also look for GOOGLE_API_KEY internally.
        os.environ["GOOGLE_API_KEY"] = self.api_key

        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=self.system_instruction,
            )
        except Exception as exc:
            print(f"Warning: Failed to initialize Gemini client: {exc}. Entering Mock Mode.")
            self.api_key = None
            self.model = None
            self.mock_mode = True

    def _is_configuration_error(self, error):
        error_text = str(error).lower()
        return any(
            fragment in error_text
            for fragment in (
                "api_key",
                "adc found",
                "application default credentials",
                "permission denied",
                "invalid api key",
                "403",
                "401",
            )
        )

    async def get_response(self, messages, context=""):
        prompt = messages[-1].content

        if self.mock_mode or self.model is None:
            return self._get_mock_response(prompt, context)

        try:
            history = []
            for msg in messages[:-1]:
                role = "user" if msg.role == "user" else "model"
                history.append({"role": role, "parts": [msg.content]})

            chat = self.model.start_chat(history=history)

            if context:
                prompt = f"Context from Knowledge Base:\n{context}\n\nUser Question: {prompt}"

            response = chat.send_message(prompt)

            if not response or not response.text:
                return "I'm sorry, I couldn't generate a response. Please try again."

            return response.text
        except Exception as exc:
            print(f"LLM Service Error: {exc}")
            if self._is_configuration_error(exc):
                self.api_key = None
                self.model = None
                self.mock_mode = True
                fallback = self._get_mock_response(messages[-1].content, context)
                return (
                    f"{fallback}\n\n"
                    "Live Gemini responses are unavailable until a valid `GEMINI_API_KEY` "
                    "is added to `backend/.env` and the backend is restarted."
                )
            return f"Error: {str(exc)}"

    def _get_mock_response(self, query, context=""):
        if "KAIN" in query.upper() and context:
            return (
                f"Mock Response: {context}\n\n"
                "(Note: I am currently running in **Mock Mode** because no Gemini API Key "
                "was found in your .env file.)"
            )

        return (
            "Hello! I am KAIN. I am currently running in **Mock Mode** because I don't "
            "have a valid API key. To get a real response, please add your `GEMINI_API_KEY` "
            "to the `backend/.env` file and restart the server."
        )

llm_service = LLMService()
