class Color:
    __slots__ = ["data"]
    def __init__(self,color:int):
        self.data = color

    def __eq__(self,other) -> bool:
        if not isinstance(other,Color):
            raise TypeError(f"Color can't compare with {type(other)}")
        return self.data == other.data

class Liquid:
    __slots__ = ["color"]
    def __init__(self,color:int):
        if not isinstance(color,int):
            raise TypeError(f"Color of liquid must be int, but {type(color)}")
        if color < 0:
            raise ValueError(f"Color of liquid must bigger than zero, but {color}")
        self.color = Color(color)

    def __repr__(self):
        return str(self.color.data)
    
    def __str__(self):
        return self.__repr__()

    def __eq__(self,other) -> bool:
        if not isinstance(other,Liquid):
            raise TypeError(f"Liquid can't compare with {type(other)}")
        return self.color == other.color
    
    def __ne__(self,other) -> bool:
        return not (self == other)

class Tube:
    __slots__ = ["liquid","empty"]
    def __init__(self,liquid:list[Liquid|int]):
        for i in range(len(liquid)):
            if not isinstance(liquid[i],Color):
                liquid[i] = Liquid(liquid[i])
                
        self.liquid = liquid
        self.empty = 4 - len(liquid)

    def __setattr__(self, name, value):
        if(name == "liquid"):
            if not isinstance(value,list):
                raise TypeError(f"Liquid of tube musted be list, but {type(value)}")
            if len(value) > 4:
                raise ValueError(f"Tube have max four liquid, but given {len(value)}")
            super().__setattr__(name,value)
        
        elif(name == "empty"):
            if not isinstance(value,int):
                raise TypeError(f"Empty of tube musted be int, but{type(value)}")
            if(value < 0 or value > 4):
                raise ValueError(f"Empty of tube must between 0 to 4, but{value}")
            super().__setattr__(name,value)

    def __repr__(self):
        return str(self.liquid)
    
    def __str__(self):
        return self.__repr__()

    def __getitem__(self,index:int):
        return self.liquid[index]

    def __add__(self,other) -> None:
        if not isinstance(other,Tube):
            raise TypeError(f"Tube can't add with {type(other)}")
        
        while (self.empty < 4) and (other.empty > 0) and (self[-1] == other[-1]):
            other.liquid.append(self.liquid.pop())
            self.empty += 1
            other.empty -= 1

    def is_empty(self) -> bool:
        return (self.empty == 4)
    
    def is_full(self) -> bool:
        return not self.is_empty()
    
    def is_finished(self) -> bool:
        if not self.is_full():
            return False
        for each in self.liquid:
            if each != self.liquid[0]:
                return False
        return True
