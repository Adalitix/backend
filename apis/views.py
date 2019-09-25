from .models import Layer, File, Project, Revision
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from geoserver.catalog import Catalog
from geoserver.support import build_url
from django.core.serializers import serialize
from django.forms.models import model_to_dict

adalitix_catalog = Catalog("http://geoserver:8080/geoserver/rest/")


# TODO add permissions checks
def clipper_check_status(request):
    return JsonResponse({'status': 'Not implemented yet'})


def find_model(name, models):
    for model in models:
        if model["is_current_version"] and model["model_name"] == name:
            return model

    return None


def count_replicas(name, containers):
    return len([container for container in containers if container["model_id"] == name])


def clipper_get_all_app(request):
    # data = json.dumps({"verbose": True})
    #
    # apps = requests.post(
    #     'http://clipper:1338/admin/get_all_applications', data=data).json()
    #
    # models_data = requests.post(
    #     'http://clipper:1338/admin/get_all_models', data=data).json()
    #
    # containers_data = requests.post(
    #     'http://clipper:1338/admin/get_all_containers', data=data).json()
    #
    # for app in apps:
    #     hydrated_models = []
    #     for model in app["linked_models"]:
    #         hydrated_model = find_model(model, models_data)
    #         if hydrated_model is not None:
    #             hydrated_model["replicas"] = count_replicas(
    #                 hydrated_model["container_name"], containers_data)
    #
    #         hydrated_models.append(hydrated_model)
    #
    #     app["linked_models"] = hydrated_models

    apps = [{
        "input_type": "temperature",
        "default_output": "-1.0",
        "latency_slo_micros": 100000,
        "name": "Fenologia",
        "linked_models": [{
            "model_name": "phenology-model",
            "model_version": "5.3",
            "input_type": "temperature",
            "labels": [""],
            "container_name": "default-cluster-avg-model:1",
            "model_data_path": "DEPRECATED",
            "is_current_version": True,
            "replicas": 1
        }]
    }, {
        "input_type": "radar",
        "default_output": "-1.0",
        "latency_slo_micros": 100000,
        "name": "MeteoTN",
        "linked_models": [{
            "model_name": "meteo-pred",
            "model_version": "1",
            "input_type": "radar",
            "labels": [""],
            "container_name": "default-cluster-sum-model:1",
            "model_data_path": "DEPRECATED",
            "is_current_version": True,
            "replicas": 1
        }]
    },
        {
            "input_type": "DTM; ClutterMap; AntennaSpecs",
            "default_output": "-1.0",
            "latency_slo_micros": 100000,
            "name": "LoRa",
            "linked_models": [{
                "model_name": "compute-lora",
                "model_version": "1",
                "input_type": "DTM; ClutterMap; AntennaSpecs",
                "labels": [""],
                "container_name": "default-cluster-avg-model:1",
                "model_data_path": "DEPRECATED",
                "is_current_version": True,
                "replicas": 1
            }]
    }
    ]

    return JsonResponse(apps, safe=False)


def clipper_remove_app(request, app_id):
    if request.method == "DELETE":
        pass
    else:
        return HttpResponse("Method Not Allowed", status=405)


def put_layer(name, data, source_type):
    workspace = "adalitix"
    params = {"configure": "first",
              "coverageName": name} if source_type == "tiff" else dict()

    url = build_url(
        adalitix_catalog.service_url,
        [
            "workspaces",
            workspace,
            "coveragestores" if source_type == "tiff" else "datastores",
            name,
            # "file" is the upload method not the file name
            "file.geotiff" if source_type == "tiff" else "file.shp"
        ],
        params
    )

    headers = {"Content-type": "image/tiff" if source_type ==
               "tiff" else "application/zip"}
    resp = adalitix_catalog.http_request(
        url, method='put', data=data, headers=headers)

    data.close()

    if resp.status_code != 201:
        raise Exception(resp.text)

    # rename shapefile layers so that their name matches the datastore name
    if source_type != "tiff":
        # load the feature type description from geoserver
        url = build_url(
            adalitix_catalog.service_url,
            [
                "workspaces",
                workspace,
                "datastores",
                name,
                "featuretypes.json"
            ],
            dict()
        )

        resp = adalitix_catalog.http_request(
            url, method='get', headers={"Accept": "application/json"})
        if resp.status_code != 200:
            raise Exception(resp.text)

        data = json.loads(resp.text)

        layer_name = data["featureTypes"]["featureType"][0]["name"]

        # update the feature type to change the name
        url = build_url(
            adalitix_catalog.service_url,
            [
                "workspaces",
                workspace,
                "datastores",
                name,
                "featuretypes",
                layer_name
            ],
            dict()
        )

        payload = json.dumps({
            "featureType": {
                "name": name
            }
        })

        resp = adalitix_catalog.http_request(
            url, method='put', data=payload, headers={"Content-type": "application/json", "Accept": "application/json"})

        if resp.status_code != 200:
            raise Exception(resp.text)

    return "Successful upload"


