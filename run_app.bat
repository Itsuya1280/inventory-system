@echo off
chcp 65001 > nul
cd /d %~dp0

echo ========================================
echo   在庫管理システムを起動しています...
echo ========================================
echo.

if not exist venv (
    echo 仮想環境がありません。作成します...
    python -m venv venv
    echo.
)

echo 仮想環境を有効化しています...
call venv\Scripts\activate.bat
echo.

echo 必要なパッケージをインストール中...
pip install -q -r requirements.txt
echo.

echo ========================================
echo   アプリケーションを起動します
echo ========================================
echo.
echo ブラウザで以下にアクセスしてください:
echo http://localhost:5000
echo.
echo ログイン情報:
echo Email: admin@example.com
echo Password: Admin@12345
echo.
echo アプリを停止するには、このウィンドウを閉じるか Ctrl+C を押してください
echo ========================================
echo.

python app.py

pause