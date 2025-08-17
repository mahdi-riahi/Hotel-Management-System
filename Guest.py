from datetime import datetime
from enum import Enum
class GuestStatus(Enum):
    REGISTERED="registered"
    RESERVED="reserved"
    CHECKED_IN="checked-in"
    CHECKED_OUT="checked-out"

class Guest:
    def __init__(self,name,ID_code,count):
        self._name=name
        self._ID_code=ID_code
        self._count=count
        self._status=GuestStatus.REGISTERED.value
        self._room=None
        self._base_charge=0         #extra charges
        self._extra_charge=0        #staying charges
        self._time_in=None
        self._time_out=None
    
    @property
    def name(self):
        return self._name
    
    @property
    def ID_code(self):
        return self._ID_code
    
    @property
    def count(self):
        return self._count
    
    @count.setter
    def count(self,value):
        if not isinstance(value,int) or not (1 <= value <= 5):
            raise ValueError("Guest count must be integer and between 1-5")
        self.count=value

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self,value):
        valid_statuses=[status.value for status in GuestStatus]
        if value not in valid_statuses:
            raise ValueError(f"Invalid guest status. Valid statuses: {valid_statuses}")
        self._status=value

    @property
    def room(self):
        return self._room
    
    @room.setter
    def room(self,value):
        if not self._room:
            self._room=value

    @property
    def time_in(self):
        return self._time_in
    
    @time_in.setter
    def time_in(self,value):
        if not isinstance(value,datetime):
            raise TypeError("time_in must be a datetime object")
        self._time_in=value

    @property
    def time_out(self):
        return self._time_out
    
    @time_out.setter
    def time_out(self,value):
        if not isinstance(value,datetime):
            raise TypeError("time_in must be a datetime object")
        self._time_out=value

    def add_extra_charge(self,amount):
        if amount<0:
            raise ValueError("Charge amout must be positive")
        self._extra_charge += amount

    def calc_stay_charge(self):
        end_time=self._time_out or datetime.now()
        if not self._time_in or not self._room or not (end_time > self._time_in):
            return 0
        stay_duration = end_time - self.time_in
        days=max(1,stay_duration.days)
        return days * self._room.cost
    
    @property
    def total_charges(self):
        stay_charge=self.calc_stay_charge()
        return stay_charge + self._extra_charge
    
    def pay(self,amount):
        if amount<=0:
            raise ValueError("Charge amount must be positive")
        if amount>self.total_charges:
            raise ValueError("Payment exceeds total charges")
        print(f" ${amount} payment received from {self._name}")
        if amount>=self.total_charges:                      #if payment is completed ---> guest status changes to checked out
            self._status=GuestStatus.CHECKED_OUT.value
        
    def inform(self,message):                           #observer (sending messages)
        print(f"\n******GUEST NOTIFICATION: {self._name}******")
        print(message)
        print("************************")