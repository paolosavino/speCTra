from sqlmodel import Session, select
from app.core.database import engine
from app.models.api_key import ApiKey
import sys
import secrets

def create_key(name: str = "Admin Key"):
    # Generate a secure random key
    key_value = f"sk-spectra-{secrets.token_urlsafe(16)}"
    
    with Session(engine) as session:
        # Unlikely to collide, but good practice
        existing = session.exec(select(ApiKey).where(ApiKey.key_hash == key_value)).first()
        if existing:
            print(f"Key collision occurred. Try again.")
            return

        new_key = ApiKey(key_hash=key_value, name=name)
        session.add(new_key)
        session.commit()
        session.refresh(new_key)
        print(f"SUCCESS! Created API Key: {new_key.key_hash}")
        print(f"Name: {new_key.name}")
        print(f"ID: {new_key.id}")

if __name__ == "__main__":
    key_name = sys.argv[1] if len(sys.argv) > 1 else "CLI Generated Key"
    create_key(name=key_name)
