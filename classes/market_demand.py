from classes.base_object import BaseObject
from typing import List, Dict, Optional

class MarketDemand(BaseObject):
    storage_file: str = 'market_demand.json'

    # Explicit attribute annotations
    id: int
    total_addressable_market: float
    serviceable_available_market: float
    serviceable_obtainable_market: float
    growth_rate: float
    competitors: List[str]
    market_segments: Dict[str, float]

    def __init__(self, 
                 total_addressable_market: float = 0.0, 
                 serviceable_available_market: float = 0.0,
                 serviceable_obtainable_market: float = 0.0, 
                 growth_rate: float = 0.0,
                 competitors: Optional[List[str]] = None,
                 market_segments: Optional[Dict[str, float]] = None,
                 id: Optional[int] = None):

        super().__init__(
            id=id,
            total_addressable_market=total_addressable_market,
            serviceable_available_market=serviceable_available_market,
            serviceable_obtainable_market=serviceable_obtainable_market,
            growth_rate=growth_rate,
            competitors=competitors or [],
            market_segments=market_segments or {}
        )