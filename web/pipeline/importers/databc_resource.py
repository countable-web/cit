import requests

from django.apps import apps

from pipeline.models.general import DataSource
from pipeline.importers.utils import import_data_into_point_model

API_URL = "https://catalogue.data.gov.bc.ca/api/3/action/datastore_search?resource_id={resource_id}&limit=10000"


def import_databc_resources(resource_type):
    databc_resource_names = DataSource.objects.filter(source_type="api").values_list("name", flat=True)
    if resource_type not in ['all', *databc_resource_names]:
        print("Error: Resource type {} not supported".format(resource_type))
        return

    if resource_type == "all":
        for available_resource_type in databc_resource_names:
            import_resource(available_resource_type)
    else:
        import_resource(resource_type)


def import_resource(resource_type):
    data_source = DataSource.objects.get(name=resource_type)
    resource_id = data_source.resource_id
    response = requests.get(API_URL.format(resource_id=resource_id))

    if response.status_code != 200:
        print("Failed to download dataset {} {}".format(resource_type, resource_id))
        print("Error: {} {}".format(response.status_code, response.content))
        return

    data = response.json()["result"]["records"]

    for row in data:
        model_class = apps.get_model("pipeline", data_source.model_name)
        import_data_into_point_model(resource_type, model_class, row)
