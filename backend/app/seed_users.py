from passlib.context import CryptContext

from database import SessionLocal
import models


pwd_context = CryptContext(schemes=["pbkdf2_sha256"])


def ensure_user(username: str, email: str, password: str, role: str, seller_verified: bool = True):
    db = SessionLocal()
    try:
        existing = db.query(models.User).filter(models.User.email == email).first()
        if existing:
            print(f"{email} already exists (role={existing.role}, id={existing.id})")
            return
        user = models.User(
            username=username,
            email=email,
            password_hash=pwd_context.hash(password),
            role=role,
            seller_verified=seller_verified,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created {email} (role={user.role}, id={user.id})")
    finally:
        db.close()


if __name__ == "__main__":
    ensure_user("user1", "user1@gmail.com", "user1", models.UserRole.buyer.value, True)
    ensure_user("seller1", "seller1@gmail.com", "seller1", models.UserRole.seller.value, True)
    ensure_user("admin1", "admin1@gmail.com", "admin1", models.UserRole.admin.value, True)
