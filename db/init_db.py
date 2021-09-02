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
                name="admin", description="Роль администратора"
                # defaults=dict(name="admin", description="Роль администратора"),
            ),
        ),
        lambda db: (
            models.Role,
            dict(
                name="manager", description="Роль менеджера"
                # defaults=dict(name="manager", description="Роль менеджера"),
            ),
        ),
        lambda db: (
            models.Role,
            dict(
                name="worker", description="Позиция работника"
                # defaults=dict(name="worker", description="Позиция работника"),
            ),
        ),
        lambda db: (
            models.User,
            dict(
                password=settings.FIRST_ADMIN_PASSWORD,
                role_id=db.query(models.Role).filter(models.Role.name == "admin").first().id,
                defaults=dict(
                    first_name=settings.FIRST_ADMIN_USERNAME,
                    middle_name=settings.FIRST_ADMIN_USERNAME,
                    last_name=settings.FIRST_ADMIN_USERNAME,
                    login=settings.FIRST_ADMIN_USERNAME,
                ),
            ),
        ),
        lambda db: (
            models.User,
            dict(
                password=settings.FIRST_MANAGER_PASSWORD,
                role_id=db.query(models.Role).filter(models.Role.name == "manager").first().id,
                defaults=dict(
                    first_name=settings.FIRST_MANAGER_USERNAME,
                    middle_name=settings.FIRST_MANAGER_USERNAME,
                    last_name=settings.FIRST_MANAGER_USERNAME,
                    login=settings.FIRST_MANAGER_USERNAME,
                ),
            ),
        ),
        lambda db: (
            models.User,
            dict(
                password="worker",
                role_id=db.query(models.Role).filter(models.Role.name == "worker").first().id,
                defaults=dict(
                    first_name="worker",
                    middle_name="worker",
                    last_name="worker",
                    login="worker",
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
