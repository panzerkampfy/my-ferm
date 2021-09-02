from typing import List

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import Job, JobType
from schemas import JobCreate, JobTypeCreate


class CRUDJob(CRUDBase[Job, JobCreate, None]):
    async def get_list_by_user(
            self, db: Session, *, user: int
    ) -> List[Job]:
        return db.query(self.model).filter(Job.user_id == user).all()


job = CRUDJob(Job)


class CRUDJobType(CRUDBase[JobType, JobTypeCreate, None]):
    pass


job_type = CRUDJobType(JobType)
