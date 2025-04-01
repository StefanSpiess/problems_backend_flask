from typing import Any, Dict, Optional

from classes.base_object import BaseObject
from classes.market_demand import MarketDemand
from classes.problem import Problem
from classes.solution_maturity import SolutionMaturity
from classes.solution_space import SolutionSpace


class ProblemSolution(BaseObject):
    storage_file: str = 'problem_solution.json'
    STATUS_VALUES = ["Idea", "In Development", "Testing", "Finished"]
    ...

    id: Optional[int]
    name: str
    problem_id: int
    market_demand_id: int
    solution_space_id: int
    solution_maturity_id: int
    user_id: Optional[int]  # <-- NEU: ID des Verantwortlichen Users
    status: str  # wir erstellen später einen Statusworkflow

    def __init__(self, 
                 name: str,
                 problem_id: int,
                 market_demand_id: int,
                 solution_space_id: int,
                 solution_maturity_id: int,
                 user_id: Optional[int] = None,
                 status: str = "Idea",
                 id: Optional[int] = None):
        
        if status not in self.STATUS_VALUES:
            raise ValueError(f"Invalid status '{status}'. Must be one of {self.STATUS_VALUES}")

        super().__init__(
            id=id,
            name=name,
            problem_id=problem_id,
            market_demand_id=market_demand_id,
            solution_space_id=solution_space_id,
            solution_maturity_id=solution_maturity_id,
            user_id=user_id,
            status=status
        )

    def load_sub_object(self, cls, obj_id) -> Optional[Dict[str, Any]]:
        obj = cls.find_by_id(obj_id)
        return obj.to_dict() if obj else None

    def to_full_dict(self) -> Dict[str, Any]:
        return {
            'id': self.get_attribute('id'),
            'name': self.get_attribute('name'),
            'updated_at': self.get_attribute('updated_at', None),
            'problem': self.load_sub_object(Problem, self.get_attribute('problem_id')),
            'market_demand': self.load_sub_object(MarketDemand, self.get_attribute('market_demand_id')),
            'solution_space': self.load_sub_object(SolutionSpace, self.get_attribute('solution_space_id')),
            'solution_maturity': self.load_sub_object(SolutionMaturity, self.get_attribute('solution_maturity_id'))
        }