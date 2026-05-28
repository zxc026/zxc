from django.shortcuts import render, get_object_or_404
from .models import CPU, Motherboard, GPU, RAM, Storage, PowerSupply


def configurator(request):
    if request.method == 'POST':
        # Получаем ID выбранных компонентов
        cpu_id = request.POST.get('cpu')
        mb_id = request.POST.get('motherboard')
        gpu_id = request.POST.get('gpu')
        ram_id = request.POST.get('ram')
        storage_id = request.POST.get('storage')
        psu_id = request.POST.get('psu')

        # Загружаем объекты из БД
        cpu = CPU.objects.get(id=cpu_id)
        mb = Motherboard.objects.get(id=mb_id)
        gpu = GPU.objects.get(id=gpu_id)
        ram = RAM.objects.get(id=ram_id)
        storage = Storage.objects.get(id=storage_id)
        psu = PowerSupply.objects.get(id=psu_id)

        errors = []

        # 1. Совместимость CPU и материнской платы
        if cpu.socket != mb.socket:
            errors.append("❌ Процессор и материнская плата несовместимы: разные сокеты.")

        # 2. Совместимость RAM и материнской платы
        if hasattr(mb, 'ram_type') and ram.ram_type != mb.ram_type:
            errors.append(f"❌ Оперативная память ({ram.ram_type}) не совместима с материнской платой ({mb.ram_type}).")

        # 3. Проверка мощности блока питания
        total_power = cpu.tdp + (gpu.tdp if hasattr(gpu, 'tdp') else 150) + 50
        if psu.wattage < total_power:
            errors.append(
                f"⚠️ Блок питания ({psu.wattage} Вт) может не справиться с нагрузкой (~{total_power} Вт). Рекомендуется запас 20%.")

        # Полная стоимость
        total_price = cpu.price + mb.price + gpu.price + ram.price + storage.price + psu.price

        context = {
            'cpus': CPU.objects.all(),
            'motherboards': Motherboard.objects.all(),
            'gpus': GPU.objects.all(),
            'rams': RAM.objects.all(),
            'storages': Storage.objects.all(),
            'psus': PowerSupply.objects.all(),
            'selected': {
                'cpu': cpu,
                'mb': mb,
                'gpu': gpu,
                'ram': ram,
                'storage': storage,
                'psu': psu,
            },
            'total_price': total_price,
            'errors': errors,
        }
        return render(request, 'builder/configurator.html', context)

    else:  # GET-запрос
        context = {
            'cpus': CPU.objects.all(),
            'motherboards': Motherboard.objects.all(),
            'gpus': GPU.objects.all(),
            'rams': RAM.objects.all(),
            'storages': Storage.objects.all(),
            'psus': PowerSupply.objects.all(),
            'selected': {
                'cpu': None,
                'mb': None,
                'gpu': None,
                'ram': None,
                'storage': None,
                'psu': None,
            },
        }
        return render(request, 'builder/configurator.html', context)


def catalog(request):
    """Список всех компонентов по категориям"""
    context = {
        'cpus': CPU.objects.all(),
        'motherboards': Motherboard.objects.all(),
        'gpus': GPU.objects.all(),
        'rams': RAM.objects.all(),
        'storages': Storage.objects.all(),
        'psus': PowerSupply.objects.all(),
    }
    return render(request, 'builder/catalog.html', context)


def component_detail(request, model_type, pk):
    """Детальная страница компонента"""
    models_map = {
        'cpu': CPU,
        'motherboard': Motherboard,
        'gpu': GPU,
        'ram': RAM,
        'storage': Storage,
        'psu': PowerSupply,
    }
    model = models_map.get(model_type.lower())
    if not model:
        from django.http import Http404
        raise Http404("Компонент не найден")

    component = get_object_or_404(model, id=pk)
    return render(request, 'builder/component_detail.html', {'component': component, 'type': model_type})