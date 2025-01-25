global objArr
objArr: list["Obj"] = []
appObj = objArr.append


class Obj:
    def __init__(self, name: str, mass: float=1, pos: list[float]=[0, 0],
                 vel: list[float]=[0, 0]) -> None:
        self.name = name
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.txt = ''

    def __str__(self) -> str:
        return f"{self.name}: Mass={self.mass}, Vel={self.vel}"
    
    def rendStr(self) -> str:
        return ''


class Sq(Obj):
    def __init__(self, name: str, mass: float=1, pos: list[float]=[0, 0],
                 vel: list[float]=[0, 0], side: int=1) -> None:
        super().__init__(name, mass=mass, pos=pos, vel=vel)
        self.side = side
        self.txt = '#' * self.side

    def rendStr(self) -> str:
        return self.txt


# def createObj(type_: type, *args, **kwargs):
#     type_(*args, **kwargs)


obj1 = Obj('haha')
