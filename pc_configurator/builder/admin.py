from django.contrib import admin
from .models import CPU, Motherboard, GPU, RAM, Storage, PowerSupply, Build

admin.site.register(CPU)
admin.site.register(Motherboard)
admin.site.register(GPU)
admin.site.register(RAM)
admin.site.register(Storage)
admin.site.register(PowerSupply)
admin.site.register(Build)