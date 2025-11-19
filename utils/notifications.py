"""
在庫管理システム - 通知システム
utils/notifications.py
"""
from datetime import datetime
from flask_mail import Message
from flask import url_for

from models import db, Notification, User, UserRole, Stock
from app import mail


def create_notification(user_id, title, message, type='info', link=None):
    """通知作成
    
    Args:
        user_id: ユーザーID
        title: 通知タイトル
        message: 通知メッセージ
        type: 通知タイプ (info/warning/error/success)
        link: リンクURL
    
    Returns:
        Notification: 作成された通知
    """
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=type,
        link=link
    )
    db.session.add(notification)
    db.session.commit()
    return notification


def notify_users(user_ids, title, message, type='info', link=None):
    """複数ユーザーに通知
    
    Args:
        user_ids: ユーザーIDのリスト
        title: 通知タイトル
        message: 通知メッセージ
        type: 通知タイプ
        link: リンクURL
    """
    for user_id in user_ids:
        create_notification(user_id, title, message, type, link)


def notify_role(role, title, message, type='info', link=None):
    """特定ロールのユーザー全員に通知
    
    Args:
        role: UserRole
        title: 通知タイトル
        message: 通知メッセージ
        type: 通知タイプ
        link: リンクURL
    """
    users = User.query.filter_by(role=role, active=True).all()
    for user in users:
        create_notification(user.id, title, message, type, link)


def notify_admins(title, message, type='info', link=None):
    """管理者全員に通知"""
    notify_role(UserRole.ADMIN, title, message, type, link)


def notify_managers(title, message, type='info', link=None):
    """マネージャー全員に通知"""
    users = User.query.filter(
        User.role.in_([UserRole.ADMIN, UserRole.MANAGER]),
        User.active == True
    ).all()
    for user in users:
        create_notification(user.id, title, message, type, link)


# ========================================
# 在庫関連通知
# ========================================

def notify_low_stock(stock: Stock):
    """在庫不足通知
    
    Args:
        stock: 在庫オブジェクト
    """
    title = '在庫不足アラート'
    message = f'{stock.product_name}の在庫が最小在庫数を下回りました（現在庫: {stock.quantity}）'
    link = url_for('inventory.index', _external=False)
    
    # 管理者とマネージャーに通知
    notify_managers(title, message, type='warning', link=link)
    
    # メール通知（オプション）
    send_low_stock_email(stock)


def notify_expiring_soon(stock: Stock):
    """期限切れ間近通知
    
    Args:
        stock: 在庫オブジェクト
    """
    if not stock.expiry_date:
        return
    
    days_until_expiry = (stock.expiry_date - datetime.utcnow()).days
    
    title = '期限切れ間近アラート'
    message = f'{stock.product_name}の有効期限が{days_until_expiry}日後に切れます'
    link = url_for('inventory.index', _external=False)
    
    notify_managers(title, message, type='warning', link=link)


def notify_stock_zero(stock: Stock):
    """在庫ゼロ通知
    
    Args:
        stock: 在庫オブジェクト
    """
    title = '在庫ゼロアラート'
    message = f'{stock.product_name}の在庫がゼロになりました'
    link = url_for('inventory.index', _external=False)
    
    notify_managers(title, message, type='error', link=link)


def notify_inbound_confirmed(order):
    """入庫確定通知
    
    Args:
        order: InboundOrder
    """
    title = '入庫確定'
    message = f'入庫指示 {order.order_number} が確定されました（{order.stock.product_name}: {order.quantity}個）'
    link = url_for('inbound.index', _external=False)
    
    # 倉庫担当者に通知
    warehouse_users = User.query.filter_by(role=UserRole.WAREHOUSE, active=True).all()
    for user in warehouse_users:
        create_notification(user.id, title, message, type='success', link=link)


def notify_outbound_confirmed(order):
    """出庫確定通知
    
    Args:
        order: OutboundOrder
    """
    title = '出庫確定'
    message = f'出庫指示 {order.order_number} が確定されました（{order.stock.product_name}: {order.quantity}個）'
    link = url_for('outbound.index', _external=False)
    
    # 倉庫担当者に通知
    warehouse_users = User.query.filter_by(role=UserRole.WAREHOUSE, active=True).all()
    for user in warehouse_users:
        create_notification(user.id, title, message, type='success', link=link)


# ========================================
# メール通知
# ========================================

def send_email(recipients, subject, body):
    """メール送信
    
    Args:
        recipients: 受信者リスト
        subject: 件名
        body: 本文
    """
    try:
        msg = Message(subject, recipients=recipients)
        msg.body = body
        mail.send(msg)
    except Exception as e:
        # ログに記録
        print(f"メール送信エラー: {e}")


