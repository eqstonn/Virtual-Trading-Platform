from auth_service import sign_up, login, get_session, sign_out, get_profile
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models for JSON body validation
class SignUpRequest(BaseModel):
    email: str
    password: str
    username: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/sign_up")
def api_sign_up(request: SignUpRequest):
    result = sign_up(request.email, request.password, request.username)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/login")
def api_login(request: LoginRequest):
    result = login(request.email, request.password)
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])
    return result

@app.post("/signout")
def api_sign_out():
    sign_out()
    return {"status": "sucess", "detail": "logged out"}

@app.get("/session")
def api_get_session():
    user = get_session()
    if not user:
        raise HTTPException(status_code = 401, detail = "No active session found")
    return {"user_id": user.id, "email": user.email}

@app.get("/profile/{user_id}")
def api_get_profile(user_id: str):
    profile = get_profile(user_id)
    if not profile:
        raise HTTPException(status_code = 404, detail = "No profile exist")
    return profile