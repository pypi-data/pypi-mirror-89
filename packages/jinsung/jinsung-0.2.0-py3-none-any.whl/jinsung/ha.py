from typing import List
from typing import Tuple


class Me:

    def __init__(self):
        print('About Me - Jinsung Ha')

    @property
    def education(self) -> str:
        degree: str = 'MEng Computing (Artificial Intelligence)'
        where: str = 'Imperial College London'
        when: str = '10.2014 - 06.2019'
        return ' | '.join([degree, where, when])

    @property
    def workspace(self) -> Tuple[str, str]:
        company: str = 'LUXROBO'
        position: str = 'Backend Software Engineer'
        return company, position

    @property
    def code(self) -> List[str]:
        return [
            'Python', 'Java', 'C', 'C++', 'Bash'
        ]
