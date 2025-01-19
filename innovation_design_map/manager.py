from sqlalchemy.orm import Session
from innovation_design_map.database import Word, Relation
from typing import List

class WordManager:
    def __init__(self, session: Session):
        self.session = session
        self.Word = Word
        self.Relation = Relation

    def add_word(self, text: str, attribute: str = "") -> Word:
        existing = self.session.query(self.Word).filter_by(text=text).one_or_none()
        if existing:
            existing.attribute = attribute
            self.session.commit()
            return existing
        new_word = self.Word(text=text, attribute=attribute)
        self.session.add(new_word)
        self.session.commit()
        return new_word

    def add_relation(self, text1: str, text2: str):
        w1 = self.session.query(self.Word).filter_by(text=text1).one_or_none()
        if not w1:
            w1 = self.add_word(text1)
        w2 = self.session.query(self.Word).filter_by(text=text2).one_or_none()
        if not w2:
            w2 = self.add_word(text2)

        # 重複チェック
        already = self.session.query(self.Relation).filter_by(
            from_word_id=w1.id, to_word_id=w2.id
        ).one_or_none()
        if not already:
            rel = self.Relation(from_word_id=w1.id, to_word_id=w2.id)
            self.session.add(rel)
            self.session.commit()

    def delete_word(self, text: str):
        w = self.session.query(self.Word).filter_by(text=text).one_or_none()
        if w:
            self.session.delete(w)
            self.session.commit()

    def get_all_relations(self) -> List[Relation]:
        return self.session.query(self.Relation).all()
