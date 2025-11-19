# ==========================================
# 在庫管理システム - Dockerfile
# ==========================================

FROM python:3.11-slim

# メタデータ
LABEL maintainer="your-email@example.com"
LABEL description="在庫管理システム"

# 作業ディレクトリ
WORKDIR /app

# システム依存関係のインストール
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# 非rootユーザーを作成
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    mkdir -p /app/logs /app/uploads && \
    chown -R appuser:appuser /app/logs /app/uploads

# ユーザー切り替え
USER appuser

# 環境変数
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# ポート公開
EXPOSE 5000

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# 起動コマンド
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]