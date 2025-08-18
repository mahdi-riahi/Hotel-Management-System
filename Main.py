from Room import room_maker,VIPRoom
from Guest import Guest,GuestStatus
from Hotel import Hotel,HotelFactory
from Booking import BookingFactory,Booking
from Save_Load import save,load
from datetime import datetime
import os


def clear_screen():
    os.system("cls" if os.name=="nt" else "clear")

def choose_hotel():
    print("=============HOTEL CHOOSE=============")
    action=input(
        "1. Alighapu Hotel\n"
        "2. Naghshe Jahan Hotel\n"
        "3. Dariushe Kabir Hotel\n"
        "4. Create Custom Hotel\n"
        "0. Exit program\n"
        "   Enter your choice: ")
    clear_screen()
    
    if action == "0":
        return "exit"

    hotel_dict={
        "1":"alighapu",
        "2":"naghshejahan",
        "3":"dariushekabir"
    }
    hotel_type=hotel_dict.get(action)
    if hotel_type:
        try:
            return HotelFactory.create_hotel(hotel_type)
        except Exception as e:
            print(f"ERROR hotel creating:{e}")

    if action =="4":
        star=input("5star: 5 Star Hotel\n"
                   "7star: 7 Star Hotel\n"
                   "Enter your choise:\n")
        name=input("Enter name of the hotel: ")
        address=input("Enter address of the hotel: ")
        try:
            return HotelFactory().create_hotel(star,name,address)
        except Exception as e:
            print(f"ERROR star selection for hotel: {e}")

    print("Invalid selection")
    return None

def create_guest(hotel):
    name=input("please enter your name: ")
    id_code=input("please enter your id code: ")
    try:
        count=int(input("please enter number of guests (1-5): "))
        if not (0<count<6):
            raise ValueError("Guest count must be between 0,6")
        guest=Guest(name,id_code,count)
        hotel.add_guest(guest)
        print("Guest registeration successful! You can log in now.")
        return guest

    except Exception as e:
        print(f"Guest registeration failed. Error creating guest: {e}")
        return None
    
def log_in_guest(hotel):
    name=input("please enter your name: ")
    id_code=input("please enter your id code: ")
    for guest in hotel.guest_list:
        if guest.name==name and guest.ID_code==id_code: 
            print("Guest login successfull.")
            return guest
    print("Invalid name or id code")
    return None

def reserve_room(guest,hotel):
    print("\nAvailable Rooms:\n")
    hotel.show_rooms_available()
    choice=input(
        "\nEnter room number\n"
        "or '1' to create a custom room\n"
        "or '0' to cancel\n"
        "Your choice: "
    )
    clear_screen()

    if choice=="0":
        return 
    
    if choice=="1":
        room_type=input("Enter type of the room ('VIP-Room' or 'Suit' or 'Standard-Room') : ")
        beds=input("Enter number of beds (1-5) : ")
        number=input("Enter a number for this room (ex: A45) : ")
        try:
            room=room_maker(room_type,number,int(beds))
            hotel.add_room(room)
            print("Custom room created successfully. You can reserve it from the previous menu.")
        except Exception as e:
            print(f"Error creating custom room: {e}")
        return


    booking_type=input(
        "1. Free bar booking (+$1000)\n"
        "2. Normal booking\n"
        "Your choice: ")
    booking_type="freebarbooking" if booking_type=="1" else "normalbooking"

    room=hotel.find_room(choice)
    if room:
        try:
            time_in_str=input("Enter your check-in time (YYYY-MM-DD HH:MM): ")
            time_in=datetime.strptime(time_in_str,"%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid format for date. use YYYY-MM-DD HH:MM")
            return 
            
        try:
            booking=BookingFactory().create_booking(booking_type,hotel,guest,room)
            success,message=booking.reserve(time_in)
            print(message)
        except Exception as e:
            print(f"Reservation Failed. Error: {e}")
    else:
        print("Invalid room selection")
        return

def check_out_guest(guest,hotel):
    if not guest.room:
        print("You dont have an active reservation")
        return
    try:
        success,message=Booking(hotel,guest,guest.room).check_out()
        print(message)
    except Exception as e:
        print(f"check-out failed. Error: {e}")


