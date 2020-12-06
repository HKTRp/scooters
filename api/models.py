from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ClientsGroup(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ScootersGroup(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class RateGroup(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Scooter(models.Model):
    scooter_name = models.CharField(max_length=50)
    status_choices = [
        ('ON', 'Online'),
        ('UR', 'Under repair'),
        ('RT', 'Rented'),
        ('BK', 'Booked')
    ]
    status = models.CharField(max_length=2, choices=status_choices, default='ON')

    alerts_choices = [
        ('OK', 'No alerts'),
        ('HJ', 'Hijacking'),
        ('LC', 'Lost connection'),
        ('LA', 'Leaving area'),
        ('LB', 'Low battery'),
    ]

    limits = [(10, '10 км/ч'), (15, '15 км/ч'), (25, '25 км/ч')]

    alert_status = models.CharField(max_length=2, choices=alerts_choices, default='OK')
    battery = models.IntegerField(default=40000)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    description = models.TextField(blank=True, default="Без описания")
    scooter_group = models.ManyToManyField(ScootersGroup, blank=True, default=[0])
    photo = models.ImageField(default='images/image.png', upload_to='images/')
    tracker_id = models.CharField(default='0000000000000000', max_length=16)
    speed_limit = models.IntegerField(default=10, choices=limits)
    lamp = models.BooleanField(default=False)
    engine = models.BooleanField(default=False)
    lock = models.BooleanField(default=True)
    #last_ping = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.scooter_name + " " + str(self.id)


class Client(models.Model):
    client_name = models.CharField(max_length=30, default='-')
    surname = models.CharField(max_length=30, default='-')
    status_choices = [
        ('AC', 'Active'),
        ('WV', 'Wait for verification'),
        ('BD', 'Blocked')
    ]
    status = models.CharField(max_length=2, choices=status_choices, default='WV')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    client_photo = models.ImageField(blank=True, default='images/image.png')
    client_group = models.ManyToManyField(ClientsGroup, blank=True, default=0)
    phone = models.CharField(max_length=15, default="0", unique=True)

    def __str__(self):
        return self.client_name + " " + self.phone


class Rate(models.Model):
    name = models.CharField(max_length=30, default="Default rate")
    rate = models.DecimalField(max_digits=15, decimal_places=2)
    group = models.ManyToManyField(RateGroup)

    def __str__(self):
        return self.name


class Alert(models.Model):
    alerts_choices = [
        ('HJ', 'Hijacking'),
        ('LC', 'Lost connection'),
        ('LA', 'Leaving area'),
        ('LB', 'Low battery'),
        ('FP', 'Failed payment')
    ]
    alert_type = models.CharField(max_length=6, default='test', choices=alerts_choices)
    alert_owner = models.ForeignKey(Scooter, on_delete=models.CASCADE)
    alert_order = models.ForeignKey(Client, blank=True, on_delete=models.CASCADE)
    gotten = models.DateTimeField(default=timezone.now)


class Order(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    finish_time = models.TimeField()
    scooter = models.ForeignKey(Scooter, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE)

    def __str__(self):
        return self.client.__str__() + " " + self.scooter.scooter_name + " " + str(self.date) + " " + str(self.id)


class Transaction(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

