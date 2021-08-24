import models
import utils
from core.config import settings
from db.session import SessionLocal
from sqlalchemy.orm import Session


def init_db(db: Session) -> None:
    entities = [
        lambda db: (
            models.Role,
            dict(
                defaults=dict(name="Администратор", description="Роль администратора"),
            ),
        ),
        lambda db: (
            models.Role,
            dict(
                defaults=dict(name="Менеджер", description="Позиция менеджера"),
            ),
        ),
        lambda db: (
            models.Role,
            dict(
               defaults=dict(name="Работник", description="Позиция работника"),
            ),
        ),
        lambda db: (
            models.User,
            dict(
                password=settings.FIRST_ADMIN_PASSWORD,
                role_id=1,
                defaults=dict(
                    first_name=settings.FIRST_ADMIN_USERNAME,
                    middle_name=settings.FIRST_ADMIN_USERNAME,
                    last_name=settings.FIRST_ADMIN_USERNAME,
                    login=settings.FIRST_ADMIN_USERNAME,
                ),
            ),
        ),
    ]

    for callback in entities:
        model, params = callback(db)
        utils.get_or_create(db, model, **params)
        db.flush()

    db.commit()


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    init()


if __name__ == "__main__":
    main()
