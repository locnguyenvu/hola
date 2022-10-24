import re
from datetime import datetime

from app.di import get_db

db = get_db()

class Log(db.Model):

    __tablename__ = "income_log"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    subject = db.Column("subject", db.String, nullable=False)
    amount = db.Column("amount", db.Numeric(10,2), nullable=False)
    created_at = db.Column("created_at", db.DateTime, server_default="NOW()")
    updated_at = db.Column("updated_at", db.DateTime)

    def set_amount_by_string(self, amount:str):
        carry = 0
        for i in range(len(amount)):
            if amount[i].isnumeric():
                carry = carry * 10
                carry = carry + int(amount[i])

        # multiply with decimal prefix
        if amount[-1].isalpha():
            decimal_prefix = amount[-1]
            if decimal_prefix == "k":
                carry = carry * 1000
            elif decimal_prefix == "M":
                carry = carry * 1000*1000
            elif decimal_prefix == "G":
                carry = carry * 1000*1000*1000

        self.amount = carry

    @classmethod
    def from_plain_str(cls, content: str):
        msg_chunks = content.split(" ")
        amount = msg_chunks[-1]
        if not re.search(r"^\d+(k)*$", amount):
            raise ValueError("Invalid chat message, spending amount not found")

        il = cls()
        il.subject = " ".join(msg_chunks[:len(msg_chunks)-1])
        il.set_amount_by_string(amount)
        il.created_at = datetime.now()
        return il


def save(model: Log):
    if not model.created_at:
        model.created_at = datetime.now()
    if not model.updated_at:
        model.updated_at = datetime.now()

    db.session.add(model)
    db.session.commit()