import enum
from dataclasses import dataclass

@dataclass(frozen=True)
class COMPONENT_TYPE:
    DEFAULT = "DEFAULT"
    STATS = "STATS"
    BODY = "BODY"
    DECAYING = "DECAYING"
    WEAPON = "WEAPON"
    ACCELERATOR = "ACCELERATOR"
    
@dataclass(frozen=True)
class SYSTEM_TYPE:
    PHYSICS = "PHYSICS"
    