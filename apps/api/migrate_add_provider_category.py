from sqlalchemy import inspect, text

from database import engine
from i18n import DEFAULT_PROVIDER_CATEGORY_KEY


def migrate() -> None:
    inspector = inspect(engine)
    if "providers" not in inspector.get_table_names():
        raise RuntimeError("The providers table does not exist.")

    provider_columns = {column["name"] for column in inspector.get_columns("providers")}

    with engine.begin() as connection:
        if "category" not in provider_columns:
            connection.execute(text("ALTER TABLE providers ADD COLUMN category VARCHAR"))

        connection.execute(
            text(
                """
                UPDATE providers
                SET category = :default_category
                WHERE category IS NULL OR TRIM(category) = ''
                """
            ),
            {"default_category": DEFAULT_PROVIDER_CATEGORY_KEY},
        )
        connection.execute(text("ALTER TABLE providers ALTER COLUMN category SET NOT NULL"))

    print("providers.category is ready for multilingual category keys.")


if __name__ == "__main__":
    migrate()
