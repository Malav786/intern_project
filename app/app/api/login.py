from fastapi import APIRouter, HTTPException, Response
from app.utils.otp import login_user
from app.db.connection import get_db
from fastapi import Depends, Form
from sqlalchemy.orm import Session
from fastapi.security import HTTPBasic, OAuth2PasswordRequestForm
from typing import Any
from app.pass_hashing import hasher
import app.models.users as user_db
from app.schemas.users import userAdd
from app.crud import crud_fn
from app.utils.email import email
from app.schemas import tokens, users
import random
from datetime import timedelta
from app.utils.token import tokens
from starlette.responses  import RedirectResponse
import re
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



security = HTTPBasic() 
otp = random.randint(1000, 9999)
templates = Jinja2Templates(directory="E:/photobooth_Management/app/app/templates")
COOKIE_NAME = "asdf"



class login():
    router = APIRouter()

    @router.get("/")
    def home(request: Request, db: Session = Depends(get_db)):
        return templates.TemplateResponse("index.html", {"request": request})
    
    @router.get("/about")
    def home(request: Request):
        return templates.TemplateResponse("about.html", {"request": request})
    
    @router.get("/user/signup")
    def signup(req: Request):
        return templates.TemplateResponse("signup.html", {"request": req})
    
    @router.get("/landing")
    def signup(req: Request):
        return templates.TemplateResponse("landing.html", {"request": req})
    
    @router.post("/signupuser")
    def signup_user(request: Request, db:Session=Depends(get_db), username : str = Form(...), email:str=Form(...), password:str=Form(...)):
        print(username)
        print(email)
        print(password)
        existing_user = db.query(user_db).filter_by(email=email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

        mv_details = user_db(
            name=username,
            email=email,
            password=hasher.get_pass_hashed(password)
        )
        db.add(mv_details)
        db.commit()
        db.refresh(mv_details)

        # SendEmailVerify.sendVerify(token)

        return templates.TemplateResponse("landing.html", {"request": request})
    
    @router.get("/user/signin")
    def login(req: Request):
        return templates.TemplateResponse("/signin.html", {"request": req})
    
        
    @router.post("/homepage")
    def signin_user(req: Request, response:Response, db:Session=Depends(get_db), username : str = Form(...), password:str=Form(...)):
        # db_user = db.query(user_db).filter_by(email=username).first()
        user = login_user.loginuser(db, username, password)
        if not user:
            return "username or password is not valid"
    
        if hasher.verify_pass(password,user.password):
            token=tokens.create_token(username, db)
            response.set_cookie(
                key=COOKIE_NAME,
                value=token,
                httponly=True,
                expires=1800
            )
            return templates.TemplateResponse("/landing.html", {"request": req, "username": username})
        
    @router.get("/user/success")
    def success(req: Request):
        return templates.TemplateResponse("/success.html", {"request": req})
        

    @router.post("/login/access-token")
    def login_access_token(db: Session = Depends(get_db), email:str=Form(), password:str=Form(), form_data: OAuth2PasswordRequestForm = Depends()):
        user = login_user.loginuser(db, email, password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        #access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return tokens.create_token(email, db)
    
    
    @router.get('/user/verify/{token}')
    def verify_user(token, db: Session = Depends(get_db)):
        payload = tokens.verify_token(token)
        username=payload.get("username")
        user = db.query(user_db).filter_by(email=username).first()
        if not user:
            #return {"Token is not for user: {username}"}
            raise  HTTPException(status_code=401, detail="Credentials not correct")
        else:
            return {"Token is for user": {username}}

    @router.post("/register")
    def register(user_email, db: Session = Depends(get_db)):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', user_email):
            raise HTTPException(status_code=400, detail="Invalid email address")
        print(user_email)
        email_sent = email.send_email(user_email, otp)
        print(user_email)
        if email_sent:
            return {"status": "success",
                    "message": "OTP sent to mail"}
        
    @router.post("/verifyotp")
    def verify_otp(user_create: userAdd, user_otp: int, db: Session = Depends(get_db)):
        if user_otp == otp:
            user = crud_fn.add_details_to_db(db=db, user=user_create)
            return  {"status": "success",
                    "message": "User added successfully"}
        else:
            return {"status": "failed",
                    "message": "User not added"}
        
        
    @router.get("/sendotp")
    async def forgot_password(request: Request):
        return templates.TemplateResponse("getemail.html", {"request": request})
        
    @router.post("/send-email")
    async def send_email(request: Request):
        form_data = await request.form()
        user_email = form_data["username"]
        email.send_email(user_email, otp)
        return templates.TemplateResponse("resetpassword.html", {"request": request})

        
    @router.post("/forgotpassword")
    def initiate_password_change(user_email:str=Form(), db: Session = Depends(get_db)):
        email.send_email(user_email, otp)
        print("Succesfully sent mail")
        return templates.TemplateResponse("resetpassword.html")
    
    @router.get("/passwordreset")
    async def forgot_password(request: Request):
        return templates.TemplateResponse("resetpassword.html", {"request": request})
        
    @router.post('/reset-password')
    def verify_password_change(username:str=Form(), user_otp:str=Form(), new_password:str=Form(), db: Session = Depends(get_db)):
        is_valid_otp = login_user.verify_otp(otp, username, user_otp, db)
        if is_valid_otp:
            login_user.update_password(username, new_password, db)
        else:
            raise HTTPException(status_code=401, detail="Invalid OTP")  
        return {"status": "success",
                "message": "Password changed successfully"}
    
    
   