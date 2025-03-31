from classes.base_object import BaseObject
from typing import Optional

class SolutionMaturity(BaseObject):
    storage_file: str = 'solution_maturity.json'

    # Explicit attribute annotations
    id: Optional[int]
    level: str                      # e.g., "Idea", "Prototype", "Proof-of-Concept", "Production-ready", "Mature"
    description: str                # Brief description of the maturity stage
    readiness_score: float          # Numeric value (0-1) indicating readiness level
    recommended_next_steps: str     # Text description of recommended next steps or actions
    updated_at: Optional[str]       # ISO-formatted timestamp

    def __init__(self,
                 level: str,
                 description: str,
                 readiness_score: float,
                 recommended_next_steps: str,
                 id: Optional[int] = None):

        super().__init__(
            id=id,
            level=level,
            description=description,
            readiness_score=readiness_score,
            recommended_next_steps=recommended_next_steps
        )