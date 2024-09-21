import json

import mercantile as mercantile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from api.vision.analyzer import getImageByXYZ


def index(request):
    return HttpResponse("Greenuzbekistan.uz api")


def loadMap(request, z, x, y):
    ll = mercantile.ul(x, y, z)

    resp = getImageByXYZ(x, y, z, request, ll.lat, ll.lng)

    return redirect(resp['analyzed_img'])


def getLoadByXYZ(request):
    x, y, z, lat, lng = (request.GET['x'], request.GET['y'], request.GET['z'], request.GET['lat'], request.GET['lng'])

    resp = getImageByXYZ(x, y, z, request, lat, lng)

    return resp


@method_decorator(csrf_exempt)
def loadByXYZ(request):
    data = json.loads(request.body)
    x, y, z, lat, lng = (data['x'], data['y'], data['z'], data['lat'], data['lng'])

    resp = getImageByXYZ(x, y, z, request, lat, lng)

    return JsonResponse(resp)


@method_decorator(csrf_exempt)
def loadAllByXYZ(request):
    data = json.loads(request.body)

    resp = []
    p = []

    for groups in data:
        gr = []

        info = {
            "totalArea": 0,
            "totalTree": 0,
            "percent": 0
        }

        for region in groups:
            perc = getImageByXYZ(region['x'], region['y'], region['z'], request, region['lat'], region['lng'])

            info["totalTree"] += perc['area']
            info["totalArea"] += perc['total_area']
            info["percent"] += perc['perc']

            gr.append(perc)

        info["percent"] = info["percent"] / len(gr)

        resp.append(gr)
        p.append(info)

    return JsonResponse({"data": resp, "percentage": p})
