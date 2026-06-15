import os

from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool


def main():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is not set")

    host = database_url.split("@")[-1].split("/")[0]
    print(f"DATABASE_URL_HOST={host}")

    engine = create_engine(database_url, poolclass=NullPool, pool_pre_ping=True)
    with engine.connect() as connection:
        database = connection.execute(text("select current_database()")).scalar()
        user = connection.execute(text("select current_user")).scalar()
        print(f"DATABASE={database}")
        print(f"USER={user}")

        rows = connection.execute(
            text(
                """
                select table_schema, table_name
                from information_schema.tables
                where table_schema not in ('pg_catalog', 'information_schema')
                order by table_schema, table_name
                """
            )
        ).fetchall()

        print(f"TABLE_COUNT={len(rows)}")
        for schema, table in rows:
            print(f"{schema}.{table}")


if __name__ == "__main__":
    main()
