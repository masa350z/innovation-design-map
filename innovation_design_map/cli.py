import click
import os
import sys
import subprocess

from innovation_design_map.database import init_db, get_session
from innovation_design_map.manager import WordManager
from innovation_design_map.openai_service import OpenAIService


@click.group()
def cli():
    pass

@cli.command()
def init():
    """
    DBの初期化(テーブル作成)
    """
    init_db()
    click.echo("Database initialized.")

@cli.command()
@click.argument("text")
@click.option("--attr", default="")
def add_word(text, attr):
    """
    単語を追加/更新
    """
    session = get_session()
    manager = WordManager(session)
    w = manager.add_word(text, attr)
    click.echo(f"Word added or updated: {w.text} (attr={w.attribute})")

@cli.command()
@click.argument("text1")
@click.argument("text2")
def add_relation(text1, text2):
    """
    2単語間の関係を追加
    """
    session = get_session()
    manager = WordManager(session)
    manager.add_relation(text1, text2)
    click.echo(f"Relation added: {text1} -> {text2}")

@cli.command()
@click.argument("text")
def delete_word(text):
    """
    単語を削除(関連する関係も削除)
    """
    session = get_session()
    manager = WordManager(session)
    manager.delete_word(text)
    click.echo(f"Deleted word: {text}")

@cli.command()
def viewer():
    """
    Streamlit のビューアを起動
    """
    # 外部コマンドとして実行
    subprocess.run(["streamlit", "run", "innovation_design_map/viewer_app.py"])

@cli.command()
@click.option("--count", default=5)
def propose(count):
    """
    OpenAI に問い合わせて新しい関係を提案
    """
    session = get_session()
    manager = WordManager(session)
    existing_relations = manager.get_all_relations()

    pairs = []
    for r in existing_relations:
        w1 = session.get(manager.Word, r.from_word_id)
        w2 = session.get(manager.Word, r.to_word_id)
        if w1 and w2:
            pairs.append((w1.text, w2.text))

    key = os.environ.get("OPENAI_API_KEY", "")
    service = OpenAIService(api_key=key)
    new_rel = service.propose_relations(pairs, minimum_count=count)
    for (a, b) in new_rel:
        manager.add_relation(a, b)
    click.echo(f"Added new relations: {new_rel}")
