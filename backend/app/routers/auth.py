from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from email.message import EmailMessage
import os
import smtplib
import random
import logging
from datetime import datetime, timedelta
from passlib.context import CryptContext
from security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

logger = logging.getLogger(__name__)
passwordResetCodes = {}
signupCodes = {}


def generateCode(length=6):
    code = ""

    for i in range(length):
        number = random.randint(0, 9)
        code = code + str(number)

    return code


# IMPORTANT: must match the hashes stored in DB (your users table has $2b$... bcrypt hashes)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signUp", response_model=schemas.UserOut)
def signUp(userCred: schemas.UserSignup, db: Session = Depends(get_db)):
    existingUser = db.query(models.User).filter(models.User.email == userCred.email).first()
    
    
    if existingUser:
        raise HTTPException(status_code=400, detail="Email already registered")

    if userCred.password != userCred.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if not userCred.signup_code:
        raise HTTPException(status_code=400, detail="Signup code required")

    stored = signupCodes.get(userCred.email)
    if not stored:
        raise HTTPException(status_code=400, detail="No signup code found")

    stored_code, expires_at = stored
    if datetime.utcnow() > expires_at:
        signupCodes.pop(userCred.email, None)
        raise HTTPException(status_code=400, detail="Signup code expired")

    if userCred.signup_code != stored_code:
        raise HTTPException(status_code=400, detail="Invalid signup code")

    requested_role = (userCred.role or "user").lower()
    if requested_role == "user":
        requested_role = models.UserRole.buyer.value
    if requested_role not in {r.value for r in models.UserRole}:
        raise HTTPException(status_code=400, detail="Invalid role")

    hashed_password = pwd_context.hash(userCred.password)

    seller_verified = True
    role_value = requested_role

    newUser = models.User(
        username=userCred.username,
        email=userCred.email,
        password_hash=hashed_password,
        role=role_value,
        seller_verified=seller_verified,
    )

    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    documents = [doc for doc in (userCred.documents or []) if isinstance(doc, str) and doc.strip()]
    if documents and role_value == models.UserRole.seller.value:
        for doc in documents:
            db.add(models.SellerDocument(user_id=newUser.id, data_url=doc))
        db.commit()

    signupCodes.pop(userCred.email, None)
    return newUser


@router.post("/requestSignupCode")
def request_signup_code(data: schemas.SignupCodeRequest, db: Session = Depends(get_db)):
    existingUser = db.query(models.User).filter(models.User.email == data.email).first()
    if existingUser:
        raise HTTPException(status_code=400, detail="Email already registered")

    code = generateCode()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    signupCodes[data.email] = (code, expires_at)

    sent = sendSignupCode(data.email, code)
    if not sent:
        return {"message": "SMTP not configured; use code below for development.", "code": code}

    return {"message": "Signup code sent"}

def sendSignupCode(recipientEmail: str, code: str) -> bool:
    smtpHost = os.getenv("SMTP_HOST")
    smtpPort = int(os.getenv("SMTP_PORT", "587"))
    smtpUser = os.getenv("SMTP_USER")
    smtpPass = os.getenv("SMTP_PASS")
    smtpFrom = os.getenv("SMTP_FROM", smtpUser)

    if not smtpHost or not smtpUser or not smtpPass:
        logger.warning("SMTP not configured; skipping signup email")
        return False

    msg = EmailMessage()
    msg["Subject"] = "Your signup code"
    msg["From"] = smtpFrom
    msg["To"] = recipientEmail
    msg.set_content(f"Your verification code is {code}")

    try:
        # Use SSL directly if port 465, otherwise STARTTLS (587)
        if smtpPort == 465:
            with smtplib.SMTP_SSL(smtpHost, smtpPort, timeout=10) as server:
                logger.info("Attempting SMTP SSL login for user: %s", smtpUser)
                server.login(smtpUser, smtpPass)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtpHost, smtpPort, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                logger.info("Attempting SMTP STARTTLS login for user: %s", smtpUser)
                server.login(smtpUser, smtpPass)
                server.send_message(msg)
        return True
    except Exception:
        logger.exception("Failed to send signup code via SMTP")
        return False

def sendPasswordResetCode(recipientEmail: str, code: str):
    smtpHost = os.getenv("SMTP_HOST")
    smtpPort = int(os.getenv("SMTP_PORT", "587"))
    smtpUser = os.getenv("SMTP_USER")
    smtpPass = os.getenv("SMTP_PASS")
    smtpFrom = os.getenv("SMTP_FROM", smtpUser)

    if not smtpHost or not smtpUser or not smtpPass:
        logger.warning("SMTP not configured; skipping reset email")
        return

    msg = EmailMessage()
    msg["Subject"] = "Your password reset code"
    msg["From"] = smtpFrom
    msg["To"] = recipientEmail
    msg.set_content(f"Your password reset code is {code}")

    try:
        if smtpPort == 465:
            with smtplib.SMTP_SSL(smtpHost, smtpPort, timeout=10) as server:
                logger.info("Attempting SMTP SSL login for user: %s", smtpUser)
                server.login(smtpUser, smtpPass)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtpHost, smtpPort, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                logger.info("Attempting SMTP STARTTLS login for user: %s", smtpUser)
                server.login(smtpUser, smtpPass)
                server.send_message(msg)
    except Exception:
        logger.exception("Failed to send password reset code via SMTP")

# @router.post("/signUp", response_model=schemas.UserOut)
# def signUp(userCred: schemas.UserCreate, db: Session = Depends(get_db)):
#     existingUser = db.query(models.User).filter(models.User.email == userCred.email).first()

#     if existingUser:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     signupCode = generateCode()
#     sendSignupCode(userCred.email, signupCode)

#     userRole = userCred.role or models.UserRole.buyer
#     newUser = models.User(
#         username=userCred.username,
#         email=userCred.email,
#         password_hash=userCred.password_hash,
#         role=userRole,
#     )

#     db.add(newUser)
#     db.commit()
#     db.refresh(newUser)

#     return newUser


@router.post("/login", response_model=schemas.TokenResponse)
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if user and pwd_context.verify(data.password, user.password_hash):
        token = create_access_token({"sub": str(user.id)})
        return {
            "access_token": token,
            "token_type": "bearer",
            "username": user.username,
            "role": user.role,
            "seller_verified": user.seller_verified,
        }

    raise HTTPException(status_code=401, detail="Wrong email or password")


@router.post("/forgotPassword")
def forgotPassword(data: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    resetCode = generateCode()
    expiresAt = datetime.utcnow() + timedelta(minutes=10)
    passwordResetCodes[data.email] = (resetCode, expiresAt)
    sendPasswordResetCode(data.email, resetCode)

    return {"message": "Reset code sent"}


@router.post("/loginWithCode")
def loginWithCode(data: schemas.LoginWithCode):
    stored = passwordResetCodes.get(data.email)
    if not stored:
        raise HTTPException(status_code=400, detail="No reset code found")

    storedCode, expiresAt = stored
    if datetime.utcnow() > expiresAt:
        passwordResetCodes.pop(data.email, None)
        raise HTTPException(status_code=400, detail="Reset code expired")

    if data.code != storedCode:
        raise HTTPException(status_code=400, detail="Invalid reset code")

    passwordResetCodes.pop(data.email, None)
    return {"message": "Login with code successful"}
