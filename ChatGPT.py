import openai
import config

class ChatGPT:
    openai.api_key = config.CHAT_TOKEN

    @staticmethod
    def Ask(message: str):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return completion
