from fastapi import FastAPI
from app.controllers import login_controller, offer_controller, reco_controller
from app.middlewares.timing_logger import ExecutionTimeLoggerMiddleware
from app.middlewares.offers_timeout import OffersRouteTimeOut

app = FastAPI()

app.add_middleware(ExecutionTimeLoggerMiddleware)
app.add_middleware(OffersRouteTimeOut)

app.include_router(login_controller.router)
app.include_router(offer_controller.router)
app.include_router(reco_controller.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)