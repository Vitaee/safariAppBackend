from django.test import TestCase
from rest_framework.test import APIClient
from safari import models, serializers, views
from faker import Faker
import random

class SafariFactory:
    @staticmethod
    def create():
        fake = Faker()
        models.Safari.objects.create(
            imageCover = fake.image_url(width=800, height=600),
            name = fake.sentence(nb_words=3),
            url = fake.image_url(width=800, height=600),
            price = random.randint(100, 1000),
            max_price = random.randint(600, 1800),
            ratingsQuantity = random.randint(10,99),
            ratingsAverage = "3.5",
            tour_data = {
                "overview": {
                "route_data": [
                    {
                    "day_0": {
                        "days": "Start",
                        "days_route": "Arusha (Day 1)"
                    },
                    "day_1": {
                        "days": "Day 1",
                        "days_route": "Tarangire NP"
                    },
                    }
                ],
                "tour_features": [
                    {
                    "feature_0": {
                        "title": "Mid-range tour",
                        "description": "This mid-range tour uses tented camps."
                    }
                    }
                ],
                "route_description": "",
                "accomodaton_and_meals": [
                    {
                    "accomodation_0": {
                        "day": "7",
                        "meals": "Breakfast & Lunch Included",
                        "accommodation": {
                        "image": "",
                        "title": "End of tour(No accommodation)",
                        "description": "(No accommodation)"
                        }
                    }
                    }
                ],
                "activities_and_transportation": [
                    "Activities: game drives &  nature hikes/walks",
                ]
                }
            }, 
            inclusions_data= {
                "inclusions": {
                "excluded": [
                    "International flights (From/to home)",
                ],
                "included": [
                    "Park fees (For non-residents)",
                ]
                }
            },
            getting_there_data = ["This tour starts and ends in Arusha"],
            day_by_day=[
                {
                "day_1": {
                    "image": "https://cloudfront.safaribookings.com/lib/tanzania/destination/464x145/Tarangire_National_Park_008.jpg",
                    "description": "Today, your safari adventure begins! We pick you up from your hotel in or around Arusha. During the 2.5-hour drive, you will enjoy the view of the beautiful nature, landscapes and local communities. We’ll do a full-day game drive in Tarangire which is famous for its large numbers of elephants, baobab trees and tree-climbing African pythons. At the end of the day, we go to Africa Safari Lake Manyara. First, you can take a dive into the swimming pool!",
                    "destination": "Tarangire National Park"
                }
                }
            ]
        )

class SafariAllViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/safari/all'
        self.serializer = serializers.SafariCreateSerializer()
        for i in range(10):
            SafariFactory.create()

    def test_list_safari_with_pagination(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()['results']), 5 )
        self.assertEqual('next' in response.json(), True)

        next_url = response.json()['next']
        response = self.client.get(next_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 5)
        self.assertEqual(response.json()["previous"] != "", True)