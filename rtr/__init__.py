from dataclasses import dataclass


@dataclass
class Artist:
    name: str
    link: str = None
    origin: str = None
    birth: str = None