import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Relation(Base):
    __tablename__ = "relations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    from_word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    to_word_id = Column(Integer, ForeignKey("words.id"), nullable=False)

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, unique=True, nullable=False)
    attribute = Column(String, nullable=True)

    from_relations = relationship(
        "Relation",
        foreign_keys=[Relation.from_word_id],
        backref="from_word",
        cascade="all, delete-orphan"
    )
    to_relations = relationship(
        "Relation",
        foreign_keys=[Relation.to_word_id],
        backref="to_word",
        cascade="all, delete-orphan"
    )

def get_engine():
    """
    PostgreSQL を優先し、環境変数 DATABASE_URL なければ SQLite を使う
    """
    db_url = os.environ.get("DATABASE_URL", "sqlite:///innovation_design_map.db")
    return create_engine(db_url, echo=False)

def init_db():
    """
    テーブル作成(既に存在すれば何もしない)
    """
    engine = get_engine()
    Base.metadata.create_all(engine)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
