from django.shortcuts import render, redirect, get_object_or_404
from .models import Lending
from inventory.models import Equipment, Item
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import timedelta, date

def lending_list(request):
    lendings = Lending.objects.all()
    return render(request, 'lending/lending_list.html', {'lendings': lendings})

def lending_create(request):
    if request.method == 'POST':
        form = LendingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lending:lending_list')
    else:
        form = LendingForm()
    return render(request, 'lending/lending_form.html', {'form': form})

def lending_update(request, pk):
    lending = Lending.objects.get(pk=pk)
    if request.method == 'POST':
        form = LendingForm(request.POST, instance=lending)
        if form.is_valid():
            form.save()
            return redirect('lending:lending_list')
    else:
        form = LendingForm(instance=lending)
    return render(request, 'lending/lending_form.html', {'form': form})

def lending_delete(request, pk):
    lending = Lending.objects.get(pk=pk)
    if request.method == 'POST':
        lending.delete()
        return redirect('lending:lending_list')
    return render(request, 'lending/lending_confirm_delete.html', {'lending': lending})

@login_required
def lending_status(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    lendings = Lending.objects.filter(item=item)
    for lending in lendings:
        lending.is_due_soon_flag = lending.is_due_soon()
    return render(request, 'lending/status.html', {
        'item': item,
        'lendings': lendings,
    })

@login_required
def lending_borrow(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if item.stock <= 0:
        return redirect('lending:status', item_id=item.id)
    if request.method == 'POST':
        Lending.objects.create(
            item=item,
            user=request.user,
            user_name=request.user.get_full_name(),
            user_department=getattr(request.user, 'department', ''),
            borrowed_at=date.today(),
            return_due_date=date.today() + timedelta(days=6)
        )
        item.stock -= 1
        item.save()
        return redirect('lending:status', item_id=item.id)
    return render(request, 'lending/borrow_confirm.html', {'item': item})

@login_required
def lending_return(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    lending = Lending.objects.filter(item=item, user=request.user).first()
    if request.method == 'POST' and lending:
        lending.delete()
        item.stock += 1
        item.save()
        return redirect('lending:status', item_id=item.id)
    return render(request, 'lending/return_confirm.html', {'item': item, 'lending': lending})