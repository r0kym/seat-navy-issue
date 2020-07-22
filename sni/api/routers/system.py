"""
SNI instance administrative paths
"""

from datetime import datetime
from typing import List, Optional

from apscheduler.job import Job
from fastapi import (APIRouter, Depends, HTTPException, status,)
import pydantic as pdt

from sni.scheduler import scheduler
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)
from sni.uac.clearance import assert_has_clearance
from sni.utils import callable_from_name

router = APIRouter()


class GetJobOut(pdt.BaseModel):
    """
    Represents a job
    """
    coalesce: bool
    executor: str
    function: str
    job_id: str
    max_instances: Optional[int]
    misfire_grace_time: Optional[int]
    name: str
    next_run_time: Optional[datetime]
    trigger: Optional[str]

    @staticmethod
    def from_job(job: Job) -> 'GetJobOut':
        """
        Converts a :class:`apscheduler.job.Job` to a
        :class:`sni.api.routers.system.GetJobOut`.
        """
        function = job.func.__name__ if callable(job.func) else str(job.func)
        return GetJobOut(
            coalesce=job.coalesce,
            executor=job.executor,
            function=function,
            job_id=job.id,
            max_instances=job.max_instances,
            misfire_grace_time=job.misfire_grace_time,
            name=job.name,
            next_run_time=job.next_run_time,
            trigger=str(job.trigger),
        )


@router.get(
    '/job',
    response_model=List[GetJobOut],
    summary='Gets the currently scheduled job list',
)
def get_jobs(tkn: Token = Depends(from_authotization_header_nondyn)):
    """
    Gets the currently scheduled job list. Requires a clearance level of 10.
    """
    assert_has_clearance(tkn.owner, 'sni.system.read_jobs')
    return [GetJobOut.from_job(job) for job in scheduler.get_jobs()]


@router.post(
    '/job/{callable_name}',
    response_model=GetJobOut,
    summary='Submits a job to the scheduler',
)
def post_job(
        callable_name: str,
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Submits a job to the scheduler. Requires a clearance level of 10.
    """
    assert_has_clearance(tkn.owner, 'sni.system.submit_job')
    try:
        function = callable_from_name(callable_name)
        job = scheduler.add_job(function)
        return GetJobOut.from_job(job)
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
