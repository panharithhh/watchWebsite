from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


def getAdminUser(adminId: int, db: Session) -> models.User:
    adminUser = db.query(models.User).filter(models.User.id == adminId).first()
    if not adminUser or adminUser.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return adminUser


@router.get("/watches", response_model=list[schemas.WatchOut])
def listWatches(
    adminId: int,
    status: schemas.WatchStatus | None = None,
    db: Session = Depends(get_db),
):
    getAdminUser(adminId, db)
    query = db.query(models.Watch)
    if status:
        query = query.filter(models.Watch.status == status)
    return query.all()


@router.post("/watches/{watchId}/approve", response_model=schemas.WatchOut)
def approveWatch(
    watchId: int,
    data: schemas.WatchApproval,
    db: Session = Depends(get_db),
):
    adminUser = getAdminUser(data.admin_id, db)
    watch = db.query(models.Watch).filter(models.Watch.id == watchId).first()
    if not watch:
        raise HTTPException(status_code=404, detail="Watch not found")

    watch.status = data.status
    watch.approved_by = adminUser.id
    db.commit()
    db.refresh(watch)
    return watch


@router.post("/watches/{watchId}/deny", response_model=schemas.WatchOut)
def denyWatch(
    watchId: int,
    data: schemas.AdminAction,
    db: Session = Depends(get_db),
):
    adminUser = getAdminUser(data.admin_id, db)
    watch = db.query(models.Watch).filter(models.Watch.id == watchId).first()
    if not watch:
        raise HTTPException(status_code=404, detail="Watch not found")

    watch.status = models.WatchStatus.rejected
    watch.approved_by = adminUser.id
    db.commit()
    db.refresh(watch)
    return watch


@router.patch("/watches/{watchId}", response_model=schemas.WatchOut)
def updateWatch(
    watchId: int,
    data: schemas.AdminWatchUpdate,
    db: Session = Depends(get_db),
):
    getAdminUser(data.admin_id, db)
    watch = db.query(models.Watch).filter(models.Watch.id == watchId).first()
    if not watch:
        raise HTTPException(status_code=404, detail="Watch not found")

    updateData = data.model_dump(exclude={"admin_id"}, exclude_unset=True)
    for key, value in updateData.items():
        setattr(watch, key, value)

    db.commit()
    db.refresh(watch)
    return watch


@router.delete("/watches/{watchId}")
def removeWatch(
    watchId: int,
    adminId: int,
    db: Session = Depends(get_db),
):
    getAdminUser(adminId, db)
    watch = db.query(models.Watch).filter(models.Watch.id == watchId).first()
    if not watch:
        raise HTTPException(status_code=404, detail="Watch not found")

    db.delete(watch)
    db.commit()
    return {"message": "Watch removed"}


@router.get("/sellers", response_model=list[schemas.UserOut])
def listSellers(
    adminId: int,
    db: Session = Depends(get_db),
):
    getAdminUser(adminId, db)
    return db.query(models.User).filter(models.User.role == models.UserRole.seller).all()


@router.post("/sellers/{sellerId}/approve", response_model=schemas.UserOut)
def approveSeller(
    sellerId: int,
    data: schemas.AdminAction,
    db: Session = Depends(get_db),
):
    getAdminUser(data.admin_id, db)
    seller = db.query(models.User).filter(models.User.id == sellerId).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    seller.role = models.UserRole.seller
    db.commit()
    db.refresh(seller)
    return seller


@router.post("/sellers/{sellerId}/disable", response_model=schemas.UserOut)
def disableSeller(
    sellerId: int,
    data: schemas.AdminAction,
    db: Session = Depends(get_db),
):
    getAdminUser(data.admin_id, db)
    seller = db.query(models.User).filter(models.User.id == sellerId).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    seller.role = models.UserRole.buyer
    db.commit()
    db.refresh(seller)
    return seller


@router.patch("/sellers/{sellerId}", response_model=schemas.UserOut)
def updateSeller(
    sellerId: int,
    data: schemas.SellerUpdate,
    db: Session = Depends(get_db),
):
    getAdminUser(data.admin_id, db)
    seller = db.query(models.User).filter(models.User.id == sellerId).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    updateData = data.model_dump(exclude={"admin_id"}, exclude_unset=True)
    for key, value in updateData.items():
        setattr(seller, key, value)

    db.commit()
    db.refresh(seller)
    return seller


@router.delete("/sellers/{sellerId}")
def deleteSeller(
    sellerId: int,
    adminId: int,
    db: Session = Depends(get_db),
):
    getAdminUser(adminId, db)
    seller = db.query(models.User).filter(models.User.id == sellerId).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    db.delete(seller)
    db.commit()
    return {"message": "Seller deleted"}


@router.get("/brands", response_model=list[schemas.BrandOut])
def listBrands(
    adminId: int,
    db: Session = Depends(get_db),
):
    getAdminUser(adminId, db)
    return db.query(models.Brand).all()


@router.post("/brands", response_model=schemas.BrandOut)
def createBrand(
    adminId: int,
    data: schemas.BrandCreate,
    db: Session = Depends(get_db),
):
    getAdminUser(adminId, db)
    brand = models.Brand(name=data.name)
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


@router.patch("/brands/{brandId}", response_model=schemas.BrandOut)
def updateBrand(
    brandId: int,
    adminId: int,
    data: schemas.BrandUpdate,
    db: Session = Depends(get_db),
):
    getAdminUser(adminId, db)
    brand = db.query(models.Brand).filter(models.Brand.id == brandId).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    updateData = data.model_dump(exclude_unset=True)
    for key, value in updateData.items():
        setattr(brand, key, value)

    db.commit()
    db.refresh(brand)
    return brand


@router.delete("/brands/{brandId}")
def deleteBrand(
    brandId: int,
    adminId: int,
    db: Session = Depends(get_db),
):
    getAdminUser(adminId, db)
    brand = db.query(models.Brand).filter(models.Brand.id == brandId).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    db.delete(brand)
    db.commit()
    return {"message": "Brand deleted"}

