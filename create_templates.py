import os

# テンプレートディレクトリ作成
os.makedirs('templates/inventory', exist_ok=True)
os.makedirs('templates/inbound', exist_ok=True)
os.makedirs('templates/outbound', exist_ok=True)
os.makedirs('templates/warehouse', exist_ok=True)
os.makedirs('templates/history', exist_ok=True)
os.makedirs('templates/item_master', exist_ok=True)
os.makedirs('templates/errors', exist_ok=True)

# inventory/index.html
with open('templates/inventory/index.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "layout.html" %}
{% block title %}在庫管理{% endblock %}
{% block content %}
<h1>在庫管理</h1>
<a href="{{ url_for('inventory.create') }}" style="display: inline-block; padding: 0.75rem 1.5rem; background: #3498db; color: white; text-decoration: none; border-radius: 4px; margin-bottom: 1rem;">新規追加</a>
<table style="width: 100%; border-collapse: collapse; margin-top: 1rem;">
    <thead>
        <tr style="background-color: #34495e; color: white;">
            <th style="padding: 1rem; text-align: left;">商品名</th>
            <th style="padding: 1rem; text-align: center;">在庫数</th>
            <th style="padding: 1rem; text-align: center;">操作</th>
        </tr>
    </thead>
    <tbody>
        {% if stocks %}
            {% for stock in stocks %}
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 1rem;">{{ stock.product_name }}</td>
                <td style="padding: 1rem; text-align: center;">{{ stock.quantity }}</td>
                <td style="padding: 1rem; text-align: center;"><a href="{{ url_for('inventory.view', stock_id=stock.id) }}">詳細</a></td>
            </tr>
            {% endfor %}
        {% else %}
        <tr><td colspan="3" style="padding: 2rem; text-align: center;">在庫がありません</td></tr>
        {% endif %}
    </tbody>
</table>
{% endblock %}''')

# inbound/index.html
with open('templates/inbound/index.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "layout.html" %}
{% block title %}入庫管理{% endblock %}
{% block content %}
<h1>入庫管理</h1>
<a href="{{ url_for('inbound.create') }}" style="display: inline-block; padding: 0.75rem 1.5rem; background: #27ae60; color: white; text-decoration: none; border-radius: 4px; margin-bottom: 1rem;">入庫を追加</a>
<p>入庫管理ページ</p>
{% endblock %}''')

# outbound/index.html
with open('templates/outbound/index.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "layout.html" %}
{% block title %}出庫管理{% endblock %}
{% block content %}
<h1>出庫管理</h1>
<a href="{{ url_for('outbound.create') }}" style="display: inline-block; padding: 0.75rem 1.5rem; background: #e74c3c; color: white; text-decoration: none; border-radius: 4px; margin-bottom: 1rem;">出庫を追加</a>
<p>出庫管理ページ</p>
{% endblock %}''')

# warehouse/index.html
with open('templates/warehouse/index.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "layout.html" %}
{% block title %}倉庫確認{% endblock %}
{% block content %}
<h1>倉庫確認</h1>
<p>倉庫確認ページ</p>
{% endblock %}''')

# history/index.html
with open('templates/history/index.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "layout.html" %}
{% block title %}履歴{% endblock %}
{% block content %}
<h1>在庫変動履歴</h1>
<p>履歴ページ</p>
{% endblock %}''')

# item_master/index.html
with open('templates/item_master/index.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "layout.html" %}
{% block title %}品名マスタ{% endblock %}
{% block content %}
<h1>品名マスタ</h1>
<a href="{{ url_for('item_master.new_group') }}" style="display: inline-block; padding: 0.75rem 1.5rem; background: #1abc9c; color: white; text-decoration: none; border-radius: 4px; margin-bottom: 1rem;">グループ追加</a>
<p>品名マスタ管理ページ</p>
{% endblock %}''')

# errors/404.html
with open('templates/errors/404.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "layout.html" %}
{% block title %}ページが見つかりません{% endblock %}
{% block content %}
<h1>404 - ページが見つかりません</h1>
<p>申し訳ありません。お探しのページは見つかりませんでした。</p>
<a href="{{ url_for('index') }}">ホームに戻る</a>
{% endblock %}''')

# errors/500.html
with open('templates/errors/500.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "layout.html" %}
{% block title %}エラー{% endblock %}
{% block content %}
<h1>500 - サーバーエラー</h1>
<p>申し訳ありません。エラーが発生しました。</p>
<a href="{{ url_for('index') }}">ホームに戻る</a>
{% endblock %}''')

print('✅ すべてのテンプレートを作成しました')