from random import shuffle
from pathlib import Path
import pygame

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
    __slots__ = ["liquid","liquid_count"]
    def __init__(self,liquid:list[Liquid|int] = []):
        '''Create a tube with liquid'''
        if len(liquid) == 0:
            liquid = []
        for i in range(len(liquid)):
            if not isinstance(liquid[i],(Liquid,int)):
                raise TypeError(f"Tube must be init with list of Liquid or int, but get {liquid[i]}")
            
            if isinstance(liquid[i],int):
                liquid[i] = Liquid(liquid[i])
                
        self.liquid = liquid
        self.liquid_count = len(liquid)

    def __setattr__(self, name, value):
        if(name == "liquid"):
            if not isinstance(value,list):
                raise TypeError(f"Liquid of tube musted be list, but {type(value)}")
            for each in value:
                if not isinstance(each,Liquid):
                    raise TypeError(f"Liquid of tube musted be list of liquid, but {type(each)}")
            if len(value) > 4:
                raise ValueError(f"Tube have max four liquid, but given {len(value)}")
            super().__setattr__(name,value)
        
        elif(name == "liquid_count"):
            if not isinstance(value,int):
                raise TypeError(f"Liquid_count of tube musted be int, but{type(value)}")
            if(value < 0 or value > 4):
                raise ValueError(f"Liquid_count of tube must between 0 to 4, but{value}")
            super().__setattr__(name,value)

    def __repr__(self):
        return str(self.liquid)
    
    def __str__(self):
        return self.__repr__()

    def __getitem__(self,index:int):
        return self.liquid[index]

    def __add__(self,other) -> int:
        '''Return number of moved liquid'''
        if not isinstance(other,Tube):
            raise TypeError(f"Tube can't add with {type(other)}")
        
        if(self.is_empty()):
            return 0
        
        ret = 0
        if(other.is_empty()):
            other.liquid.append(self.liquid.pop())
            self.liquid_count -= 1
            other.liquid_count += 1
            ret += 1
        
        while (not self.is_empty()) and (not other.is_full()) and (self[-1] == other[-1]):
            other.liquid.append(self.liquid.pop())
            self.liquid_count -= 1
            other.liquid_count += 1
            ret += 1
        return ret

    def is_empty(self) -> bool:
        return (self.liquid_count == 0)
    
    def is_full(self) -> bool:
        return (self.liquid_count == 4)
    
    def is_finished(self) -> bool:
        if self.is_empty():
            return True
        if not self.is_full():
            return False
        for each in self.liquid:
            if each != self.liquid[0]:
                return False
        return True
    
class Scence:
    __slots__ = ["tubes","tube_num","history","squence"]
    def __init__(self,num:int):
        '''Create a scence with num tubes'''
        if not isinstance(num,int):
            raise TypeError(f"Scence musted be init with int, but {type(num)}")
        if num < 3:
            raise ValueError(f"Scence musted be init with number bigger than 2, but {num}")
        
        self.tube_num = num
        self.squence = list()
        for i in range(num - 2):
            self.squence.extend([i for j in range(4)])
        shuffle(self.squence)
        self.set_tubes()

        self.history = list()

    def set_tubes(self):
        self.tubes = list()
        for i in range(self.tube_num - 2):
            self.tubes.append(Tube(self.squence[i*4:i*4+4]))
        self.tubes.append(Tube())
        self.tubes.append(Tube())

    def replay(self):
        self.set_tubes()
        self.history = ()

    def __repr__(self):
        result = ""
        count = 0
        for each in self.tubes:
            result += f"{count}: {each}\n"
            count += 1
        return result

    def solution(self):
        '''Return the solution of the scence'''
        pass

    def move(self,source:int,dest:int):
        '''Move liquid from souce tube to dest tube'''
        if not isinstance(source,int) or not isinstance(dest,int):
            raise TypeError(f"Source and dest must be int, but {type(source)} and {type(dest)}")
        if source < 0 or source >= self.tube_num or dest < 0 or dest >= self.tube_num:
            raise ValueError(f"Source and dest must between 0 to {self.tube_num - 1}, but {source} and {dest}")
        move_num = self.tubes[source] + self.tubes[dest]
        if move_num != 0:
            self.history.append(Record(source,dest,move_num))

    def redo(self):
        '''Redo last move'''
        if(len(self.history) == 0):
            return
        history = self.history.pop()
        source = self.tubes[history.source]
        dest = self.tubes[history.dest]
        source.liquid_count += history.num
        dest.liquid_count -= history.num

        for i in range(history.num):
            source.liquid.append(dest.liquid.pop())

    def is_finished(self) -> bool:
        '''Return True if the scence is finished'''
        for each in self.tubes:
            if not each.is_finished():
                return False
        return True
    
class Record:
    __slots__ = ['source','dest','num']
    def __init__(self,source:int,dest:int,num:int):
        '''
        Record of move history
        source:liquid from which tube
        dest:liquid move to which tube
        num:move number of liquid
        '''
        if not isinstance(source,int):
            raise TypeError(f"Source of record must be int, but get {type(source)}")
        if not isinstance(dest,int):
            raise TypeError(f"Dest of record must be int, but get {type(dest)}")
        if not isinstance(num,int):
            raise TypeError(f"Num of record must be int, but get {type(num)}")
        self.source = source
        self.dest = dest
        self.num = num
    
def ignore():
    pass
    
class Button(pygame.sprite.Sprite):
    __slots__ = ['image','rect','func','base']
    def __init__(self,image:Path|pygame.Surface,position:tuple[int],base:Path,func=ignore):
        '''
        表示按钮的类
        image:图标,文件的存放位置或对应Surface对象
        rect:按钮的位置
        base:根目录
        func:按钮被点击时执行的函数,默认什么都不做
        '''
        if isinstance(image,(str,Path)):
            self.image = pygame.image.load(image)
            #根据图片类型进行转换
            try:
                self.image.convert_alpha()
            except:
                self.image.convert()
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = position
        self.base = base
        self.func = func
        pygame.sprite.Sprite.__init__(self)
        self.mask = pygame.mask.from_surface(self.image)


    def check(self) -> bool:
        '''
        检查鼠标是否在按钮上
        '''
        posi = pygame.mouse.get_pos()
        collide_point = Button(self.base/"collide_point.png",posi,None)
        return pygame.sprite.collide_mask(self,collide_point)
