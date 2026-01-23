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


router = APIRouter(
    prefix="/users",
    tags=["Auth"]
)

logger = logging.getLogger(__name__)
passwordResetCodes = {}


def generateCode(length=6):
    code = ""

    for i in range(length):
        number = random.randint(0, 9)
        code = code + str(number)

    return code

def sendSignupCode(recipientEmail: str, code: str):
    smtpHost = os.getenv("SMTP_HOST")
    smtpPort = int(os.getenv("SMTP_PORT", "587"))
    smtpUser = os.getenv("SMTP_USER")
    smtpPass = os.getenv("SMTP_PASS")
    smtpFrom = os.getenv("SMTP_FROM", smtpUser)

    if not smtpHost or not smtpUser or not smtpPass:
        raise HTTPException(status_code=500, detail=" wrong stuff here man")

    msg = EmailMessage()
    msg["Subject"] = "Your signup code"
    msg["From"] = smtpFrom
    msg["To"] = recipientEmail
    msg.set_content(f"Your verification code is {code}")

    with smtplib.SMTP(smtpHost, smtpPort) as server:
        server.starttls()
        logger.info("Attempting SMTP login for user: %s", smtpUser)
        server.login(smtpUser, smtpPass)
        server.send_message(msg)

def sendPasswordResetCode(recipientEmail: str, code: str):
    smtpHost = os.getenv("SMTP_HOST")
    smtpPort = int(os.getenv("SMTP_PORT", "587"))
    smtpUser = os.getenv("SMTP_USER")
    smtpPass = os.getenv("SMTP_PASS")
    smtpFrom = os.getenv("SMTP_FROM", smtpUser)

    if not smtpHost or not smtpUser or not smtpPass:
        raise HTTPException(status_code=500, detail="SMTP credentials not configured")

    msg = EmailMessage()
    msg["Subject"] = "Your password reset code"
    msg["From"] = smtpFrom
    msg["To"] = recipientEmail
    msg.set_content(f"Your password reset code is {code}")

    with smtplib.SMTP(smtpHost, smtpPort) as server:
        server.starttls()
        logger.info("Attempting SMTP login for user: %s", smtpUser)
        server.login(smtpUser, smtpPass)
        server.send_message(msg)

@router.post("/signUp", response_model=schemas.UserOut)
def signUp(userCred: schemas.UserCreate, db: Session = Depends(get_db)):
    existingUser = db.query(models.User).filter(models.User.email == userCred.email).first()

    if existingUser:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    signupCode = generateCode()
    sendSignupCode(userCred.email, signupCode)

    userRole = userCred.role or models.UserRole.buyer
    newUser = models.User(
        username=userCred.username,
        email=userCred.email,
        password_hash=userCred.password_hash,
        role=userRole,
    )

    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser


@router.post("/login")
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if user:
        if data.password_hash == user.password_hash:
            return {"msg": "Login successful"}
        return {"msg": " Wrong password, or Wrong Login"}
    return {"message": "This account email doesn't exist"}


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
