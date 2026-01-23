from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


def buildCart(items: list[schemas.OrderItemCreate], db: Session) -> tuple[list[schemas.CartItemOut], Decimal]:
    cartItems: list[schemas.CartItemOut] = []
    totalAmount = Decimal("0")

    for item in items:
        if item.quantity < 1:
            raise HTTPException(status_code=400, detail="Quantity must be at least 1")

        watch = db.query(models.Watch).filter(models.Watch.id == item.watch_id).first()
        if not watch:
            raise HTTPException(status_code=404, detail=f"Watch {item.watch_id} not found")
        if watch.status != models.WatchStatus.approved:
            raise HTTPException(status_code=400, detail=f"Watch {item.watch_id} not approved")

        unitPrice = Decimal(str(watch.price))
        lineTotal = unitPrice * item.quantity
        totalAmount += lineTotal
        cartItems.append(
            schemas.CartItemOut(
                watch_id=item.watch_id,
                quantity=item.quantity,
                unit_price=unitPrice,
                line_total=lineTotal,
            )
        )

    return cartItems, totalAmount


@router.post("/cart/total", response_model=schemas.CartTotalOut)
def cartTotal(
    data: schemas.CartTotalRequest,
    db: Session = Depends(get_db),
):
    cartItems, totalAmount = buildCart(data.items, db)
    return {"total_amount": totalAmount, "items": cartItems}


@router.post("/checkout", response_model=schemas.OrderOut)
def checkout(
    data: schemas.OrderCreate,
    db: Session = Depends(get_db),
):
    buyer = db.query(models.User).filter(models.User.id == data.buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    if buyer.role != models.UserRole.buyer:
        raise HTTPException(status_code=403, detail="Buyer role required")

    cartItems, totalAmount = buildCart(data.items, db)
    paymentStatus = (
        models.PaymentStatus.paid
        if data.payment_method == models.PaymentMethod.card
        else models.PaymentStatus.unpaid
    )

    order = models.Order(
        buyer_id=data.buyer_id,
        total_amount=totalAmount,
        payment_method=data.payment_method,
        payment_status=paymentStatus,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    orderItems = []
    for item in cartItems:
        orderItem = models.OrderItem(
            order_id=order.id,
            watch_id=item.watch_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            line_total=item.line_total,
        )
        db.add(orderItem)
        orderItems.append(orderItem)

    db.commit()
    for orderItem in orderItems:
        db.refresh(orderItem)

    return {
        "id": order.id,
        "buyer_id": order.buyer_id,
        "total_amount": order.total_amount,
        "payment_method": order.payment_method,
        "payment_status": order.payment_status,
        "created_at": order.created_at,
        "items": orderItems,
    }


@router.get("/{orderId}", response_model=schemas.OrderOut)
def getOrder(
    orderId: int,
    db: Session = Depends(get_db),
):
    order = db.query(models.Order).filter(models.Order.id == orderId).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    items = db.query(models.OrderItem).filter(models.OrderItem.order_id == orderId).all()
    return {
        "id": order.id,
        "buyer_id": order.buyer_id,
        "total_amount": order.total_amount,
        "payment_method": order.payment_method,
        "payment_status": order.payment_status,
        "created_at": order.created_at,
        "items": items,
    }


@router.get("/{orderId}/paymentSuccess")
def paymentSuccess(orderId: int):
    return {"message": "Payment successful", "order_id": orderId}
