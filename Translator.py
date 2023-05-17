from translate import Translator


class Translator_bot:
    @staticmethod
    def translate(message):
        text = message.lower()
        print(text)
        text = text.split(' ')
        text.pop(0)
        translator = Translator(from_lang=text[0], to_lang=text[len(text)-1])
        print(text)
        text.pop(0)
        text.pop(len(text)-1)
        return translator.translate(" ".join(text))
