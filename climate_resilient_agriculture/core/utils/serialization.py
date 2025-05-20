from datetime import datetime
from typing import Any, Dict, List
from sqlalchemy.orm import Query

def serialize_datetime(obj: datetime) -> str:
    """Convert datetime to ISO format string"""
    return obj.isoformat()

def serialize_region(region: Dict) -> Dict:
    """Return region dict as-is (already contains all required fields)"""
    return region

def serialize_results(results: List[Dict]) -> List[Dict]:
    """Serialize simulation results for JSON storage"""
    serialized = []
    for result in results:
        serialized_result = {
            'date': serialize_datetime(result['date']),
            'regions': [serialize_region(region) for region in result['regions']]
        }
        serialized.append(serialized_result)
    return serialized 