def send_low_stock_email(stock: Stock):
    """在庫不足メール送信
    
    Args:
        stock: 在庫オブジェクト
    """
    # 管理者とマネージャーのメールアドレス取得
    users = User.query.filter(
        User.role.in_([UserRole.ADMIN, UserRole.MANAGER]),
        User.active == True,
        User.email_verified == True
    ).all()
    
    recipients = [user.email for user in users]
    
    if not recipients:
        return
    
    subject = f'【在庫管理】在庫不足アラート - {stock.product_name}'
    body = f'''
在庫不足アラート

以下の商品の在庫が最小在庫数を下回りました。

商品名: {stock.product_name}
商品コード: {stock.product_code or '-'}
現在在庫: {stock.quantity}
最小在庫: {stock.min_stock}
不足数: {stock.min_stock - stock.quantity}

至急、発注をご検討ください。

在庫管理システム
'''
    send_email(recipients, subject, body)


def send_daily_summary():
    """日次サマリーメール送信（定期実行用）"""
    from models import StockHistory, HistoryAction
    from sqlalchemy import func
    
    today = datetime.utcnow().date()
    
    # 今日の入出庫統計
    today_in = StockHistory.query.filter(
        StockHistory.action == HistoryAction.IN,
        func.date(StockHistory.created_at) == today
    ).count()
    
    today_out = StockHistory.query.filter(
        StockHistory.action == HistoryAction.OUT,
        func.date(StockHistory.created_at) == today
    ).count()
    
    # 在庫不足アイテム
    low_stock_items = Stock.query.filter(
        Stock.deleted_at.is_(None),
        Stock.quantity <= Stock.min_stock
    ).count()
    
    # 管理者に送信
    admins = User.query.filter_by(role=UserRole.ADMIN, active=True, email_verified=True).all()
    recipients = [admin.email for admin in admins]
    
    if not recipients:
        return
    
    subject = f'【在庫管理】日次サマリー - {today.strftime("%Y年%m月%d日")}'
    body = f'''
日次サマリー

【{today.strftime("%Y年%m月%d日")}の実績】

入庫件数: {today_in}件
出庫件数: {today_out}件

【現在の状況】

在庫不足アイテム: {low_stock_items}件

詳細は在庫管理システムをご確認ください。

在庫管理システム
'''
    send_email(recipients, subject, body)


def send_weekly_report():
    """週次レポートメール送信（定期実行用）"""
    from datetime import timedelta
    from models import StockHistory, HistoryAction
    from sqlalchemy import func
    
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    # 週間統計
    week_in = db.session.query(func.sum(StockHistory.quantity)).filter(
        StockHistory.action == HistoryAction.IN,
        StockHistory.created_at >= week_ago
    ).scalar() or 0
    
    week_out = db.session.query(func.sum(StockHistory.quantity)).filter(
        StockHistory.action == HistoryAction.OUT,
        StockHistory.created_at >= week_ago
    ).scalar() or 0
    
    # マネージャー以上に送信
    users = User.query.filter(
        User.role.in_([UserRole.ADMIN, UserRole.MANAGER]),
        User.active == True,
        User.email_verified == True
    ).all()
    
    recipients = [user.email for user in users]
    
    if not recipients:
        return
    
    subject = f'【在庫管理】週次レポート'
    body = f'''
週次レポート（過去7日間）

【入出庫実績】

入庫合計: {week_in}個
出庫合計: {week_out}個
差引: {week_in - week_out}個

詳細なレポートは在庫管理システムのレポート機能からご確認ください。

在庫管理システム
'''
    send_email(recipients, subject, body)


# ========================================
# バッチ処理用通知チェック
# ========================================

def check_and_notify_low_stock():
    """在庫不足チェックと通知（定期実行用）
    
    crontabで定期実行:
        0 9 * * * cd /path/to/app && flask check-low-stock
    """
    low_stocks = Stock.query.filter(
        Stock.deleted_at.is_(None),
        Stock.quantity <= Stock.min_stock
    ).all()
    
    for stock in low_stocks:
        notify_low_stock(stock)
    
    return len(low_stocks)


def check_and_notify_expiring():
    """期限切れ間近チェックと通知（定期実行用）
    
    crontabで定期実行:
        0 9 * * * cd /path/to/app && flask check-expiring
    """
    from datetime import timedelta
    
    thirty_days_later = datetime.utcnow() + timedelta(days=30)
    
    expiring = Stock.query.filter(
        Stock.deleted_at.is_(None),
        Stock.expiry_date.isnot(None),
        Stock.expiry_date <= thirty_days_later
    ).all()
    
    for stock in expiring:
        notify_expiring_soon(stock)
    
    return len(expiring)