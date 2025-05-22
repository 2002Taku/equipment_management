from django.shortcuts import render, redirect, get_object_or_404
from .models import ArchiveItem
from .forms import ArchiveReasonForm
from supplies.models import Item
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    # 管理者判定（例: is_staffフラグやカスタム判定に変更可）
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def archive_list(request):
    archived_supplies = ArchiveItem.objects.select_related('item').all()
    return render(request, 'archive/list.html', {'archived_supplies': archived_supplies})

@login_required
@user_passes_test(is_admin)
def archive_hide(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ArchiveReasonForm(request.POST)
        if form.is_valid():
            # 非表示処理
            ArchiveItem.objects.create(item=item, archive_reason=form.cleaned_data['archive_reason'])
            item.is_active = False  # Itemモデルにis_activeフィールドがある前提
            item.save()
            return redirect(reverse('archive:list'))
    else:
        form = ArchiveReasonForm()
    return render(request, 'archive/hide.html', {'item': item, 'form': form})

@login_required
@user_passes_test(is_admin)
def archive_restore(request, item_id):
    archive_item = get_object_or_404(ArchiveItem, id=item_id)
    if request.method == 'POST':
        # 復元処理
        archive_item.item.is_active = True  # Itemモデルにis_activeフィールドがある前提
        archive_item.item.save()
        archive_item.delete()
        return redirect(reverse('archive:list'))
    return redirect(reverse('archive:list'))