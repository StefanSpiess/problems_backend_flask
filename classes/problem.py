from classes.base_object import BaseObject
from typing import List, Optional

class Problem(BaseObject):
    storage_file: str = 'problem.json'

    # Epistemically well-defined Problem clearly
    id: Optional[int]
    description: str
    context: Optional[str]
    impact: str
    root_causes: List[str]
    stakeholders: List[str]
    updated_at: Optional[str]
    problem_solution_ids: List[int]  # <-- clearly list related solution IDs

    def __init__(self,
                 description: str,
                 context: Optional[str],
                 impact: str,
                 root_causes: Optional[List[str]] = None,
                 stakeholders: Optional[List[str]] = None,
                 problem_solution_ids: Optional[List[int]] = None,
                 id: Optional[int] = None):

        super().__init__(
            id=id,
            description=description,
            context=context,
            impact=impact,
            root_causes=root_causes or [],
            stakeholders=stakeholders or [],
            problem_solution_ids=problem_solution_ids or []
        )