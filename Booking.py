from datetime import datetime,timedelta
from Room import RoomStatus
from Guest import Guest,GuestStatus
from Hotel import Hotel

class BookingError(Exception):
    pass

class Booking:
    def __init__(self,hotel:Hotel,guest:Guest,room):
        self.hotel=hotel
        self.guest=guest
        self.room=room
    
    def validate_reservation(self):
        if self.guest not in self.hotel.guest_list:
            raise BookingError("Guest not registered in hotel")
        if self.guest.status != GuestStatus.REGISTERED.value:
            raise BookingError("Guest status not suitable for reservation")
        if self.room not in self.hotel.room_list:
            raise BookingError("Room not part of this hotel")
        if self.room.status != RoomStatus.AVAILABLE.value:
            raise BookingError("Room is not available")
        if self.room.beds < self.guest.count:
            raise BookingError("Room capacity insufficient for guest count")
    
    def validate_check_out(self):
        if self.guest not in self.hotel.guest_list:
            raise BookingError("Guest not registered in hotel")
        if self.guest.status != GuestStatus.CHECKED_IN.value:
            raise BookingError("Guest has not checked in")
        if self.room.status!=RoomStatus.OCCUPIED.value:
            raise BookingError("Room not occupied")
        if self.guest.room != self.room:
            raise BookingError("Room not occupied by this guest")
    
    def reserve(self,check_in_time:datetime):                      #reserve_room
        try:
            self.validate_reservation()
            
            self.room.status=RoomStatus.RESERVED.value
            self.guest.status=GuestStatus.RESERVED.value
            self.guest.room=self.room               #so there is no need for check in validate_check_out
            self.guest.time_in=check_in_time
            
            self.guest.inform(
                f"Reservation for Room {self.room.number} was successfull.\n"
                f"Room will be ready for you at : {check_in_time}.")
            
            return (True,
                    f"Guest : {self.guest.name} , Room : {self.room.number}\n"
                    f"Reservation time : {datetime.now()}\n"
                    f"Room reserved for : {check_in_time}"
            )
        
        except BookingError as e:
            return (False,str(e))


    def check_out(self):                                #clear_room
        try:
            self.validate_check_out()

            total_charges=self.guest.total_charges
            self.guest.pay(total_charges)
            self.room.status=RoomStatus.OUT_OF_SERVICE.value
            self.guest.time_out=datetime.now()
            self.room.available_time= self.guest.time_out + timedelta(hours=1)
            self.guest.room=None
            self.guest.status=GuestStatus.CHECKED_OUT.value
            self.hotel.remove_guest(self.guest)
            
            return (True,
                    f"Guest : {self.guest.name} , Room : {self.room.number}\n"
                    f"Guest cleared the room at : {self.guest.time_out}\n"
                    f"Time in : {self.guest.time_in} , Time out {self.guest.time_out}\n"
                    f"Total charges : ${total_charges} , successfully paid"
            )
        
        except BookingError as e:
            return False,str(e)



def free_bar(func):                             #decorator
    def wrapper(booking,*args,**kwargs):
        booking.guest.add_extra_charge(1000)
        print("Congradulations!\nFree Bar Services activated for you (cost only $1000)")
        return func(booking,*args,**kwargs)
    return wrapper

class FreeBarBooking(Booking):                  #subclass with decorator          
    @free_bar
    def reserve(self, time_in):
        return super().reserve(time_in)
    
class NormalBooking(Booking):
    pass

class BookingFactory:
    @staticmethod
    def create_booking(booking_type,hotel,guest,room):
        booking_classes={
            "freebarbooking":FreeBarBooking,
            "normalbooking":NormalBooking
        }

        if booking_type not in booking_classes:
            raise TypeError(f"Invalid booking type. Valid types: {booking_classes}")
        return booking_classes[booking_type](hotel,guest,room)