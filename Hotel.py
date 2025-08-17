from datetime import datetime
import hashlib
from Guest import GuestStatus
from Room import RoomStatus


class Hotel:
    def __init__(self):
        self._name=None
        self._address=None
        self._type=None
        self._services=[]
        self._room_list=[]
        self._guest_list=[]
        self.__admin_pass=None

    def set_admin_pass(self,password):
        self.__admin_pass=hashlib.sha256(password.encode()).hexdigest()

    def verify_admin_pass(self,password):
        return self.__admin_pass==hashlib.sha256(password.encode()).hexdigest()
    
    @property
    def name(self):
        return self._name
    
    @property
    def address(self):
        return self._address

    @property
    def type(self):
        return self._type
    
    @property
    def services(self):
        return self._services
    
    @services.setter
    def services(self,services_list):
        if not isinstance(services_list,list):
            raise TypeError("Service list must be a list")
        self.services=services_list
    
    def add_service(self,service):
        if service not in self._services:
            self._services.append(service)


    @property
    def room_list(self):
        return self._room_list
    
    def add_room(self,room_obj):
        if room_obj not in self._room_list:
            self._room_list.append(room_obj)
            room_obj.status="available"
    
    @property
    def guest_list(self):
        return self._guest_list
    
    def add_guest(self,guest_obj):
        if guest_obj not in self._guest_list:
            self._guest_list.append(guest_obj)
            guest_obj.status="registered"

    def remove_guest(self,guest_obj):
        if guest_obj in self._guest_list:
            self._guest_list.remove(guest_obj)

    def find_room(self,number):
        for room in self._room_list:
            if room.number==number:
                return room
        return None

    def show_rooms(self):
        for room in self.room_list:
            print(f"Room : {room.number} | Status : {room.status} | Beds : {room.beds} | Type : {room.type} | Cost : ${room.cost}" )

    def show_rooms_available(self):
        for room in self.room_list:
            if room.status==RoomStatus.AVAILABLE.value:
                print(f"Room : {room.number} | Status : {room.status} | Beds : {room.beds} | Type : {room.type} | Cost : ${room.cost}")

    def update(self):
        for guest in self.guest_list:
            if guest.room:
                if all([guest.time_in <= datetime.now() , guest.status==GuestStatus.RESERVED.value , guest.room.status==RoomStatus.RESERVED.value]):
                    guest.status=GuestStatus.CHECKED_IN.value
                    guest.room.status=RoomStatus.OCCUPIED.value
                    guest.inform(f"Dear {guest.name}! Your room is ready")
        
        for room in self.room_list:
            if room.status==RoomStatus.OUT_OF_SERVICE.value and room.available_time < datetime.now():
                room.status=RoomStatus.AVAILABLE.value
                room.available_time=None
                for guest in self.guest_list:
                    if guest.status==GuestStatus.REGISTERED.value and guest.count <= room.beds:
                        guest.inform(f"Dear {guest.name}! Room {room.number} is availble for you.")


class StarHotel(Hotel):                             #Star Hotels base class
    def __init__(self,name,address,star_rating):
        super().__init__()
        self._name=name
        self._address=address
        self._star_rating=star_rating
        self._type=f"{star_rating}-Star Hotel"

class Isfahan5StarHotel(StarHotel):                 #subclass
    def __init__(self,name,address):
        super().__init__(name,address,5)
        self._services=["Laundry","Breakfast","Cafe","Restuarant","Pool","Night-Services"]
        self.set_admin_pass("I5S")

class Tehran7StarHotel(StarHotel):                  #subclass
    def __init__(self,name,address):
        super().__init__(name,address,7)
        self._services=["Laundry","Breakfast","Lunch","Dinner","Free Cafe","Restaurant","Pool","Night-Services"]
        self.set_admin_pass("T7S")


class Singleton:                                    #Singleton base class and pattern
    _instances={}

    def __new__(cls,*args,**kwargs):
        if cls not in cls._instances:
            instance=super().__new__(cls)
            cls._instances[cls]=instance
        return cls._instances[cls]

class Alighapu(Singleton,Isfahan5StarHotel):                  #singleton
    def __init__(self):
        if not hasattr(self,"_name"):                         #stopping from writing again
            super().__init__("Hotel Alighapu","Iran , Isfahan , Charbagh-Abbasi St.")
            self._services=["Laundry","Breakfast","Lunch","Dinner","Free Cafe","Restaurant","Pool","Night-Services"]
            self.set_admin_pass("AG")

class NaghsheJahan(Isfahan5StarHotel,Singleton):          #singleton
    def __init__(self):
        if not hasattr(self,"_name"):
            super().__init__("Hotel Naghsh-e-Jahan","Iran , Isfahan , Neshat St.")
            self._star_rating=6
            self._type="6 Star Super Hotel"
            self._services=["Breakfast","Lunch","Dinner","Free Cafe","Restaurant","Pool","Night-Services"]
            self.set_admin_pass("NJ")

class DariusheKabir(Tehran7StarHotel):          #singleton
    def __init__(self):
        if not hasattr(self,"_name"):
            super().__init__("Hotel Dariush-e-Kabir","Iran , Tehran , Tagrish St.")
            self._services=["Laundry","Breakfast","Lunch","Dinner","Restaurant","Pool","Night-Services","Mall","Gim"]
            self.set_admin_pass("DK")

class HotelFactory:                               #factory
    @staticmethod
    def create_hotel(hotel_type,*args):
        hotels={
            "alighapu":Alighapu,
            "naghshejahan":NaghsheJahan,
            "dariushekabir":DariusheKabir,
            "5star":Isfahan5StarHotel,
            "7star":Tehran7StarHotel
        }
        hotel_type=hotel_type.lower()
        if hotels.get(hotel_type):
            return hotels.get(hotel_type)(*args)
        raise TypeError(f"Invalid hotel type. Valid types: {hotels.keys()}")

