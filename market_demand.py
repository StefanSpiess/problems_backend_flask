from base_object import BaseObject

class MarketDemand(BaseObject):
    storage_file = 'market_demand.json'

    def __init__(self, total_addressable_market=0.0, 
                 serviceable_available_market=0.0,
                 serviceable_obtainable_market=0.0, 
                 growth_rate=0.0,
                 competitors=None,
                 market_segments=None,
                 id=None):

        super().__init__(
            id=id,
            total_addressable_market=total_addressable_market,
            serviceable_available_market=serviceable_available_market,
            serviceable_obtainable_market=serviceable_obtainable_market,
            growth_rate=growth_rate,
            competitors=competitors or [],
            market_segments=market_segments or {}
        )
