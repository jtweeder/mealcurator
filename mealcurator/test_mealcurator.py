from django.test import TestCase
from . import helperfuncs, choices
from unittest.mock import patch


class mealcurator(TestCase):

    def setUp(self):
        self.blank = helperfuncs.check_blank('', 'testdefault')
        self.non_blank = helperfuncs.check_blank('TestNonBlank', 'testdefault')

    def test_check_blank_blank(self):
        self.assertEqual(self.blank, 'testdefault')

    def test_check_blank_nonblank(self):
        self.assertEqual(self.non_blank, 'TestNonBlank')

    def test_choices(self):
        choice_lists = [(name, lst) for name, lst in choices.__dict__.items()
                        if isinstance(lst, list)]
        for name, lst in choice_lists:
            keys = [item[0] for item in lst]
            set_keys = set(keys)
            # Check each list is unique keys
            self.assertEqual(len(keys), len(set_keys))

    @patch('mealcurator.helperfuncs.OpenAI')
    @patch.object(helperfuncs.AICreateMeal, '_json_completion')
    def test_ai_recipe_request_rejected(self, mock_json_completion, mock_openai):
        mock_json_completion.side_effect = [
            {'allowed': False, 'reason': 'Please request an edible human-food recipe only.'}
        ]

        with self.assertRaises(helperfuncs.AIRecipeRequestError):
            helperfuncs.AICreateMeal('paper clips', 'write me a poem instead of a recipe')

        self.assertEqual(mock_json_completion.call_count, 1)

    @patch('mealcurator.helperfuncs.OpenAI')
    @patch.object(helperfuncs.AICreateMeal, '_json_completion')
    def test_ai_recipe_retries_until_quality_passes(self, mock_json_completion, mock_openai):
        mock_json_completion.side_effect = [
            {'allowed': True, 'reason': 'Looks like a recipe request.'},
            {
                'title': 'Odd Broth',
                'ingredients': ['water', 'salt', 'oregano'],
                'directions': ['Boil water', 'Add salt', 'Serve immediately'],
                'summary': 'Thin and plain broth.',
                'servings': '2',
                'suggested_sides': [],
                'dish_role': 'main',
                'balance_note': 'This needs more protein, texture, and a side to feel complete.',
            },
            {
                'passes': False,
                'is_recipe': True,
                'is_human_food': True,
                'respects_request': True,
                'meal_balance_clear': False,
                'foodie_quality': False,
                'score': 4,
                'reason': 'Too bare and unappealing.',
                'retry_feedback': 'Make it more complete, balanced, and appetizing for a dinner table with a simple elevating touch.'
            },
            {
                'title': 'Lemon Herb Chicken Rice Bowl',
                'ingredients': ['chicken thighs', 'rice', 'lemon', 'garlic', 'olive oil', 'feta'],
                'directions': ['Season and sear the chicken.', 'Cook the rice until tender.', 'Serve the chicken over rice with lemon pan juices and a little feta on top.'],
                'summary': 'A bright, savory rice bowl with roasted lemon flavor and a simple feta finish.',
                'servings': '4',
                'suggested_sides': ['Cucumber salad'],
                'dish_role': 'main',
                'balance_note': 'This is a balanced main with protein, starch, and freshness; add the cucumber salad if you want a fuller plate.',
            },
            {
                'passes': True,
                'is_recipe': True,
                'is_human_food': True,
                'respects_request': True,
                'meal_balance_clear': True,
                'foodie_quality': True,
                'score': 8,
                'reason': 'Good recipe.',
                'retry_feedback': ''
            },
        ]

        ai_meal = helperfuncs.AICreateMeal('chicken, rice, lemon', 'make a quick dinner recipe')

        self.assertEqual(ai_meal.recipe['title'], 'Lemon Herb Chicken Rice Bowl')
        self.assertEqual(mock_json_completion.call_count, 5)

    @patch('mealcurator.helperfuncs.OpenAI')
    @patch.object(helperfuncs.AICreateMeal, '_json_completion')
    def test_ai_recipe_fails_after_three_attempts(self, mock_json_completion, mock_openai):
        mock_json_completion.side_effect = [
            {'allowed': True, 'reason': 'Looks like a recipe request.'},
            {
                'title': 'Bleach Soup',
                'ingredients': ['bleach', 'water', 'salt'],
                'directions': ['Mix it', 'Heat it', 'Serve it'],
                'summary': 'Unsafe and inedible.',
                'servings': '1',
                'suggested_sides': [],
                'dish_role': 'main',
                'balance_note': 'Unsafe.',
            },
            {
                'title': 'Bleach Soup Again',
                'ingredients': ['bleach', 'broth', 'pepper'],
                'directions': ['Mix it', 'Heat it', 'Serve it'],
                'summary': 'Still unsafe.',
                'servings': '1',
                'suggested_sides': [],
                'dish_role': 'main',
                'balance_note': 'Unsafe.',
            },
            {
                'title': 'Still Not Food',
                'ingredients': ['motor oil', 'salt', 'water'],
                'directions': ['Mix it', 'Heat it', 'Serve it'],
                'summary': 'Still unsafe.',
                'servings': '1',
                'suggested_sides': [],
                'dish_role': 'main',
                'balance_note': 'Unsafe.',
            },
        ]

        with self.assertRaises(helperfuncs.AIRecipeGenerationError):
            helperfuncs.AICreateMeal('mystery ingredients', 'make something weird')

        self.assertEqual(mock_json_completion.call_count, 4)

    @patch('mealcurator.helperfuncs.OpenAI')
    @patch.object(helperfuncs.AICreateMeal, '_json_completion')
    def test_ai_recipe_requires_balance_guidance_for_side_dishes(self, mock_json_completion, mock_openai):
        mock_json_completion.side_effect = [
            {'allowed': True, 'reason': 'Looks like a recipe request.'},
            {
                'title': 'Tomato Salad',
                'ingredients': ['tomatoes', 'olive oil', 'salt'],
                'directions': ['Slice tomatoes.', 'Season them.', 'Serve.'],
                'summary': 'A simple tomato salad.',
                'servings': '2',
                'suggested_sides': [],
                'dish_role': 'side',
                'balance_note': 'Nice side salad.',
            },
            {
                'title': 'Tomato Salad With Feta',
                'ingredients': ['tomatoes', 'olive oil', 'salt', 'feta', 'basil'],
                'directions': ['Slice tomatoes.', 'Dress with oil and salt.', 'Top with feta and basil and serve with grilled chicken or crusty bread.'],
                'summary': 'A bright tomato salad with a salty feta finish.',
                'servings': '2',
                'suggested_sides': ['Grilled chicken', 'Crusty bread'],
                'dish_role': 'side',
                'balance_note': 'This is a side dish; pair it with grilled chicken and bread or beans to make the meal more balanced.',
            },
            {
                'passes': True,
                'is_recipe': True,
                'is_human_food': True,
                'respects_request': True,
                'meal_balance_clear': True,
                'foodie_quality': True,
                'score': 8,
                'reason': 'Good side dish with clear pairings.',
                'retry_feedback': ''
            },
        ]

        ai_meal = helperfuncs.AICreateMeal('tomatoes, olive oil, basil', 'make a simple summer tomato side dish')

        self.assertEqual(ai_meal.recipe['title'], 'Tomato Salad With Feta')
        self.assertEqual(mock_json_completion.call_count, 4)
