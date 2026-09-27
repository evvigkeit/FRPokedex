from fastapi.security import OAuth2PasswordBearer

oauth2scheme = OAuth2PasswordBearer(tokenUrl="token")

SESSION_EXPIRE_MINUTES = 5
COOKIE_SESSION_ID_KEY = "web-app-session-id"