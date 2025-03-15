from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uvicorn

from src.models.base import get_db
from src.blockchain.smart_contract import SmartContractManager
from src.ai.predictor import SupplyChainPredictor
from src.config.settings import API_V1_PREFIX, PROJECT_NAME, API_PORT

app = FastAPI(title=PROJECT_NAME)
security = HTTPBearer()
blockchain_manager = SmartContractManager()
ai_predictor = SupplyChainPredictor()


@app.get("/")
async def root():
    return {"message": "Supply Chain Management System API"}


@app.post(f"{API_V1_PREFIX}/products/create")
async def create_product(
    product_data: Dict[str, Any],
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    try:
        # Create product on blockchain
        tx_hash = blockchain_manager.create_product(
            product_data, credentials.credentials
        )

        # Store in database
        # Implementation details...

        return {"status": "success", "transaction_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(f"{API_V1_PREFIX}/products/{product_id}/update-status")
async def update_product_status(
    product_id: int,
    status: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    try:
        tx_hash = blockchain_manager.update_product_status(
            product_id, status, credentials.credentials
        )
        return {"status": "success", "transaction_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get(f"{API_V1_PREFIX}/products/{product_id}/history")
async def get_product_history(product_id: int, db: Session = Depends(get_db)):
    try:
        history = blockchain_manager.get_product_history(product_id)
        return {"status": "success", "history": history}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(f"{API_V1_PREFIX}/ai/predict-bottlenecks")
async def predict_supply_chain_bottlenecks(
    data: Dict[str, Any], db: Session = Depends(get_db)
):
    try:
        predictions = ai_predictor.predict_bottlenecks(data)
        return {"status": "success", "predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(f"{API_V1_PREFIX}/ai/predict-demand")
async def predict_demand(
    historical_data: Dict[str, Any], db: Session = Depends(get_db)
):
    try:
        forecast = ai_predictor.predict_demand(historical_data)
        return {"status": "success", "forecast": forecast}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=API_PORT, reload=True)
