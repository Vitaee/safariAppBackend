from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch.exceptions import NotFoundError
from django_elasticsearch_dsl.registries import registry
from .models import Safari

# safari_index = Index('safari')



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
    tour_data = fields.ObjectField()
    inclusions_data = fields.ObjectField()
    getting_there_data = fields.ObjectField()
    day_by_day = fields.ObjectField()

    class Django:
        model = Safari

"""
safari_index.document(Document)

try:
    safari_index.create()
except NotFoundError as e:
    print(f"Error creating index: {e}")
"""