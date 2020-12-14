from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from .models import *
from random import randint
import json
from . import serializers
import requests
from datetime import datetime

# Meta API classes


class AddView(APIView):

    def __init__(self):
        self.serializer = None

    def post(self, request):
        api_object = self.serializer(data=request.data)
        if api_object.is_valid():
            api_object.save()
            return Response(status=201)
        else:
            return Response(status=100)


class RemoveView(APIView):

    def __init__(self):
        self.model = None

    def post(self, request):
        self.model.objects.get(id=request.data['id']).delete()
        return Response(status=200)


class GetView(APIView):

    def __init__(self):
        self.model = None
        self.serializer = None

    def get_objects_to_response(self, request):
        pass

    def get(self, request):
        api_objects = self.get_objects_to_response(request)
        serializer = self.serializer(api_objects, many=True)
        return Response(serializer.data)


class AddToGroupView(APIView):

    def __init__(self):
        self.model = None
        self.group_model = None

    def post(self, request):
        model_id = request.data['id']
        group_id = request.data['group_id']
        self.model.objects.get(id=model_id).group.add(self.group_model.objects.get(id=group_id))
        return Response(status=200)


class RemoveFromGroupView(APIView):
    def __init__(self):
        self.model = None
        self.group_model = None

    def post(self, request):
        model_id = request.data['id']
        group_id = request.data['group_id']
        self.model.objects.get(id=model_id).group.remove(self.group_model.objects.get(id=group_id))
        return Response(status=200)


# Scooter API


class GetScooterView(GetView):

    def __init__(self):
        self.model = Scooter
        self.serializer = serializers.ScooterSerializer

    def get_objects_to_response(self, request):
        api_objects = self.model.objects.all()
        if 'id' in request.query_params:
            api_objects = api_objects.filter(id=request.query_params['id'])
        if 'group' in request.query_params:
            api_objects = api_objects.filter(group=request.query_params['group'])
        if 'status' in request.query_params:
            api_objects = api_objects.filter(status=request.query_params['status'])
        return api_objects


class AddScooterView(AddView):

    def __init__(self):
        self.serializer = serializers.ScooterSerializer


class RemoveScooterView(RemoveView):

    def __init__(self):
        self.model = Scooter


class ChangeScooterStatusView(APIView):

    def post(self, request):
        new_status = request.data['status']
        scooter = Scooter.objects.get(id=request.data['id'])
        scooter.status = new_status
        scooter.save()
        return Response(status=200)


class AddScooterToGroupView(AddToGroupView):

    def __init__(self):
        self.model = Scooter
        self.group_model = ScootersGroup


class RemoveScooterFromGroupView(RemoveFromGroupView):

    def __init__(self):
        self.model = Scooter
        self.group_model = ScootersGroup


class ChangeScooterDataView(APIView):

    def post(self, request):
        data = request.data
        scooter = Scooter.objects.get(id=request.data['id'])
        if 'status' in data:
            scooter.status = data['status']
        if 'name' in data:
            scooter.name = data['name']
        if 'alert' in data:
            scooter.alert = data['alert']
        if 'coord_x' in data:
            scooter.coord_x = data['coord_x']
        if 'coord_y' in data:
            scooter.coord_y = data['coord_y']
        if 'group' in data:
            scooter.group = data['group']
        scooter.save()
        return Response(status=200)


# Client API


class GetClientView(GetView):

    def __init__(self):
        self.model = Client
        self.serializer = serializers.ClientSerializer

    def get_objects_to_response(self, request):
        api_objects = self.model.objects.all()
        if 'id' in request.query_params:
            api_objects = api_objects.filter(id=request.query_params['id'])
        else:
            api_objects = []
        return api_objects


class AddClientView(AddView):

    def __init__(self):
        self.serializer = serializers.ClientSerializer


class ChangeClientStatusView(APIView):

    def post(self, request):
        new_status = request.data['status']
        client = Client.objects.get(id=request.data['id'])
        client.status = new_status
        client.save()
        return Response(status=200)


class AddClientToGroupView(AddToGroupView):

    def __init__(self):
        self.model = Client
        self.group_model = ClientsGroup


class RemoveClientFromGroupView(RemoveFromGroupView):

    def __init__(self):
        self.model = Client
        self.group_model = ClientsGroup


# Order API

class GetOrderView(GetView):

    def __init__(self):
        self.model = Order
        self.serializer = serializers.OrderSerializer

    def get_objects_to_response(self, request):
        api_objects = self.model.objects.all()
        if 'client' in request.query_params:
            api_objects = api_objects.filter(client=request.query_params['client'])
        elif 'id' in request.query_params:
            api_objects = api_objects.filter(id=request.query_params['id'])
        else:
            api_objects = []
        if 'is_paid' in request.query_params:
            api_objects = api_objects.filter(is_paid=request.query_params['is_paid'])
        return api_objects


class AddOrderView(APIView):

    def post(self, request):
        date = datetime.strptime(request.data['date'], "%d-%m-%Y")
        start_time = datetime.strptime(request.data['start_time'], "%H:%M:%S")
        finish_time = datetime.strptime(request.data['finish_time'], "%H:%M:%S")
        delta = finish_time - start_time
        scooter = request.data['scooter']
        client = request.data['client']
        rate = request.data['rate']
        rate_object = Rate.objects.filter(id=rate)
        if not rate:
            return Response(status=400)
        rate_object = rate_object.get(id=rate)
        long = delta.seconds/60
        cost = float(rate_object.rate)*long
        new_order = Order.objects.create(start_time=start_time, finish_time=finish_time,
                                         scooter=Scooter.objects.get(id=scooter), client=Client.objects.get(id=client),
                                         rate=Rate.objects.get(id=rate), cost=cost, date=date)
        new_order.save()
        return Response(json.dumps({'id': new_order.id}), status=200)


class RemoveOrderView(RemoveView):

    def __init__(self):
        self.model = Order


class SetPaymentTrueView(APIView):

    def post(self, request):
        order = Order.objects.get(id=request.data['order_id'])
        order.is_paid = True
        return Response(status=200)


class GetTransactionView(GetView):

    def __init__(self):
        self.model = Transaction
        self.serializer = serializers.TransactionSerializer

    def get_objects_to_response(self, request):
        api_objects = self.model.objects.all()
        return api_objects


# Rate API

class GetRateView(GetView):

    def __init__(self):
        self.model = Rate
        self.serializer = serializers.RateSerializer

    def get_objects_to_response(self, request):
        api_objects = self.model.objects.all()
        if 'id' in request.query_params:
            api_objects = api_objects.filter(id=request.query_params['id'])
        if 'group' in request.query_params:
            api_objects = api_objects.filter(group=request.query_params['group'])
        return api_objects


class AddRateView(AddView):

    def __init__(self):
        self.serializer = serializers.RateSerializer


class RemoveRateView(RemoveView):

    def __init__(self):
        self.model = Rate


class ChangeRateDataView(APIView):

    def post(self, request):
        data = request.data
        rate = Rate.objects.get(id=request.data['id'])
        if 'cost' in data:
            rate.cost = data['cost']
        if 'name' in data:
            rate.name = data['name']
        if 'group' in data:
            rate.group = data['group']
        rate.save()
        return Response(status=200)


class AddRateToGroupView(AddToGroupView):

    def __init__(self):
        self.model = Rate
        self.group_model = RateGroup


class RemoveRateFromGroupView(RemoveFromGroupView):

    def __init__(self):
        self.model = Rate
        self.group_model = RateGroup

# Scooters group API


class GetScootersGroupView(GetView):

    def __init__(self):
        self.model = ScootersGroup
        self.serializer = serializers.ScootersGroupSerializer

    def get_objects_to_response(self, request):
        api_objects = self.model.objects.all()
        if 'id' in request.query_params:
            api_objects = api_objects.filter(id=request.query_params['id'])
        return api_objects


class RemoveScootersGroupView(RemoveView):

    def __init__(self):
        self.model = ScootersGroup


class AddScootersGroupView(AddView):

    def __init__(self):
        self.serializer = serializers.ScootersGroupSerializer


# Client Group API

class GetClientsGroupView(GetView):

    def __init__(self):
        self.model = ClientsGroup
        self.serializer = serializers.ClientsGroupSerializer

    def get_objects_to_response(self, request):
        api_objects = self.model.objects.all()
        if 'id' in request.query_params:
            api_objects = api_objects.filter(id=request.query_params['id'])
        return api_objects


class RemoveClientsGroupView(RemoveView):

    def __init__(self):
        self.model = ClientsGroup


class AddClientsGroupView(AddView):

    def __init__(self):
        self.serializer = serializers.ClientsGroupSerializer


# RateGroupAPI

class GetRateGroupView(GetView):

    def __init__(self):
        self.model = RateGroup
        self.serializer = serializers.RateGroupSerializer

    def get_objects_to_response(self, request):
        api_objects = self.model.objects.all()
        if 'id' in request.query_params:
            api_objects = api_objects.filter(id=request.query_params['id'])
        return api_objects


class AddRateGroupView(AddView):

    def __init__(self):
        self.serializer = serializers.RateGroupSerializer


class RemoveRateGroupView(RemoveView):

    def __init__(self):
        self.model = RateGroup


class ClientLogInView(APIView):

    def post(self, request):
        data = request.data
        if 'phone' in data and 'name' in data:
            phone = data['phone']
            code = 1234
            api_get_data = '?login=HooinKema&psw=Q314ztb812&phones=' + phone + '&mes=' + str(code) + '&cost=0'
            string = 'https://smsc.ru/sys/send.php' + api_get_data
            requests.get(string)
            users = Client.objects.filter(phone=data['phone'])
            resp = {"code": code}
            if users:
                user = Client.objects.get(phone=data['phone'])
                resp['id'] = user.id
                return HttpResponse(json.dumps(resp), status=200)
            else:
                api_object = serializers.ClientSerializer(data=request.data)
                if api_object.is_valid():
                    api_object.save()
                    return HttpResponse(resp, status=201)
                else:
                    return Response(status=100)
        else:
            return Response(status=400)


class GetPaymentLinkView(APIView):

    def get(self, request):
        return Response({'': ""}, status=200)


class GetGeoZoneView(APIView):

    def get(self, request):
        data = []
        zones = GeoZone.objects.all()
        for zone in zones:
            zone_points = []
            points = GeoPoint.objects.filter(zone=zone.id)
            for point in points:
                zone_points.append([point.lat, point.lon])
            data.append({'type': zone.zone_type, 'points': zone_points})
        return HttpResponse(json.dumps(data), status=200)

