from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import ArchiveItem
from supplies.models import Item
from .forms import ArchiveReasonForm

def is_admin(user):
    # 管理者判定（is_staffフラグやカスタム判定に変更可）
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def archive_list(request):
    """
    アーカイブ（非表示）された備品の一覧を表示
    管理者のみアクセス可能
    """
    archived_supplies = ArchiveItem.objects.select_related('item').all()
    return render(request, 'archive/list.html', {'archived_supplies': archived_supplies})

@login_required
@user_passes_test(is_admin)
def archive_hide(request, item_id):
    """
    備品を非表示（アーカイブ）にする処理
    POST: 理由を受け取りアーカイブ化
    GET: 理由入力フォームを表示
    """
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ArchiveReasonForm(request.POST)
        if form.is_valid():
            # アーカイブアイテムを作成し、備品を非表示にする
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
    """
    アーカイブ（非表示）から備品を復元する処理
    POST: 備品を再表示し、アーカイブ記録を削除
    """
    archive_item = get_object_or_404(ArchiveItem, id=item_id)
    if request.method == 'POST':
        # 備品を再表示
        archive_item.item.is_active = True  # Itemモデルにis_activeフィールドがある前提
        archive_item.item.save()
        # アーカイブ記録を削除
        archive_item.delete()
        return redirect(reverse('archive:list'))
    return redirect(reverse('archive:list'))