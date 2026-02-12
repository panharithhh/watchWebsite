from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/services", tags=["Services"])

SERVICE_DATA = {
    "repair": {
        "key": "repair",
        "title": "Watch Repair",
        "summary": "Full-service mechanical and quartz repairs with OEM-grade parts.",
        "bullets": [
            "Complete movement inspection and diagnosis",
            "Water resistance testing and gasket replacement",
            "Polish/refinish on request",
            "2-year service warranty",
        ],
        "turnaround": "Typical turnaround: 7–14 business days",
        "price": "Starting at $250 (parts + labor)",
    },
}


@router.get("")
def get_service(service: str = Query(..., alias="type")):
    key = service.strip().lower()
    data = SERVICE_DATA.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="Service not found")
    return data

