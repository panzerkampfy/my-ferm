import models, utils
from core import security
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
                defaults=dict(name="Менеджер", description="Судья соревнований"),
            ),
        ),
        lambda db: (
            models.User,
            dict(
                # first_name=settings.FIRST_ADMIN_USERNAME,
                # middle_name=settings.FIRST_ADMIN_USERNAME,
                # last_name=settings.FIRST_ADMIN_USERNAME,
                # login=settings.FIRST_ADMIN_USERNAME,
                defaults=dict(
                    first_name=settings.FIRST_ADMIN_USERNAME,
                    middle_name=settings.FIRST_ADMIN_USERNAME,
                    last_name=settings.FIRST_ADMIN_USERNAME,
                    login=settings.FIRST_ADMIN_USERNAME,
                    password=settings.FIRST_ADMIN_PASSWORD,
                    role=db.query(models.Role)
                    .filter(models.Role.code == "admin")
                    .first(),
                ),
            ),
        ),
        lambda db: (
            models.GradeType,
            dict(
                judge_role_id=db.query(models.JudgeRole)
                .filter(models.JudgeRole.code == "brigade_master")
                .first()
                .id,
                defaults=dict(
                    name="Оценка председателя бригады",
                    description="-",
                    code="brigade_master_grade",
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
