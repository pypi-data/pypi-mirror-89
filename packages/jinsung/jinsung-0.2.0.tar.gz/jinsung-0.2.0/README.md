## :nerd_face: About Me

From your terminal,
```bash
pip install jinsung
```
Then in python shell,
```python
import jinsung
```

Briefly,
```python
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
    def location(self) -> Tuple[float, float]:
        return 37.5665, 126.9780

    @property
    def code(self) -> List[str]:
        return [
            'Python', 'Java', 'C', 'C++', 'Bash'
        ]
```

## :chart_with_upwards_trend: Github Stats
[![Jinsung Ha's Github Stats](https://github-readme-stats.vercel.app/api?username=jha929&count_private=true&show_icons=true&hide_border=true)](https://github.com/jha929)
[![Jinsung Ha's Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=jha929&hide=jupyter%20notebook&hide_border=true&layout=compact)](https://github.com/jha929)
