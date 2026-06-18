from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.db.base import get_db
from app.models.staff import DigitalStaff
from app.schemas.staff import StaffCreate, StaffUpdate, StaffListResponse, StaffInDB
from app.api.v1.endpoints.admin import get_current_admin

router = APIRouter()


@router.get("/list", response_model=StaffListResponse, summary="员工分页列表")
def staff_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    status: Optional[str] = Query(None, description="状态筛选"),
    db: Session = Depends(get_db)
):
    """分页查询数字员工列表，支持关键词搜索和状态筛选"""
    query = db.query(DigitalStaff)

    if keyword:
        query = query.filter(
            (DigitalStaff.name.contains(keyword)) |
            (DigitalStaff.role.contains(keyword)) |
            (DigitalStaff.tag.contains(keyword))
        )

    if status:
        query = query.filter(DigitalStaff.status == status)

    total = query.count()
    items = query.order_by(DigitalStaff.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return StaffListResponse(
        code=200,
        message="success",
        data={
            "items": [StaffInDB.model_validate(item).model_dump(mode='json') for item in items],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    )


@router.get("/stats", response_model=StaffListResponse, summary="员工统计数据")
def staff_stats(
    db: Session = Depends(get_db)
):
    """返回员工统计信息，用于仪表盘"""
    total = db.query(func.count(DigitalStaff.id)).scalar()
    active = db.query(func.count(DigitalStaff.id)).filter(DigitalStaff.is_active == True).scalar()
    busy = db.query(func.count(DigitalStaff.id)).filter(DigitalStaff.status == "处理中").scalar()

    return StaffListResponse(
        code=200,
        message="success",
        data={
            "total": total,
            "active": active,
            "busy": busy
        }
    )


@router.post("/create", response_model=StaffListResponse, summary="创建员工")
def staff_create(
    data: StaffCreate,
    db: Session = Depends(get_db)
):
    staff = DigitalStaff(**data.model_dump())
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return StaffListResponse(code=200, message="创建成功", data=StaffInDB.model_validate(staff).model_dump(mode='json'))


@router.put("/update/{staff_id}", response_model=StaffListResponse, summary="更新员工")
def staff_update(
    staff_id: int,
    data: StaffUpdate,
    db: Session = Depends(get_db)
):
    staff = db.query(DigitalStaff).filter(DigitalStaff.id == staff_id).first()
    if not staff:
        return StaffListResponse(code=404, message="员工不存在")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(staff, key, value)

    db.commit()
    db.refresh(staff)
    return StaffListResponse(code=200, message="更新成功", data=StaffInDB.model_validate(staff).model_dump(mode='json'))


@router.delete("/delete/{staff_id}", response_model=StaffListResponse, summary="删除员工")
def staff_delete(
    staff_id: int,
    db: Session = Depends(get_db)
):
    staff = db.query(DigitalStaff).filter(DigitalStaff.id == staff_id).first()
    if not staff:
        return StaffListResponse(code=404, message="员工不存在")

    db.delete(staff)
    db.commit()
    return StaffListResponse(code=200, message="删除成功")