@csrf_exempt
def files(request):
    if request.method == "GET":
        files = list(File.objects.values())
        data = {"results": files}

        return JsonResponse(data, safe=False)
    elif request.method == "POST":
        name = request.GET.get("name", "")
        source_type = request.GET.get("type", "")
        revision = request.GET.get("revision", "")
        if name == "" or source_type == "" or revision == "":
            return HttpResponse("name, revision and type query parameter are required", status=400)

        try:
            data = request.FILES.get("data", None)
            new_file = File.objects.create(
                name=name, revision=Revision.objects.get(id=revision), file_type=source_type)

            put_layer(str(new_file.id), data, source_type)

            values = model_to_dict(new_file)
            values["id"] = new_file.id

            return JsonResponse(values, safe=False)
        except Exception as e:
            print(e)
            return HttpResponse("Upload failed", status=500)
    else:
        return HttpResponse("Method Not Allowed", status=405)


@csrf_exempt
def file_handler(request, id):
    if request.method == "POST":
        try:
            data = request.FILES.get("data", None)
            file_type = File.objects.get(id=id).file_type

            put_layer(id, data, file_type)

            return HttpResponse("Upload successful")
        except Exception as e:
            print(e)
            return HttpResponse("Upload failed", status=500)
    else:
        return HttpResponse("Method Not Allowed", status=405)


@csrf_exempt
def project(request):
    if request.method == "GET":
        projects = list(Project.objects.values())
        data = {"results": projects}

        return JsonResponse(data, safe=False)
    elif request.method == "POST":
        name = request.GET.get("name", "")

        if name == "":
            return HttpResponse("Name parameter is required", status=400)

        new_project = Project.objects.create(name=name)
        values = model_to_dict(new_project)
        values["id"] = new_project.id

        return JsonResponse(values, safe=False)
    else:
        return HttpResponse("Method Not Allowed", status=405)


@csrf_exempt
def revision(request):
    if request.method == "GET":
        revisions = list(Revision.objects.values())
        data = {"results": revisions}

        return JsonResponse(data, safe=False)
    elif request.method == "POST":
        name = request.GET.get("name", "")
        tags = request.GET.get("tags", "")
        project = request.GET.get("project", "")

        if name == "" or project == "":
            return HttpResponse("Name and project parameters is required", status=400)

        new_revision = Revision.objects.create(
            name=name, tags=tags, project=Project.objects.get(id=project))
        values = model_to_dict(new_revision)
        values["id"] = new_revision.id

        return JsonResponse(values, safe=False)
    else:
        return HttpResponse("Method Not Allowed", status=405)


@csrf_exempt
def layer_handler(request):
    if request.method == "GET":
        layers = Layer.objects.all()[:]
        data = {"results": [json.loads(layer["config"])
                            for layer in list(layers.values("config"))]}

        return JsonResponse(data)
    elif request.method == "POST":
        try:
            config = json.loads(request.body)

            if config.get("name", "") == "":
                return HttpResponse("name field in config is required", status=400)

            Layer.objects.create(config=json.dumps(config))

            return HttpResponse("Operation Successful")
        except json.JSONDecodeError:
            return HttpResponse("Invalid json config passed", status=400)
    else:
        return HttpResponse("Method Not Allowed", status=405)


@csrf_exempt
def clipper_proxy(request, model):
    if request.method == "POST":
        try:
            input_json = json.loads(request.body)
            data = json.dumps({
                "input": json.dumps(input_json)
            })

            r = requests.post(
                f"http://query_frontend-42:1337/" + model + f"/predict", data=data)

            return JsonResponse(r.text)
        except json.JSONDecodeError:
            return HttpResponse("Invalid json input passed", status=400)
    else:
        return HttpResponse("Method Not Allowed", status=405)


def predict_pheno(request, days, step):
    data = json.dumps({
        "input": json.dumps({"step": step, 'days': days})
    })

    r = requests.post(
        f"http://query_frontend-42:1337/phenology/predict", data=data)

    return JsonResponse(r.text + "\n", safe=False)
