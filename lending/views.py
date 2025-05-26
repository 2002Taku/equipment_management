from django.shortcuts import render, redirect, get_object_or_404
from .models import Lending
from supplies.models import Item
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from datetime import timedelta, date

def lending_list(request):
    """
    全ての貸出履歴を一覧表示（管理者用など）
    """
    lendings = Lending.objects.all()
    return render(request, 'lending/lending_list.html', {'lendings': lendings})

def lending_create(request):
    """
    新規貸出申請の作成（フォーム入力→保存）
    """
    if request.method == 'POST':
        form = LendingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lending:lending_list')
    else:
        form = LendingForm()
    return render(request, 'lending/lending_form.html', {'form': form})

def lending_update(request, pk):
    """
    貸出情報の編集
    """
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
    """
    貸出情報の削除
    """
    lending = Lending.objects.get(pk=pk)
    if request.method == 'POST':
        lending.delete()
        return redirect('lending:lending_list')
    return render(request, 'lending/lending_confirm_delete.html', {'lending': lending})

@login_required
def lending_status(request, item_id):
    """
    指定した備品の貸出状況を表示
    - 現在貸出中のユーザー一覧
    - 返却期限が近い場合はフラグを立てる
    """
    item = get_object_or_404(Item, id=item_id)
    lendings = Lending.objects.filter(item=item)
    for lending in lendings:
        lending.is_due_soon_flag = lending.is_due_soon()  # 返却期限が近いか判定
    return render(request, 'lending/status.html', {
        'item': item,
        'lendings': lendings,
    })

@login_required
def lending_borrow(request, item_id):
    """
    備品の貸出申請処理
    - すでに借りていればエラー
    - 在庫がなければエラー
    - POST時に貸出レコード作成＆在庫減少
    """
    item = get_object_or_404(Item, id=item_id)
    # 1ユーザ1備品1回までの貸出制限
    already_borrowed = Lending.objects.filter(item=item, user=request.user).exists()
    if already_borrowed:
        messages.error(request, "すでに貸出済みです")
        return redirect('supplies:detail', item_id=item.id)

    if item.stock <= 0:
        messages.error(request, "在庫がありません")
        return redirect('lending:status', item_id=item.id)
    if request.method == 'POST':
        # 新規貸出レコード作成
        Lending.objects.create(
            item=item,
            user=request.user,
            user_name=request.user.get_full_name(),
            user_department=getattr(request.user, 'department', ''),
            borrowed_at=date.today(),
            return_due_date=date.today() + timedelta(days=6)
        )
        item.stock -= 1  # 在庫数を減らす
        item.save()
        messages.success(request, "貸出申請が完了しました")
        return redirect('lending:status', item_id=item.id)
    return render(request, 'lending/borrow_confirm.html', {'item': item})

@login_required
def lending_return(request, item_id):
    """
    備品の返却処理
    - POST時に貸出レコード削除＆在庫数を戻す
    """
    item = get_object_or_404(Item, id=item_id)
    lending = Lending.objects.filter(item=item, user=request.user).first()
    if request.method == 'POST' and lending:
        lending.delete()
        item.stock += 1  # 在庫数を戻す
        item.save()
        return redirect('lending:status', item_id=item.id)
    return render(request, 'lending/return_confirm.html', {'item': item, 'lending': lending})