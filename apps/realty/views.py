from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import RealtyForm, RealtyPhotoForm, CatalogFilterForm
from .models import Realty, RealtyPhoto, Favorite


def catalog(request):
    qs = Realty.objects.prefetch_related('photos').select_related('owner')
    form = CatalogFilterForm(request.GET or None)

    if form.is_valid():
        d = form.cleaned_data
        if d.get('price_min') is not None:
            qs = qs.filter(price__gte=d['price_min'])
        if d.get('price_max') is not None:
            qs = qs.filter(price__lte=d['price_max'])
        if d.get('area_min') is not None:
            qs = qs.filter(area__gte=d['area_min'])
        if d.get('area_max') is not None:
            qs = qs.filter(area__lte=d['area_max'])
        if d.get('floors_min') is not None:
            qs = qs.filter(floors__gte=d['floors_min'])
        if d.get('floors_max') is not None:
            qs = qs.filter(floors__lte=d['floors_max'])

    paginator = Paginator(qs, settings.REALTY_PER_PAGE)
    page = paginator.get_page(request.GET.get('page'))

    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(user=request.user).values_list('realty_id', flat=True)
        )

    return render(request, 'realty/catalog.html', {
        'page_obj': page,
        'form': form,
        'favorite_ids': favorite_ids,
        'total': qs.count(),
    })


def realty_detail(request, pk):
    realty = get_object_or_404(Realty.objects.prefetch_related('photos').select_related('owner'), pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, realty=realty).exists()
    return render(request, 'realty/detail.html', {'realty': realty, 'is_favorite': is_favorite})


@login_required
def realty_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Добавление объектов доступно только персоналу.')
        return redirect('realty:catalog')

    form = RealtyForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        photos = request.FILES.getlist('photos')
        if len(photos) > settings.MAX_PHOTOS_PER_REALTY:
            messages.error(request, f'Можно загрузить не более {settings.MAX_PHOTOS_PER_REALTY} фотографий.')
        else:
            with transaction.atomic():
                realty = form.save(commit=False)
                realty.owner = request.user
                realty.save()
                for i, photo_file in enumerate(photos):
                    if photo_file.size > settings.MAX_PHOTO_SIZE:
                        messages.warning(request, f'Фото {i+1} превышает 30 МБ и пропущено.')
                        continue
                    RealtyPhoto.objects.create(realty=realty, image=photo_file, order=i)
            messages.success(request, 'Объект успешно добавлен.')
            return redirect('realty:detail', pk=realty.pk)

    return render(request, 'realty/form.html', {
        'form': form,
        'title': 'Добавить объект',
        'max_photos': settings.MAX_PHOTOS_PER_REALTY,
    })


@login_required
def realty_edit(request, pk):
    realty = get_object_or_404(Realty, pk=pk)
    if not request.user.is_superuser and realty.owner != request.user:
        messages.error(request, 'Нет доступа к редактированию этого объекта.')
        return redirect('realty:detail', pk=pk)

    form = RealtyForm(request.POST or None, instance=realty)
    if request.method == 'POST' and form.is_valid():
        photos = request.FILES.getlist('photos')
        current_count = realty.photos_count()
        available_slots = settings.MAX_PHOTOS_PER_REALTY - current_count

        with transaction.atomic():
            form.save()
            added = 0
            for i, photo_file in enumerate(photos):
                if added >= available_slots:
                    messages.warning(request, 'Достигнут лимит фотографий (10 шт).')
                    break
                if photo_file.size > settings.MAX_PHOTO_SIZE:
                    messages.warning(request, f'Фото {i+1} превышает 30 МБ и пропущено.')
                    continue
                RealtyPhoto.objects.create(
                    realty=realty, image=photo_file,
                    order=current_count + added,
                )
                added += 1
        messages.success(request, 'Объект успешно обновлён.')
        return redirect('realty:detail', pk=pk)

    return render(request, 'realty/form.html', {
        'form': form,
        'realty': realty,
        'title': 'Редактировать объект',
        'photos': realty.photos.all(),
        'max_photos': settings.MAX_PHOTOS_PER_REALTY,
    })


@login_required
def realty_delete(request, pk):
    realty = get_object_or_404(Realty, pk=pk)
    if not request.user.is_superuser and realty.owner != request.user:
        messages.error(request, 'Нет доступа к удалению этого объекта.')
        return redirect('realty:detail', pk=pk)

    if request.method == 'POST':
        realty.delete()
        messages.success(request, 'Объект удалён.')
        return redirect('realty:catalog')

    return render(request, 'realty/confirm_delete.html', {'realty': realty})


@login_required
@require_POST
def delete_photo(request, photo_pk):
    photo = get_object_or_404(RealtyPhoto, pk=photo_pk)
    realty = photo.realty
    if not request.user.is_superuser and realty.owner != request.user:
        return JsonResponse({'error': 'Нет доступа'}, status=403)
    photo.delete()
    return JsonResponse({'ok': True})


@login_required
def favorites(request):
    favs = Favorite.objects.filter(user=request.user).select_related('realty').prefetch_related('realty__photos')
    return render(request, 'realty/favorites.html', {'favorites': favs})


@login_required
@require_POST
def toggle_favorite(request, pk):
    realty = get_object_or_404(Realty, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, realty=realty)
    if not created:
        fav.delete()
        is_favorite = False
    else:
        is_favorite = True
    return JsonResponse({'is_favorite': is_favorite})
