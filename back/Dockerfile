# ベースイメージの指定
FROM python:3.10

# 作業ディレクトリを作成
WORKDIR /app

# Poetryをインストール
RUN pip install --upgrade pip && pip install poetry

# 依存関係をインストール
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-dev

# ソースコードをコピー
COPY . .

# アプリケーションの起動
CMD ["poetry", "run", "uvicorn", "back.main:app", "--host", "0.0.0.0", "--port", "8000"]
