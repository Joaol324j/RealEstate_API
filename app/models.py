import datetime as _dt
import sqlalchemy as _sql
import database as _database

class User(_database.Base):
    __tablename__ = "user"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    nome = _sql.Column(_sql.String, index=True)
    sobrenome = _sql.Column(_sql.String, index=True)
    email = _sql.Column(_sql.String, index=True, unique=True)
    numero_telefone = _sql.Column(_sql.String, index=True, unique=True)
    criado_data = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)