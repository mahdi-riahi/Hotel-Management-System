#سیستم مدیریت هتل: طراحی یک سیستم برای مدیریت اتاق ها. مهمانان. رزروها و خدمات هتل به کمک شی گرایی
from datetime import datetime
from enum import Enum
class RoomStatus(Enum):
    AVAILABLE="available"
    RESERVED="reserved"
    OCCUPIED="occupied"
    OUT_OF_SERVICE="out-of-service"

class Room:
    def __init__(self,number,room_type,beds):
        self._number=number
        self._type=room_type
        self._beds=beds
        self._cost=self.calculate_cost()                       #Dollor
        self._status=RoomStatus.AVAILABLE.value                #available , reserved , occupied , out-of-service --> available,...
        self._available_time=None
    
    def calculate_cost(self):
        if self._type=="VIP-Room":
            return self._beds * 100
        elif self._type=="Suit":
            return self._beds * 85
        elif self._type=="Standard-Room":
            return self._beds * 75
        raise ValueError("Invalid room type. Valid types: VIP-Room / Suit / Standard-Room")

    @property
    def number(self):
        return self._number
    @property
    def type(self):
        return self._type
    @property
    def beds(self):
        return self._beds
    @property
    def cost(self):
        return self._cost
    @cost.setter
    def cost(self,value):
        if value<0:
            raise ValueError("Cost must be positive")
        self._cost=value
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self,value):
        valid_statuses=[status.value for status in RoomStatus]
        if value in valid_statuses:
            self._status=value 
        else:
            raise ValueError(f"Invalid room status. Valid statuses: {valid_statuses}")

    @property
    def available_time(self):
        return self._available_time
    
    @available_time.setter
    def available_time(self,value):
        if not isinstance(value,datetime):
            raise ValueError("Available time must be datetime type")
        self._available_time=value


class VIPRoom(Room):                            #subclass
    def __init__(self, number, beds):
        super().__init__(number, "VIP-Room",beds)

class Suit(Room):                               #subclass
    def __init__(self, number, beds):
        super().__init__(number, "Suit", beds)

class StandardRoom(Room):                       #subclass
    def __init__(self, number, beds):
        super().__init__(number, "Standard-Room",beds)


def room_maker(room_type,number,beds):                          #factory
    room_classes={
        "VIP-Room":VIPRoom,
        "Suit":Suit,
        "Standard-Room":StandardRoom
    }
    if beds>5 or beds<1:
        raise ValueError("Beds must be between 1,5")
    if room_type not in room_classes:
        raise ValueError("Invalid room type. Valid types: VIP-Room / Suit / Standard-Room")
    return room_classes[room_type](number,beds)