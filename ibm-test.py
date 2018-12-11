import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
     import Features, CategoriesOptions, EmotionOptions, SentimentOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    iam_apikey='-z3ULU3trXBnNhlm9aAKaVz5Y_WcwuDWW1oVem7V3meI',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api'
)

response = natural_language_understanding.analyze(
    text="It's the most common. Is there good treatment? Then there must be therapies.",
    features=Features(
        emotion=EmotionOptions(),
        categories=CategoriesOptions(),
        sentiment=SentimentOptions())).get_result()
    # features=Features(categories=CategoriesOptions())).get_result()

print(json.dumps(response, indent=2))


