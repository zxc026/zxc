from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import CPU, Motherboard, GPU, RAM, Storage, PowerSupply, Build


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
            errors.append(f"⚠️ Блок питания ({psu.wattage} Вт) может не справиться с нагрузкой (~{total_power} Вт).")

        total_price = cpu.price + mb.price + gpu.price + ram.price + storage.price + psu.price

        # Сохраняем текущую сборку в сессии, чтобы потом её можно было сохранить
        request.session['current_build'] = {
            'cpu_id': cpu_id,
            'mb_id': mb_id,
            'gpu_id': gpu_id,
            'ram_id': ram_id,
            'storage_id': storage_id,
            'psu_id': psu_id,
            'total_price': float(total_price),
        }

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

    else:  # GET
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


def my_builds(request):
    """Список сохранённых сборок пользователя (по сессии)"""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    builds = Build.objects.filter(session_key=session_key).order_by('-created_at')
    return render(request, 'builder/my_builds.html', {'builds': builds})


def save_build(request):
    """Сохраняет текущую сборку из сессии в базу данных"""
    if request.method == 'POST':
        build_name = request.POST.get('build_name', 'Моя сборка')
        current_build = request.session.get('current_build')
        if not current_build:
            messages.error(request, "Нет активной сборки для сохранения. Сначала соберите ПК.")
            return redirect('configurator')

        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        # Создаём объект сборки
        Build.objects.create(
            session_key=session_key,
            name=build_name,
            cpu_id=current_build['cpu_id'],
            motherboard_id=current_build['mb_id'],
            gpu_id=current_build['gpu_id'],
            ram_id=current_build['ram_id'],
            storage_id=current_build['storage_id'],
            psu_id=current_build['psu_id'],
        )
        messages.success(request, f"Сборка «{build_name}» успешно сохранена!")
        return redirect('my_builds')
    else:
        return redirect('configurator')


def load_build(request, build_id):
    """Загружает сохранённую сборку в конфигуратор"""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    build = get_object_or_404(Build, id=build_id, session_key=session_key)
    # Сохраняем в сессию текущую сборку
    request.session['current_build'] = {
        'cpu_id': build.cpu_id,
        'mb_id': build.motherboard_id,
        'gpu_id': build.gpu_id,
        'ram_id': build.ram_id,
        'storage_id': build.storage_id,
        'psu_id': build.psu_id,
    }
    # Перенаправляем на конфигуратор – там подхватится из сессии
    return redirect('configurator')


def about(request):
    """Страница 'О проекте'"""
    return render(request, 'builder/about.html')