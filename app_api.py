from auth_service import sign_up, login, get_session, sign_out, get_profile
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/sign_up")
def api_sign_up(email: str, password: str, username: str):
    return sign_up(email, password, username)

@app.post("/login")
def api_login(email: str, password: str):
    return login(email, password)

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