def guest_menu(guest,hotel):
    while True:
        print(f" ^^^^^^^ NAME: {guest.name} ^^^^^^^ STATUS: {guest.status} ^^^^^^^ HOTEL : {hotel.name}  ^^^^^^^ TOTAL CHARGES (SO FAR):{guest.total_charges} ^^^^^^^ ")
        action=input(
            "1. See all rooms \n"
            "2. Reserve a room\n"
            "3. Check out\n"
            "4. View my charges\n"
            "0. LOG OUT\n"
            "   ^^^^^^^^^^^^^^^\n"
            "   Enter your responce: ")
        clear_screen()
        hotel.update()

        if action=="1":                                               #show_all_rooms_of_the_hotel
            hotel.show_rooms()

        elif action=="2":                                               #reserve
            reserve_room(guest,hotel)

        elif action=="3":                                               #clear_room
            check_out_guest(guest,hotel)

        elif action=="4":                                               #see pay check
            paycheck = guest.total_charges
            print(f"Your pay check so far equals ${paycheck}")

        elif action=="0":
                break

        else:
            print("Invalid selection")

def admin_menu(hotel):
    print("----------------Welcome Admin!----------------\n")
    while True:
        print(f"--------------{hotel.name} Administration---------------")
        action=input(
            "1. Add new guests\n"
            "2. Add rooms\n"
            "3. Add services\n"
            "4. View guests\n"
            "5. View rooms\n"
            "0. LOG OUT\n"
            "   ^^^^^^^^^^^^^^^\n"
            "   Enter your responce: ")
        clear_screen()
        hotel.update()

        if action=="1":                                                     #add guest
            create_guest(hotel)

        elif action=="2":                                                     #add room
            room_type=input("Enter type of the room ('VIP-Room' or 'Suit' or 'Standard-Room') : ")
            beds=input("Enter number of beds (1-5) : ")
            number=input("Enter a number for this room (ex: A45) : ")
            try:
                room=room_maker(room_type,number,int(beds))
                hotel.add_room(room)
                print("Room added successfully.")

            except Exception as e:
                print(f"ERROR adding room: {e}")

        elif action=="3":                                                     #add services
            service=input("Enter service you want to add to hotel : ")
            hotel.add_service(service)
            print(f"Service {service} added successfully")

        elif action=="4":                                                     #see guests information
            print("\n=====Guests=====")
            for guest in hotel.guest_list:
                room_info=f"Room {guest.room.number}" if guest.room else "No room"
                print(f"{guest.name} | ID: {guest.ID_code} | COUNT: {guest.count} | STATUS: {guest.status} | CHARGES ${guest.total_charges} | {room_info}")
        
        elif action=="5":                                                     #see rooms information
            print("\n=====Rooms=====")
            for room in hotel.room_list:
                print(f"Room: {room.number} | Type: {room.type} | Beds: {room.beds} | Cost: ${room.cost}/day | Status: {room.status}")

        elif action=="0":
            break

        else:
            print("Invalid Selection")


def main():
    print("=============WELCOME TO HOTEL RESERVATION CENTER=============")
    while True:
        hotel=choose_hotel()

        if hotel=="exit":
            #END OF PROGRAM
            break

        if not hotel:
            continue

        try:
            load(hotel)         #LOADING DATA FROM EXCEL FILE FOR THE SPICIFIC HOTEL
            print("Data loaded successfully")
        except Exception as e:
            print(f"Error loading data: {e}")

        while True:
            print(f"|    ||   |||  |||| |||||    {hotel.name} ========== Address:{hotel.address}    ||||| ||||  |||   ||    |")
            action=input(
                "1. Guest login\n"
                "2. Administrator login\n"
                "0. Select another hotel\n"
                "Please Enter your choice: ")
            clear_screen()
            hotel.update()

            if action=="0":
                try:
                    save(hotel)
                    print("Data saved successfully")
                except Exception as e:
                    print(f"Error saving datas: {e}")
                break

            if action=="1":                                             #guest log in / sign up
                sub_action=input(
                    "1. LOG IN\n"
                    "2. REGISTER\n"
                    "0. Back\n"
                    "   Enter your choice: ")
                clear_screen()
                hotel.update()

                if sub_action=="0":
                    continue
                
                if sub_action=="1":                                            #guest log in
                    guest=log_in_guest(hotel)
                    
                elif sub_action=="2":
                    guest=create_guest(hotel)

                else:
                    print("Invalid choice")
                    continue

                if guest:
                    guest_menu(guest,hotel)
            

            elif action=="2":                                           #adminstrator
                password=input("Enter admin's password for Hotel: ")
                if hotel.verify_admin_pass(password):
                        print("ADMINSTRATION LOG IN SUCCESSFUL")
                        admin_menu(hotel)
                else:
                    print("Invalid password. Administration login failed.")

            else:
                print("Invalid selection")

    print("=============GOOD BYE=============")

main()

