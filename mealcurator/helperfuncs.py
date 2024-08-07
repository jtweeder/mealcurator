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
class AIMealCurator:
    def __init__(self):
        self.model = AI_COMPLETION_MODEL
        self.client = OpenAI()


class AICreateMeal(AIMealCurator):
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
            f'That is cooked in or with {cooking_mode}'
            f'That takes about {cooking_time}'
            f'Other Considerations {cooking_other}'
        )

    def _get_response(self):
        """Send request to OpenAI API and get response"""
        response = self.client.chat.completions.create(
            model=AI_COMPLETION_MODEL,
            messages=[
                {
                    'role': 'system',
                    
                    
                    'content': 
                        '''You are a chef you will be provided a list of ingredients, a cooking method, a cooking time and other considerations
                        Your goal is to create a recipe in a valid HTML format that contains no images, and has a body and head section with a title from the provided ingredients and other information,
                        You do not have to use all the ingredients, and you may add in other ingredients as you see fit since you are a chef,
                        but the recipe should be something considered a complete meal and delicious.  
                        When you are adding in other ingredients, stay with ingredients that would be found in most 
                        american grocery stores.  The recipe should be something that can made in a home kitchen.
                        Before returning check to ensure the recipe is something that you would be proud to serve to a guest.
                        
                        If you are only given some information like how long the meal should take to cook, and other considerations, with some or no ingredients,
                        try to understand the theme of meal that they user is trying to find and generate a recipe for that theme.  Use the other considerations to help
                        guide you on what this theme may be.

                        Pay close attention to any dietary restrictions such as food allergies, vegan or vegetarian requests that will appear in the Other Considerations section.

                        If you are uncertain if you would want to serve this, retry making the recipe at most 5 times and 
                        exclude ingredients that may seem odd in the combination to get to a result. If you are still uncertain, return what you 
                        think is a safe meal based on the information you have been provided.
                        
                        Ensure that the response is a complete meal with possible suggestions for sides to ensure the meal has all food groups and contains the anticipated number of servings in the summary.
                        The title in the HTML must be less than 30 characters long

                        Your return should be a valid HTML document without images and MUST contain a head section with a title, and a body section broken into sections of <h3> size of Ingredients, Directions, Summary with anticipated number of servings, and suggested sides if applicable
                        that contains no images
                        '''
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

        # Get contents of body tag and create string
        body_content = soup.body.contents
        body_content_str = ''.join(str(x) for x in body_content)
        # Append a disclaimer to the end of the recipe that says it was AI generated
        body_content_str += '<p>Recipe generated by AI - May be incorrect - Always cook ingredients to a safe temperature</p>'
        # Find title tag and extract text
        title_tag = soup.find('title')

        if title_tag:
            title = title_tag.text
        else:
            title = 'Untitled AI Recipe'

        return title, body_content_str
