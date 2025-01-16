from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time

from app.config import metric_logger_path

logger_M = logging.getLogger("metrics_logger")
logger_M.setLevel(logging.INFO)
file_handler = logging.FileHandler(metric_logger_path)
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
logger_M.addHandler(file_handler)


class   MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        status_code = response.status_code
        endpoint = request.url.path

        response_time = time.time() - start_time

        logger_M.info(f"Endpoint: {endpoint} | Status: {status_code} | Time: {response_time:.4f}s")

        return response
