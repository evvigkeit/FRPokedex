from fastapi.security import OAuth2PasswordBearer

oauth2scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = 120