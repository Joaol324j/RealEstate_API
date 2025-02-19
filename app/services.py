import database as _database
import models as _models

def _add_tables():
    try:
        _database.Base.metadata.create_all(bind=_database.engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise