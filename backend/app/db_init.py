from app.core.database import create_db_and_tables
# Import models to register them with metadata
from app import models

# Allow the user to run this module to init DB
if __name__ == "__main__":
    create_db_and_tables()
    print("Database initialized!")
