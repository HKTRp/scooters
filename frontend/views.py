from django.shortcuts import render
from api.models import *
import os


def dashboard(request):

    scooters_data = Scooter.objects.all()
    count = len(scooters_data)
    online = len(scooters_data.filter(status="ON"))
    under_repair = len(scooters_data.filter(status="UR"))
    rented = len(scooters_data.filter(status="RT"))
    scooters = {'count': count, 'online': online, 'under_repair': under_repair, 'rented': rented}

    alerts_data = Alert.objects.filter(checked=False)
    hijacking = len(alerts_data.filter(alert_type="HJ"))
    low_battery = len(alerts_data.filter(alert_type="LB"))
    leaving_area = len(alerts_data.filter(alert_type="LA"))
    lost_connection = len(alerts_data.filter(alert_type="LC"))
    payment_failed = len(alerts_data.filter(alert_type="PF"))

    alerts = {'hijacking': hijacking, 'low_battery': low_battery, 'leaving_area': leaving_area,
              'lost_connection': lost_connection, 'payment_failed': payment_failed}

    return render(request, 'frontend/dashboard_content.html', context={'scooters': scooters, 'alerts': alerts})


def scooters_list_view(request):
    scooters_list = Scooter.objects.all()
    if 'group' in request.GET:
        if request.GET.get('group') != 'all':
            scooters_list = scooters_list.filter(scooter_group=request.GET.get('group'))
    if 'status' in request.GET:
        if request.GET.get('status') != 'all':
            scooters_list = scooters_list.filter(status=request.GET.get('status'))
    if 'alert' in request.GET:
        if request.GET.get('alert') != 'all':
            scooters_list = scooters_list.filter(alert=request.GET.get('alert'))
    groups = ScootersGroup.objects.all()
    return render(request, 'frontend/scooters_list.html', context={'scooters': scooters_list, 'groups': groups})


def scooter_card_view(request, scooter_id):
    obj = Scooter.objects.get(id=scooter_id)
    i_c_s = False
    if request.method == "POST":
        tracker_id = obj.tracker_id
        command = 'mosquitto_pub -h scooteradminpanel.ru -p 8883 -t "{}/cmd" -m "{}" --capath /etc/ssl/certs/'
        data = request.POST
        if 'scooter' in data:
            if data['scooter'] == 'on':
                command = command.format(tracker_id, '011')
            elif data['scooter'] == 'off':
                command = command.format(tracker_id, '012')
        elif 'headlight' in data:
            if data['headlight'] == 'on':
                command = command.format(tracker_id, '013')
            elif data['headlight'] == 'off':
                command = command.format(tracker_id, '014')
        elif 'lock' in data:
            if data['lock'] == 'on':
                command = command.format(tracker_id, '015')
            elif data['lock'] == 'off':
                command = command.format(tracker_id, '016')
        elif 'speed_limit' in data:
            if data['speed_limit'] == 'mode_0':
                command = command.format(tracker_id, '0220')
            elif data['speed_limit'] == 'mode_1':
                command = command.format(tracker_id, '0221')
            elif data['speed_limit'] == 'mode_2':
                command = command.format(tracker_id, '0222')
        elif 'syren' in data:
            command = command.format(tracker_id, '0211')
        elif 'open_battery_cap' in data:
            command = command.format(tracker_id, '0212')
        os.system(command)
        i_c_s = True
    return render(request, 'frontend/scooter_card.html', context={'scooter': obj, 'is_command_sent': i_c_s})


def create_new_scooter_view(request):
    is_m_c = False

    if request.method == 'POST':
        data = request.POST
        photo = 'images/image.png'
        if data.get('photo'):
            photo = data.get('photo')
        new_scooter = Scooter.objects.create(scooter_name=data.get('title'), description=data.get('description'),
                                             photo=photo, tracker_id=data.get('tracker_id'))
        new_scooter.scooter_group.set(data.get('scooter_group'))
        new_scooter.save()
        is_m_c = True

    groups = ScootersGroup.objects.all()
    return render(request, 'frontend/add_new_scooter.html', context={'groups': groups, 'is_model_created': is_m_c})


def redact_scooter_view(request, scooter_id):
    is_m_c = False
    redacting_scooter = Scooter.objects.get(id=scooter_id)

    if request.method == 'POST':
        data = request.POST
        redacting_scooter.scooter_name = data.get('title')
        redacting_scooter.description = data.get('description')
        if data.get('photo'):
            redacting_scooter.photo = data.get('photo')
        redacting_scooter.tracker_id = data.get('tracker_id')
        redacting_scooter.scooter_group.set(data.get('scooter_group'))
        redacting_scooter.save()
        is_m_c = True

    groups = ScootersGroup.objects.all()
    return render(request, 'frontend/add_new_scooter.html',
                  context={'groups': groups, 'is_model_created': is_m_c, 'current': redacting_scooter})


def client_list_view(request):
    clients_list = Client.objects.all()
    if 'group' in request.GET:
        if request.GET.get('group') != 'all':
            clients_list = clients_list.filter(client_group=request.GET.get('group'))
    if 'status' in request.GET:
        if request.GET.get('status') != 'all':
            clients_list = clients_list.filter(status=request.GET.get('status'))
    groups = ClientsGroup.objects.all()
    return render(request, 'frontend/clients_list.html', context={'clients': clients_list, 'groups': groups})


def client_card_view(request, client_id):
    client = Client.objects.get(id=client_id)
    if 'ban' in request.GET:
        if request.GET.get('ban') == "True":
            client.status = 'BD'
            client.save()
        elif request.GET.get('ban') == "False":
            client.status = 'AC'
            client.save()
    return render(request, 'frontend/client_card.html', context={'client': client})


def alerts_list_view(request):
    alerts = Alert.objects.all()
    if 'alert' in request.GET:
        if request.GET.get('alert') != 'all':
            alerts = alerts.filter(alert_type=request.GET.get('alert'))
    alerts = alerts.order_by('-gotten')
    alerts = alerts.order_by('checked')
    return render(request, 'frontend/alerts_list.html', context={'alerts': alerts})


def alert_card_view(request, alert_id):
    alert = Alert.objects.get(id=alert_id)
    alert.checked = True
    alert.save()
    return render(request, 'frontend/alert_card.html', context={'alert': alert})


def alert_settings_view(request):
    is_settings_changed = False
    settings = AlarmSettingsSingleton.objects.get(id=2)

    if request.method == 'POST':
        data = request.POST
        settings.low_battery = float(data.get('battery'))
        settings.leaving_area_time = float(data.get('area_lost_time'))
        settings.hijacking_speed = float(data.get('speed'))
        settings.lost_track = float(data.get('track_lost_time'))
        is_settings_changed = True
        settings.save()
    cont = {'settings': settings, 'is_settings_changed': is_settings_changed}
    return render(request, 'frontend/alert_settings.html', context=cont)

