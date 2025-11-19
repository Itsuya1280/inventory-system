"""
在庫管理システム - カスタムデコレータ
utils/decorators.py
"""
from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

from models import UserRole


def role_required(role):
    """ロール必須デコレータ
    
    使用例:
        @bp.route('/admin')
        @role_required(UserRole.ADMIN)
        def admin_page():
            return 'Admin only'
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('ログインが必要です', 'error')
                return redirect(url_for('auth.login'))
            
            if not current_user.has_permission(role):
                flash('この機能を使用する権限がありません', 'error')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """管理者必須デコレータ
    
    使用例:
        @bp.route('/admin/users')
        @admin_required
        def manage_users():
            return 'Admin users'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('ログインが必要です', 'error')
            return redirect(url_for('auth.login'))
        
        if current_user.role != UserRole.ADMIN:
            flash('管理者権限が必要です', 'error')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def manager_required(f):
    """マネージャー以上必須デコレータ"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('ログインが必要です', 'error')
            return redirect(url_for('auth.login'))
        
        if not current_user.has_permission(UserRole.MANAGER):
            flash('マネージャー権限が必要です', 'error')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def active_user_required(f):
    """アクティブユーザー必須デコレータ"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('ログインが必要です', 'error')
            return redirect(url_for('auth.login'))
        
        if not current_user.active:
            flash('アカウントが無効化されています', 'error')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def email_verified_required(f):
    """メール認証必須デコレータ"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('ログインが必要です', 'error')
            return redirect(url_for('auth.login'))
        
        if not current_user.email_verified:
            flash('メールアドレスの認証が必要です', 'warning')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function


def permission_required(*permissions):
    """複数権限チェックデコレータ
    
    使用例:
        @permission_required('edit_stock', 'view_reports')
        def advanced_feature():
            return 'Advanced feature'
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('ログインが必要です', 'error')
                return redirect(url_for('auth.login'))
            
            # TODO: 権限チェックロジックを実装
            # for permission in permissions:
            #     if not current_user.has_permission(permission):
            #         abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator