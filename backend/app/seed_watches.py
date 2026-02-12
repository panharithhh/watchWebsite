from database import SessionLocal
import models
from passlib.context import CryptContext


SEED_WATCHES = [
    {
        "name": "Submariner Date 16610",
        "brand": "Rolex",
        "price": 11950.00,
        "description": "Diver category, 300m water resistance.",
        "tags": "category:diver,rolex,submariner",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Rolex-Submariner.jpg",
    },
    {
        "name": "Datejust 16013",
        "brand": "Rolex",
        "price": 8950.00,
        "description": "Dress category, classic two-tone style.",
        "tags": "category:dress,rolex,datejust",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Rolex_Datejust_16013.jpg",
    },
    {
        "name": "GMT Master II 126710BLRO",
        "brand": "Rolex",
        "price": 15800.00,
        "description": "Travel category, dual time bezel.",
        "tags": "category:travel,rolex,gmt",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Rolex_GMT_Master_II_126710BLRO.jpg",
    },
    {
        "name": "Nautilus 5711",
        "brand": "Patek",
        "price": 129995.00,
        "description": "Sport category, iconic steel luxury.",
        "tags": "category:sport,patek,nautilus",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Patek-Philippe-Nautilus-5711.jpg",
    },
    {
        "name": "Calatrava 5055",
        "brand": "Patek",
        "price": 29500.00,
        "description": "Dress category, slim gold case.",
        "tags": "category:dress,patek,calatrava",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Patek_Philippe_Calatrava_ref._5055.jpg",
    },
    {
        "name": "Speedmaster",
        "brand": "Omega",
        "price": 6900.00,
        "description": "Chronograph category, moonwatch icon.",
        "tags": "category:chronograph,omega,speedmaster",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Omega_Speedmaster_%2851310333132%29.jpg",
    },
    {
        "name": "Seamaster Diver Chronograph",
        "brand": "Omega",
        "price": 7200.00,
        "description": "Diver category, chronograph bezel.",
        "tags": "category:diver,omega,seamaster",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Omega_Seamaster_Diver_chronograph_watch_%28300_m_water_resistance%29.jpg",
    },
    {
        "name": "Constellation Rotgold 1958",
        "brand": "Omega",
        "price": 8400.00,
        "description": "Dress category, vintage 1958 dial.",
        "tags": "category:dress,omega,constellation",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Omega_Constellation_Rotgold_1958.jpg",
    },
    {
        "name": "Royal Oak 15202",
        "brand": "Audemars",
        "price": 52000.00,
        "description": "Sport category, blue dial, octagon.",
        "tags": "category:sport,audemars,royal-oak",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Audemars_Piguet_Royal_Oak_ref._15202.jpg",
    },
    {
        "name": "Royal Oak Offshore",
        "brand": "Audemars",
        "price": 38900.00,
        "description": "Chronograph category, bold case.",
        "tags": "category:chronograph,audemars,royal-oak,offshore",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Royal_Oak_Offshore_watch_by_Audemars_Piguet.JPG",
    },
    {
        "name": "Big Pilot St Exupery",
        "brand": "IWC",
        "price": 12500.00,
        "description": "Pilot category, oversized crown.",
        "tags": "category:pilot,iwc,big-pilot",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/IWC_Big_Pilot_St_Exupery_Edition_%28cropped%29.jpg",
    },
    {
        "name": "Portuguese Automatic",
        "brand": "IWC",
        "price": 9900.00,
        "description": "Dress category, clean open dial.",
        "tags": "category:dress,iwc,portuguese",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/IWC_Portuguese_Automatic_%28cropped%29.JPG",
    },
    {
        "name": "Aquatimer",
        "brand": "IWC",
        "price": 5600.00,
        "description": "Diver category, rotating timing ring.",
        "tags": "category:diver,iwc,aquatimer",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/IWC_Aquatimer.jpg",
    },
    {
        "name": "Santos",
        "brand": "Cartier",
        "price": 7800.00,
        "description": "Dress category, square case icon.",
        "tags": "category:dress,cartier,santos",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Cartier_Santos_wristwatch.jpg",
    },
    {
        "name": "Tank Americaine",
        "brand": "Cartier",
        "price": 9200.00,
        "description": "Dress category, elongated Tank case.",
        "tags": "category:dress,cartier,tank",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Tank_Americaine%2C_designed_by_Louis_Cartier%2C_1917_-_Design_Museum%2C_Kensington_-_London_-_DSC01588.jpg",
    },
    {
        "name": "Navitimer",
        "brand": "Breitling",
        "price": 9400.00,
        "description": "Chronograph category, slide rule bezel.",
        "tags": "category:chronograph,breitling,navitimer",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Breitling-Navitimer.jpg",
    },
    {
        "name": "Superocean 01",
        "brand": "Breitling",
        "price": 5200.00,
        "description": "Diver category, rugged steel build.",
        "tags": "category:diver,breitling,superocean",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Breitling_Superocean_01.jpg",
    },
    {
        "name": "Luminor Marina PAM 111",
        "brand": "Panerai",
        "price": 7600.00,
        "description": "Tool category, crown-guard bridge.",
        "tags": "category:tool,panerai,luminor",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/LUMINOR_%2830075754506%29.jpg",
    },
    {
        "name": "Radiomir California",
        "brand": "Panerai",
        "price": 8600.00,
        "description": "Tool category, California dial.",
        "tags": "category:tool,panerai,radiomir",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Radiomircalifornia.jpg",
    },
    {
        "name": "Carrera Chronograph CV2010",
        "brand": "TAG Heuer",
        "price": 4200.00,
        "description": "Chronograph category, racing heritage.",
        "tags": "category:chronograph,tagheuer,carrera",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/TAG_Heuer_Carrera_chronograph_CV2010.JPG",
    },
    {
        "name": "Monaco 24",
        "brand": "TAG Heuer",
        "price": 5900.00,
        "description": "Chronograph category, square case.",
        "tags": "category:chronograph,tagheuer,monaco",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/TAG_Heuer_Monaco_24_%28cropped%2C_turned%2C_colours%29.jpg",
    },
    {
        "name": "Black Bay Chrono 79350",
        "brand": "Tudor",
        "price": 4900.00,
        "description": "Diver category, black bay chrono.",
        "tags": "category:diver,tudor,black-bay",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Tudor_Black_Bay_Chrono_ref._79350.jpg",
    },
    {
        "name": "Black Bay 54",
        "brand": "Tudor",
        "price": 4100.00,
        "description": "Diver category, vintage-inspired.",
        "tags": "category:diver,tudor,black-bay",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Tudor_Black_Bay_54_ref._m79000n-0001.jpg",
    },
    {
        "name": "Seiko 5 6309-5320",
        "brand": "Seiko",
        "price": 750.00,
        "description": "Everyday category, automatic movement.",
        "tags": "category:everyday,seiko,automatic",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Seiko_5.jpg",
    },
    {
        "name": "Seiko SJW041P1",
        "brand": "Seiko",
        "price": 220.00,
        "description": "Dress category, quartz classic.",
        "tags": "category:dress,seiko,quartz",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Seiko_watch.jpg",
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
