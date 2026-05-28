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

    def __str__(self):
        return self.name

# Аналогично для RAM, Storage, PowerSupply, Case