from app import create_app
from database.db import db


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Supabase schema is ready.")


if __name__ == "__main__":
    main()
