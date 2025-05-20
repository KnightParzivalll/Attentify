from typing import List, OrderedDict

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import (
    Student,
    Teacher,
)
from app.auth import get_current_active_student, get_current_active_teacher
from app.schemas.schedule import DayLessonResponse, WeekLessonResponse
from app.services.schedule import ScheduleService
from app.utils.date_utils import get_current_date, parse_date
from app.utils.validate import validate_week_type

teacher_router = APIRouter(prefix="/teacher/schedule", tags=["schedule"])
student_router = APIRouter(prefix="/student/schedule", tags=["schedule"])


@teacher_router.get("/day", response_model=List[DayLessonResponse])
async def get_day_schedule(
    target_date: str = Query(
        ..., description="Date in YYYY-MM-DD format", example="2024-03-15"
    ),
    only_for_me: bool = False,  # TODO set to true in prod
    teacher: Teacher = Depends(get_current_active_teacher),
    db: AsyncSession = Depends(get_db),
):
    """
    Get daily schedule for a teacher with optional filtering for current user only

    - **target_date**: Date in YYYY-MM-DD format
    - **only_for_me**: Show only lessons assigned to current teacher
    """
    try:
        parsed_date = parse_date(target_date)
        schedule_service = ScheduleService(db)
        term = await schedule_service.get_active_term(parsed_date)

        if not term:
            raise HTTPException(status_code=404, detail="No active term found")

        schedules = await schedule_service.get_teacher_daily_schedules(
            term.id, parsed_date, teacher.id if only_for_me else None
        )

        for i in schedules:
            for j in i.schedule_groups:
                print(j.group)

        return [
            schedule_service.map_to_lesson_response(schedule) for schedule in schedules
        ]

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@student_router.get("/day", response_model=List[DayLessonResponse])
async def get_student_day_schedule(
    target_date: str = Query(
        ..., description="Date in YYYY-MM-DD format", example="2024-03-15"
    ),
    student: Student = Depends(get_current_active_student),
    db: AsyncSession = Depends(get_db),
):
    """
    Get daily schedule for a teacher with optional filtering for current user only

    - **target_date**: Date in YYYY-MM-DD format
    - **only_for_me**: Show only lessons assigned to current teacher
    """
    try:
        parsed_date = parse_date(target_date)
        schedule_service = ScheduleService(db)
        term = await schedule_service.get_active_term(parsed_date)

        if not term:
            raise HTTPException(status_code=404, detail="No active term found")

        schedules = await schedule_service.get_student_daily_schedules(
            term.id, parsed_date, student.id
        )

        for i in schedules:
            for j in i.schedule_groups:
                print(j.group)

        return [
            schedule_service.map_to_lesson_response(schedule) for schedule in schedules
        ]

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@teacher_router.get("/week", response_model=OrderedDict[str, List[WeekLessonResponse]])
async def get_teacher_weekly_schedule(
    week_type: str = Query(..., description="Week type (upper/bottom)"),
    group_ids: List[int] = Query([], description="Filter by group IDs"),
    teacher: Teacher = Depends(get_current_active_teacher),
    only_for_me: bool = False,  # TODO set to true in prod
    db: AsyncSession = Depends(get_db),
):
    """
    Get weekly schedule for authenticated teacher

    - Returns lessons for current active term
    - Filters by week type (upper/bottom)
    - Optionally filters by group IDs
    """
    try:
        current_date = get_current_date()
        schedule_service = ScheduleService(db)

        # Get active term
        term = await schedule_service.get_active_term(current_date)

        if not term:
            raise HTTPException(status_code=404, detail="No active term found")

        # Validate week type
        validate_week_type(week_type)

        # Get filtered schedules
        schedules = await schedule_service.get_teacher_weekly_schedules(
            term_id=term.id,
            week_type=week_type,
            teacher_id=teacher.id if only_for_me else None,
            group_ids=group_ids if group_ids else None,
        )

        # Build ordered weekly structure
        return await schedule_service.build_weekly_structure(schedules)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@student_router.get("/week", response_model=OrderedDict[str, List[WeekLessonResponse]])
async def get_student_weekly_schedule(
    week_type: str = Query(..., description="Week type (upper/bottom)"),
    student: Student = Depends(get_current_active_student),
    db: AsyncSession = Depends(get_db),
):
    """
    Get weekly schedule for authenticated teacher

    - Returns lessons for current active term
    - Filters by week type (upper/bottom)
    - Optionally filters by group IDs
    """
    try:
        current_date = get_current_date()
        schedule_service = ScheduleService(db)

        # Get active term
        term = await schedule_service.get_active_term(current_date)

        if not term:
            raise HTTPException(status_code=404, detail="No active term found")

        # Validate week type
        validate_week_type(week_type)

        # Get filtered schedules
        schedules = await schedule_service.get_student_weekly_schedules(
            term_id=term.id,
            week_type=week_type,
            student_id=student.id,
        )

        # Build ordered weekly structure
        return await schedule_service.build_weekly_structure(schedules)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
