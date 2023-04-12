from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch.exceptions import NotFoundError
from django_elasticsearch_dsl.registries import registry
from .models import Safari


@registry.register_document
class SafariDocument(Document):
    class Index:
        name = 'safari'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    id = fields.IntegerField(attr='id')
    name = fields.TextField()
    url = fields.TextField()
    price = fields.FloatField()
    max_price = fields.FloatField()
    ratingsQuantity = fields.IntegerField()
    ratingsAverage = fields.FloatField()

    tour_data = fields.NestedField(properties={
        'overview': fields.NestedField(properties={
            'route_data': fields.ObjectField(properties={
                'days': fields.TextField(),
                'days_route': fields.TextField(),
            }),
            'tour_features': fields.ObjectField(properties={
                'title': fields.TextField(),
                'description': fields.TextField(),
            }),
            'route_description': fields.TextField(),
            'accommodation_and_meals': fields.NestedField(properties={
                'day': fields.TextField(),
                'meals': fields.TextField(),
                'accommodation': fields.ObjectField(properties={
                    'image': fields.TextField(),
                    'title': fields.TextField(),
                    'description': fields.TextField(),
                })
            }),
            'activities_and_transportation': fields.TextField(),
        }),
    })

    inclusions_data = fields.NestedField(properties={
        'inclusions': fields.ObjectField(properties={
            'included': fields.TextField(multi=True),
            'excluded': fields.TextField(multi=True),
        }),
    })

    getting_there_data = fields.TextField(multi=True)

    day_by_day = fields.NestedField(properties={
        'image': fields.TextField(),
        'description': fields.TextField(),
        'destination': fields.TextField(),
    })


    class Django:
        model = Safari
