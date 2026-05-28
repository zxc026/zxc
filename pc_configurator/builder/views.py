from django.shortcuts import render, redirect
from .models import CPU, Motherboard, GPU


def configurator(request):
    if request.method == 'POST':
        cpu_id = request.POST.get('cpu')
        mb_id = request.POST.get('motherboard')
        gpu_id = request.POST.get('gpu')

        cpu = CPU.objects.get(id=cpu_id)
        mb = Motherboard.objects.get(id=mb_id)
        gpu = GPU.objects.get(id=gpu_id)

        errors = []
        if cpu.socket != mb.socket:
            errors.append("Процессор и материнская плата несовместимы: разные сокеты.")

        total_price = cpu.price + mb.price + gpu.price
        # Добавьте остальные компоненты позже

        context = {
            'cpus': CPU.objects.all(),
            'motherboards': Motherboard.objects.all(),
            'gpus': GPU.objects.all(),
            'selected': {'cpu': cpu, 'mb': mb, 'gpu': gpu},
            'total_price': total_price,
            'errors': errors,
        }
        return render(request, 'builder/configurator.html', context)
    else:
        context = {
            'cpus': CPU.objects.all(),
            'motherboards': Motherboard.objects.all(),
            'gpus': GPU.objects.all(),
            'selected': {'cpu': None, 'mb': None, 'gpu': None},   # <-- добавить эту строку
        }
        return render(request, 'builder/configurator.html', context)