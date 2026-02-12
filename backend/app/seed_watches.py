from database import SessionLocal
import models
from passlib.context import CryptContext


SEED_WATCHES = [
    {
        "name": "Rolex Datejust",
        "brand": "Rolex",
        "price": 28995.00,
        "description": "Full set, 41mm, verified listing.",
        "tags": "rolex,datejust,classic",
        "image_url": "https://images.unsplash.com/photo-1625258832775-0bcbdd61b280?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Patek Nautilus",
        "brand": "Patek",
        "price": 129995.00,
        "description": "Steel sports icon with blue dial.",
        "tags": "patek,nautilus,sports",
        "image_url": "https://images.unsplash.com/photo-1735137019205-0e8431694e15?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Omega Seamaster",
        "brand": "Omega",
        "price": 8900.00,
        "description": "Diver classic, ceramic bezel.",
        "tags": "omega,seamaster,diver",
        "image_url": "https://images.unsplash.com/photo-1645760370913-1a34f83814c6?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Audemars Royal Oak",
        "brand": "Audemars",
        "price": 44500.00,
        "description": "Octagonal bezel, integrated bracelet.",
        "tags": "audemars,royal oak,luxury",
        "image_url": "https://images.unsplash.com/photo-1662230178048-8d1a2649b3dd?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "IWC Pilot Chronograph",
        "brand": "IWC",
        "price": 8200.00,
        "description": "Aviation classic with chronograph complication.",
        "tags": "iwc,pilot,chronograph",
        "image_url": "https://images.unsplash.com/photo-1661030419605-3d4ca9cda193?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Cartier Santos",
        "brand": "Cartier",
        "price": 7500.00,
        "description": "Iconic square case with steel bracelet.",
        "tags": "cartier,santos,classic",
        "image_url": "https://images.unsplash.com/photo-1646141496467-379a5b6202a2?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Breitling Navitimer",
        "brand": "Breitling",
        "price": 9800.00,
        "description": "Slide rule bezel and aviation heritage.",
        "tags": "breitling,navitimer,aviation",
        "image_url": "https://images.unsplash.com/photo-1665682603248-5101564253bc?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Panerai Luminor",
        "brand": "Panerai",
        "price": 9100.00,
        "description": "Cushion case with signature crown guard.",
        "tags": "panerai,luminor,toolwatch",
        "image_url": "https://images.unsplash.com/photo-1735137019201-7b5a4fe586f7?auto=format&fit=crop&w=900&q=80",
    },
]


def seed():
    db = SessionLocal()
    try:
        seller = db.query(models.User).order_by(models.User.id.asc()).first()
        if not seller:
            pwd_context = CryptContext(schemes=["pbkdf2_sha256"])
            seller = models.User(
                username="seed-seller",
                email="seed-seller@example.com",
                password_hash=pwd_context.hash("seed1234"),
                role=models.UserRole.seller.value,
                seller_verified=True,
            )
            db.add(seller)
            db.commit()
            db.refresh(seller)

        for data in SEED_WATCHES:
            exists = (
                db.query(models.Watch)
                .filter(models.Watch.name == data["name"], models.Watch.brand == data["brand"])
                .first()
            )
            if exists:
                continue
            watch = models.Watch(
                name=data["name"],
                brand=data["brand"],
                price=data["price"],
                description=data["description"],
                tags=data["tags"],
                image_url=data["image_url"],
                status="approved",
                seller_id=seller.id,
                approved_by=seller.id,
            )
            db.add(watch)
        db.commit()
        print("Seeded watches successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
