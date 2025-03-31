from classes.base_object import BaseObject
from typing import List, Optional

class SolutionSpace(BaseObject):
    storage_file: str = 'solution_space.json'

    # Explicit attribute annotations
    id: Optional[int]
    name: str                                 # Short descriptive name (e.g. "Blockchain-based payment systems")
    description: str                          # General context or scope definition
    required_skills: List[str]                # e.g. ["Blockchain development", "Cryptography"]
    technologies: List[str]                   # e.g. ["Ethereum", "Solidity", "Web3.js"]
    additional_notes: Optional[str]           # Free-text field for insights or comments
    updated_at: Optional[str]                 # ISO-formatted timestamp

    def __init__(self,
                 name: str,
                 description: str,
                 required_skills: Optional[List[str]] = None,
                 technologies: Optional[List[str]] = None,
                 additional_notes: Optional[str] = None,
                 id: Optional[int] = None):

        super().__init__(
            id=id,
            name=name,
            description=description,
            required_skills=required_skills or [],
            technologies=technologies or [],
            additional_notes=additional_notes
        )