from App.models.models import Session,engine
from starlette.middleware.base import BaseHTTPMiddleware

class DBConnection(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.db = Session()
        response = await call_next(request)
        request.state.db.close()
        return response