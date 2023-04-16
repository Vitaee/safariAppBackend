from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from safari import models

class SafariCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/safari/create'

    def test_create_safari_successfully(self):
        data = {
        "imageCover": "https://cloudfront.safaribookings.com/lib/tanzania/tour/1184x259/Serengeti_National_Park_048.jpg",
        "name": "7-Day Northern Parks Budget Safari Tent (Migration)",
        "url": "https://www.safaribookings.com/tours/t9480",
        "price": "2330.00",
        "max_price": "0.00",
        "ratingsQuantity": 272,
        "ratingsAverage": "4.9",
        "tour_data": {
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
                "day_2": {
                    "days": "Day 2",
                    "days_route": "Ngorongoro Crater"
                }
                }
            ],
            "tour_features": [
                {
                "feature_0": {
                    "title": "Mid-range tour",
                    "description": "This mid-range tour uses tented camps."
                },
                "feature_1": {
                    "title": "Private tour",
                    "description": "This tour will be organized exclusively for you and won't be shared with others."
                }
                }
            ],
            "route_description": "Enjoy the best of the Northern parks in 7 days’ time! You'll be visiting Tarangire, the Ngorongoro Crater, Serengeti National Park, Lake Natron and Lake Manyara. Enjoy the beautiful landscape and great views of the animals as you do game drives around the parks. This itinerary offers a unique game drive and walking safari in the Ikona Wildlife Management Area and an overnight stay in a Maasai boma lodge! You also have a chance to see the migration in Serengeti.",
            "accomodaton_and_meals": [
                {
                "accomodation_0": {
                    "day": "7",
                    "meals": "Breakfast & Lunch Included",
                    "accommodation": {
                    "image": "\n                                        End of tour(No accommodation)\n\n\n                                            – Breakfast & Lunch Included\n                                            \n",
                    "title": "End of tour(No accommodation)                                            – Breakfast & Lunch Included",
                    "description": "(No accommodation)"
                    }
                }
                }
            ],
            "activities_and_transportation": [
                "Activities: game drives &  nature hikes/walks",
                "Game drives: pop-up roof 4x4 vehicle"
            ]
            }
        },
        "inclusions_data": {
            "inclusions": {
            "excluded": [
                "International flights (From/to home)",
                "Roundtrip airport transfer",
            ],
            "included": [
                "Park fees (For non-residents)",
                "All activities (Unless labeled as optional)",
            ]
            }
        },
        "getting_there_data": [
            "This tour starts and ends in Arusha",
            "This operator can help select your international flights, but you'll have to book them yourself help",
        ],
        "day_by_day": [
        {
          "day_1": {
            "image": "https://cloudfront.safaribookings.com/lib/tanzania/destination/464x145/Tarangire_National_Park_008.jpg",
            "description": "Today, your safari adventure begins! We pick you up from your hotel in or around Arusha. During the 2.5-hour drive, you will enjoy the view of the beautiful nature, landscapes and local communities. We’ll do a full-day game drive in Tarangire which is famous for its large numbers of elephants, baobab trees and tree-climbing African pythons. At the end of the day, we go to Africa Safari Lake Manyara. First, you can take a dive into the swimming pool!",
            "destination": "Tarangire National Park"
          },
          "day_2": {
            "image": "https://cloudfront.safaribookings.com/lib/tanzania/destination/464x145/Ngorongoro_Conservation_Area_021.jpg",
            "description": "Today we wake up early in the morning and after breakfast, we will drive into the amazing Ngorongoro Crater. The Ngorongoro Crater is the largest intact crater in the world. The crater is home to an estimated 30,000 large mammals. Due to its natural borders, there is an abundance of wildlife throughout the conservation area. It is also home to the Big Five including the African black rhino, as well as hyena and zebra to name a few. At the end of the day we head to Ndutu/South Serengeti where we overnight at Africa Safari South Serengeti. The area is famous for the calving season of the Great Migration, an absolute highlight of the annual wildebeest migration.",
            "destination": "Ngorongoro Crater"
          }
        }
      ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Safari.objects.count(), 1)
        self.assertEqual(models.Safari.objects.get().name, '7-Day Northern Parks Budget Safari Tent (Migration)')

    def test_create_safari_with_invalid_data(self):
        data = {
            "imageCover": "https://cloudfront.safaribookings.com/lib/tanzania/tour/1184x259/Serengeti_National_Park_048.jpg",
            "name": "7-Day Northern Parks Budget Safari Tent (Migration)",
            "url": "https://www.safaribookings.com/tours/t9480",
            "price": "invalid price",
            "max_price": "0.00",
            "ratingsQuantity": 272,
            "ratingsAverage": "4.9",
            "tour_data": {
                "overview": {
                    "route_data": [
                        {
                            "day_0": {
                                "days": "Start",
                                "days_route": "Arusha (Day 1)"
                            }
                        }
                    ]
                }
            },
            "inclusions_data": {
                "inclusions": {
                    "excluded": [
                        "International flights (From/to home)",
                        "Roundtrip..."
                    ]
                }
            }
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Safari.objects.count(), 0)