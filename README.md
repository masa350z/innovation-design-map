# Innovation Design Map

**Innovation Design Map** は、単語と単語間の関係を **PostgreSQL** データベースで管理し、  
**OpenAI API** を通じてアイデアを拡張し、**Streamlit** を利用して可視化するツールです。

---

## 特長

- **データベース永続化**  
  単語と単語間の関係を PostgreSQL で管理します。  
- **CLI 操作**  
  `docker compose exec app bash` でコンテナ内に入り、コマンド (`python -m innovation_design_map ...`) を実行することで単語や関係を追加・削除でき、DB スキーマ初期化や OpenAI 提案も行えます。  
- **OpenAI 提案**  
  既存の関係リストを OpenAI（ChatCompletion）に投げ、新しい単語間の関係を生成させることが可能です。  
- **可視化**  
  `streamlit` でネットワークグラフを描画し、ブラウザから確認できます。色分けやノードレイアウトも設定可能。  
- **bind mount**  
  ホストのプロジェクトディレクトリをコンテナにマウントするため、ソースを編集してすぐ反映でき、開発しやすい構成となっています。

---

## ディレクトリ構成

```plaintext
innovation_design_map/
 ┣━ .env
 ┣━ docker-compose.yml
 ┣━ Dockerfile.app
 ┣━ Dockerfile.db
 ┣━ requirements.txt
 ┣━ innovation_design_map/
 │   ┣━ __init__.py
 │   ┣━ cli.py
 │   ┣━ database.py
 │   ┣━ manager.py
 │   ┣━ openai_service.py
 │   ┣━ viewer.py
 │   ┗━ viewer_app.py
.env : OpenAI の API キー (OPENAI_API_KEY=sk-xxxx) を記載
docker-compose.yml : DB コンテナ (PostgreSQL) と アプリケーション コンテナを定義
Dockerfile.app : Python/Streamlit 用のコンテナイメージをビルド
Dockerfile.db : PostgreSQL 用コンテナイメージをビルド
requirements.txt : Python ライブラリ依存
innovation_design_map/ : アプリケーション本体 (CLI や DB モジュール、可視化、OpenAI 機能など)
```

---

## セットアップ

### 1. .env を作成

```bash
echo "OPENAI_API_KEY=sk-xxxxxxx" > .env
```

実際のキーを設定し、.gitignore に .env を追加して秘匿してください。

### 2. Docker イメージのビルドと起動

```bash
docker compose build --no-cache
docker compose up -d
```

`-d` はデタッチドモード。外すとフォアグラウンドでログを見られます。

### 3. テーブル初期化

初回のみ以下を実行し、DB に words・relations テーブルを作成します。

```bash
docker compose exec app bash
python -m innovation_design_map init
```

---

## 使い方 (CLI)

コンテナ内に入り、CLI コマンドを使います。

```bash
docker compose exec app bash
```

### 1. 単語を追加

```bash
python -m innovation_design_map add-word "AI" --attr 1
```

同じ単語が存在する場合は属性を更新します。

### 2. 関係を追加

```bash
python -m innovation_design_map add-relation "AI" "自然言語処理"
```

単語がなければ自動で追加。

### 3. 単語削除

```bash
python -m innovation_design_map delete-word "AI"
```

関連する関係も削除されます。

### 4. OpenAI 提案

```bash
python -m innovation_design_map propose --count 5
```

既存の関係リストを基に、5 個以上の新たな関係を生成し、DB に反映します。  
(.env 内の OPENAI_API_KEY が必要)

### 5. Streamlit ビューア

```bash
python -m innovation_design_map viewer
```

コンテナ内から実行すると、Streamlit がポート 8501 を使って起動し、  
ブラウザで http://localhost:8501 にアクセスするとネットワークグラフを確認できます。

---

## ソース編集 (Bind Mount)

- `./:/app` でホストのファイルをコンテナへマウントしているため、ホスト上の `innovation_design_map/` 以下を編集すると、  
コンテナ内でもすぐに変更が反映されます。Streamlit アプリは「Refresh Data」ボタンや「Rerun」で更新できます。

---

## PostgreSQL データ管理

- **ボリューム** : `db_data` が PostgreSQL のデータを永続化
- **データリセット** :

```bash
docker compose down --volumes
```

これで `db_data` が削除され、DB が空に戻ります。

---

## トラブルシューティング

- **テーブルが存在しないエラー** : `relation "words" does not exist` など  
  → `python -m innovation_design_map init` を実行していない可能性があります。DB 初期化が必要です。
- **OpenAI API 関連エラー** :  
  → `.env` に `OPENAI_API_KEY` が空、またはキーが無効になっている可能性があります。
- **起動失敗** :  
  → `docker compose logs app` / `docker compose logs db` でエラーの詳細を確認し、ライブラリや環境変数を修正してください。
- **bind mount が反映されない** :  
  → ディレクトリ構成が `docker-compose.yml` の場所と異なっている可能性があります。正しく `./:/app` されているか確認してください。

---

## ライセンス

本プロジェクトを使用・改変する場合は、必要に応じてライセンスファイルを追加してください。  
秘匿情報（API キーなど）は `.env` に記載し、リポジトリに含めないようにご注意ください。

