from base_object import BaseObject
from problem import Problem
from market_demand import MarketDemand
from solution_space import SolutionSpace
from solution_maturity import SolutionMaturity

class ProblemSolution(BaseObject):
    storage_file = 'problem_solution.json'

    def __init__(self, name: str,
                 problem_id: int,
                 market_demand_id: int,
                 solution_space_id: int,
                 solution_maturity_id: int,
                 id=None):

        super().__init__(
            id=id,
            name=name,
            problem_id=problem_id,
            market_demand_id=market_demand_id,
            solution_space_id=solution_space_id,
            solution_maturity_id=solution_maturity_id
        )

    def load_sub_object(self, cls, obj_id):
            obj = cls.find_by_id(obj_id)
            return obj.to_dict() if obj else None

    def to_full_dict(self):
        return {
            'id': self.get_attribute('id'),
            'name': self.get_attribute('name'),
            'updated_at': self.get_attribute('updated_at', None),
            'problem': self.load_sub_object(Problem, self.get_attribute('problem_id')),
            'market_demand': self.load_sub_object(MarketDemand, self.get_attribute('market_demand_id')),
            'solution_space': self.load_sub_object(SolutionSpace, self.get_attribute('solution_space_id')),
            'solution_maturity': self.load_sub_object(SolutionMaturity, self.get_attribute('solution_maturity_id'))
        }