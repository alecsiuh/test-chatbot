from translate import Translator
from langdetect import detect

translator = Translator(to_lang='nl')



class MessageHandler:

    @staticmethod
    def translate_message(query):
        detected_language = detect(query)
        if detected_language == 'en':
            translated_message = translator.translate(query)
            return translated_message
        else:
            return query

    @staticmethod
    def format_message(role, content):
        return {"role": role, "content": content}

    @staticmethod
    def extract_function_name(response):
        # Extract function name logic here
        pass
