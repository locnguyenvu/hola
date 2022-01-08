import re
from datetime import datetime
from sqlalchemy import and_

from app.di import get_db
import app.spending.log as spending_log
import app.spending.category as spending_category

db = get_db()

class SpendingLogCategory(db.Model):

    __tablename__ = "recommendation_spending_log_category"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    hits = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def increase_hit(self):
        if self.hits is None:
            self.hits = 0
        self.hits = self.hits + 1

    def decrease_hit(self):
        if self.hits is None:
            self.hits = 0
        elif self.hits > 0:
            self.hits = self.hits - 1

        

def first_or_new(word:str, position, category_id:int) -> SpendingLogCategory:
    record = SpendingLogCategory.query.filter(and_(
        SpendingLogCategory.word == word,
        SpendingLogCategory.position == position,
        SpendingLogCategory.category_id == category_id
    )).first()
    if record is None:
        return SpendingLogCategory(
            word=word,
            position=position,
            category_id=category_id,
            created_at=datetime.now()
        )
    return record

def delete(model: SpendingLogCategory):
    db.session.delete(model)
    db.session.commit()

def save(model: SpendingLogCategory):
    db.session.add(model)
    db.session.commit()

def tokenize(slog: spending_log.Log):
    worlds = slog.subject.split(" ")
    
    for idx, w in enumerate(worlds):
        if re.search(r"^\d+$", w) is not None:
            continue

        node = first_or_new(w, idx, slog.spending_category_id)
        node.increase_hit()
        node.save()

def detokenize(slog: spending_log.Log):
    worlds = slog.subject.split(" ")
    
    for idx, w in enumerate(worlds):
        if re.search(r"^\d+$", w) is not None:
            continue

        node = first_or_new(w, idx, slog.spending_category_id)
        if node.id is None:
            continue

        node.decrease_hit()
        if node.hits > 0:
            save(node)
        else:
            delete(node)

def list_categories(subject: str) -> list:
    worlds = subject.split(" ")

    categories_id = {}

    for idx, w in enumerate(worlds):
        if re.search(r"^\d+$", w) is not None:
            continue
        
        matched = SpendingLogCategory.query.filter(and_(
            SpendingLogCategory.word == w,
            SpendingLogCategory.position == idx
        )).all()

        if len(matched) == 0:
            continue

        for m in matched:
            if m not in categories_id:
                categories_id[m.category_id] = 0
            categories_id[m.category_id] = categories_id[m.category_id] + m.hits

    if bool(categories_id) == False:
        return spending_category.list_all()

    categories = spending_category.Category.query.filter(spending_category.Category.id.in_(categories_id.keys())).all()
    categories_id_order_by_hits = {k: v for k, v in sorted(categories_id.items(), key=lambda item: item[1], reverse=False)}
    
    output = []

    for cat_id in categories_id_order_by_hits.keys():
        for cat in categories:
            if cat.id != cat_id:
                continue
            output.append(cat)

    return output
    
def remove_context(subject: str, category_id: int) -> bool:
    worlds = subject.split(" ")
    found_words = []

    for idx, w in enumerate(worlds):
        if re.search(r"^\d+$", w) is not None:
            continue
    
        matched = SpendingLogCategory.query.filter(and_(
            SpendingLogCategory.word == w,
            SpendingLogCategory.position == idx,
            SpendingLogCategory.category_id == category_id
        )).first()
        if matched is None:
            continue
        found_words.append(matched)

    for w in found_words:
        delete(w)
    return True 
