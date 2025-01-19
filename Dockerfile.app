# Dockerfile.app

FROM python:3.9-slim

# 必要なライブラリを入れる (GCC, libpq-dev 等)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# requirements.txt だけコピーし先にライブラリをインストール
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 環境変数
ENV PYTHONUNBUFFERED=1

EXPOSE 8501

# CMD: Python の CLI で viewer をデフォルト起動 (任意変更可)
CMD ["python", "-m", "innovation_design_map", "viewer"]
