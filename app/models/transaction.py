from datetime import datetime, UTC

from ..extensions import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    pred_category = db.Column(db.String(100), nullable=False)
    user_category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "amount": str(self.amount),
            "pred_category": self.pred_category,
            "user_category": self.user_category,
            "created_at": self.created_at.isoformat(),
        }
