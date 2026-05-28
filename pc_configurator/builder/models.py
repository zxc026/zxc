from django.db import models

class CPU(models.Model):
    name = models.CharField(max_length=100)
    socket = models.CharField(max_length=50)  # например, "AM4", "LGA1700"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tdp = models.IntegerField(help_text="Тепловыделение в Вт")
    integrated_graphics = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Motherboard(models.Model):
    name = models.CharField(max_length=100)
    socket = models.CharField(max_length=50)
    form_factor = models.CharField(max_length=20)  # ATX, Micro-ATX, Mini-ITX
    ram_slots = models.IntegerField()
    ram_type = models.CharField(max_length=10)     # DDR4, DDR5
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class GPU(models.Model):
    name = models.CharField(max_length=100)
    length_mm = models.IntegerField()
    power_connectors = models.CharField(max_length=50)  # например, "2x8-pin"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tdp = models.IntegerField(help_text="Тепловыделение в Вт", default=150)

    def __str__(self):
        return self.name

# Аналогично для RAM, Storage, PowerSupply, Case

class RAM(models.Model):
    name = models.CharField(max_length=100)
    ram_type = models.CharField(max_length=10)  # DDR4, DDR5
    capacity_gb = models.IntegerField()
    speed_mhz = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Storage(models.Model):
    name = models.CharField(max_length=100)
    storage_type = models.CharField(max_length=10)  # SSD, HDD
    capacity_gb = models.IntegerField()
    interface = models.CharField(max_length=10)  # SATA, NVMe
    price = models.DecimalField(max_digits=10, decimal_places=2)

class PowerSupply(models.Model):
    name = models.CharField(max_length=100)
    wattage = models.IntegerField(help_text="Мощность блока питания в Ваттах")
    efficiency_rating = models.CharField(max_length=10)  # Bronze, Gold, Platinum
    price = models.DecimalField(max_digits=10, decimal_places=2)