from typing import List
from typing import Tuple


class Me:

    def greet(self):
        print("Hello I'm Jinsung Ha!")

    @property
    def education(self) -> str:
        degree = 'MEng Computing (Artificial Intelligence)'
        where = 'Imperial College London'
        when = '10.2014 - 06.2019'
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
