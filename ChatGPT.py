import openai


class ChatGPT:
    openai.api_key = "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"

    @staticmethod
    def Ask(message):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return completion
