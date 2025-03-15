from typing import Dict, Any, List
import re
from datetime import datetime


def validate_product_data(product_data: Dict[str, Any]) -> bool:
    required_fields = ["name", "manufacturer", "batch_number"]

    # Check required fields
    if not all(field in product_data for field in required_fields):
        return False

    # Validate name
    if not isinstance(product_data["name"], str) or len(product_data["name"]) < 1:
        return False

    # Validate batch number format (e.g., "BATCH-2024-001")
    batch_pattern = r"^BATCH-\d{4}-\d{3}$"
    if not re.match(batch_pattern, product_data["batch_number"]):
        return False

    return True


def validate_tracking_event(event_data: Dict[str, Any]) -> bool:
    required_fields = ["location", "timestamp", "event_type"]

    # Check required fields
    if not all(field in event_data for field in required_fields):
        return False

    # Validate timestamp
    try:
        if isinstance(event_data["timestamp"], str):
            datetime.fromisoformat(event_data["timestamp"].replace("Z", "+00:00"))
        elif not isinstance(event_data["timestamp"], (int, float)):
            return False
    except ValueError:
        return False

    # Validate location format
    if not isinstance(event_data["location"], str) or len(event_data["location"]) < 1:
        return False

    # Validate event type
    valid_event_types = ["created", "shipped", "received", "stored", "delivered"]
    if event_data["event_type"] not in valid_event_types:
        return False

    return True


def validate_prediction_data(data: Dict[str, Any]) -> bool:
    required_fields = ["historical_data", "features"]

    # Check required fields
    if not all(field in data for field in required_fields):
        return False

    # Validate historical data
    if not isinstance(data["historical_data"], list):
        return False

    # Validate features
    if not isinstance(data["features"], list):
        return False

    return True


def sanitize_input(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove any potentially harmful characters or data"""
    sanitized = {}

    for key, value in input_data.items():
        if isinstance(value, str):
            # Remove any control characters
            value = "".join(char for char in value if ord(char) >= 32)
            # Limit string length
            value = value[:1000]
        elif isinstance(value, (list, dict)):
            # Recursively sanitize nested structures
            value = (
                sanitize_input(value)
                if isinstance(value, dict)
                else [
                    sanitize_input(item) if isinstance(item, dict) else item
                    for item in value
                ]
            )

        sanitized[key] = value

    return sanitized


def format_blockchain_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Format blockchain response for API output"""
    formatted = {
        "transaction_hash": response.get("hash", ""),
        "status": response.get("status", "pending"),
        "timestamp": datetime.utcnow().isoformat(),
    }

    if "error" in response:
        formatted["error"] = response["error"]

    return formatted
