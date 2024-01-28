from mealcurator.settings import AI_COMPLETION_MODEL
from openai import OpenAI
from bs4 import BeautifulSoup

# Holds helper functions for various things that need solutions

# Check for blanks and if found default value
def check_blank(input, default):
    if input == '':
        return default
    else:
        return input

# AI Configurations
class aimealcurator:
    def __init__(self):
        self.model = AI_COMPLETION_MODEL
        self.client = OpenAI()

class aicreatemeal(aimealcurator):
    def __init__(self, ingredients, mode, time, other):
        super().__init__()
        self.message_start = self._message_prep(ingredients, mode, time, other)
        self.response = self._get_response()

    def _message_prep(self, ingredients, mode, time, other):
        """Function to prep message parts before passing to OpenAI."""
        cooking_mode = ''
        if len(mode) > 0:
            cooking_mode = f' made in {mode}'

        cooking_time = ''
        if len(time) > 0:
            cooking_time = f' that takes {time}'

        cooking_other = ''
        if len(other) > 0:
            cooking_other = f' and is {other}' 

        return (
            f'A recipe with {",".join(str(x) for x in ingredients[:10])}'
            f'{cooking_mode}'
            f'{cooking_time}'
            f'{cooking_other}'
        )

    def _get_response(self):
        """Send request to OpenAI API and get response"""
        response = self.client.chat.completions.create(
            model = AI_COMPLETION_MODEL,
            messages = [
                {
                    'role': 'system',
                    'content': 'Create a recipe in HTML from the provided ingredients and other information.'
                },
                {
                    'role': 'user',
                    'content': self.message_start
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response

    def clean_response(self):
        """Take HTML and pull out just the body portion"""
        soup = BeautifulSoup(
            self.response.choices[0].message.content,
            'html.parser'
        )
        return soup.body
