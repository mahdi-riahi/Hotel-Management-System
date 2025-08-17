import pandas as pd
from Room import room_maker,RoomStatus
from Guest import Guest,GuestStatus
from Hotel import Hotel
from datetime import datetime

def save(hotel):
    data_room={
        "number": [],
        "type": [],
        "beds": [],
        "cost": [],
        "status": [],
        "available_time": []
    }
    for room in hotel.room_list:
        data_room["number"].append(room.number)
        data_room["type"].append(room.type)
        data_room["beds"].append(room.beds)
        data_room["cost"].append(room.cost)
        data_room["status"].append(room.status)
        data_room["available_time"].append(
            room.available_time.isoformat() if room.available_time else None
        )
        
    data_guest = {
        "name": [],
        "ID_code": [],
        "count": [],
        "status": [],
        "room_number": [],
        "time_in": [],
        "time_out": [],
        "extra_charge": []
    }
        
    for guest in hotel.guest_list:
        data_guest["name"].append(guest.name)
        data_guest["ID_code"].append(guest.ID_code)
        data_guest["count"].append(guest.count)
        data_guest["status"].append(guest.status)
        data_guest["room_number"].append(
            guest.room.number if guest.room else None
        )
        data_guest["time_in"].append(
            guest.time_in.isoformat() if guest.time_in else None
        )
        data_guest["time_out"].append(
            guest.time_out.isoformat() if guest.time_out else None
        )
        data_guest["extra_charge"].append(guest._extra_charge)

        hotel_data = {
            "hotel_name": [hotel.name],
            "hotel_address": [hotel.address],
            "hotel_type": [hotel.type],
            "services": [",".join(hotel.services)]
        }

        filename = f"{hotel.name.replace(' ', '_')}.xlsx"
        with pd.ExcelWriter(filename) as writer:
            pd.DataFrame(data_room).to_excel(writer, sheet_name="rooms", index=False)
            pd.DataFrame(data_guest).to_excel(writer, sheet_name="guests", index=False)
            pd.DataFrame(hotel_data).to_excel(writer, sheet_name="hotel", index=False)
        

def load(hotel:Hotel):
    
    filename = f"{hotel.name.replace(' ', '_')}.xlsx"
    df_hotel=pd.read_excel(filename,sheet_name="hotel")
    df_room=pd.read_excel(filename,sheet_name="rooms")
    df_guest=pd.read_excel(filename,sheet_name="guests")
    
    df_hotel = pd.read_excel(filename, sheet_name="hotel")
    hotel._name = df_hotel["hotel_name"][0]
    hotel._address = df_hotel["hotel_address"][0]
    hotel._type = df_hotel["hotel_type"][0]
    hotel._services = df_hotel["services"][0].split(",")
         
    data_room=df_room.to_dict("split")["data"]      # 'split' method gives keys(index,columns,data) & values(lists in a list)
    for room in data_room:
        room_obj=room_maker(room[1],room[0],room[2])
        room_obj.cost=room[3]
        room_obj.status=room[4]
        room_obj.available_time=datetime.fromisoformat(room[5]) if pd.notna(room[5]) else None
        #I will use hotel's _protected variables in order to keep current status. and I didn't use hotel.add_room() because it changes room's status. Same thing happens with guest
        hotel._room_list.append(room_obj)

    data_guest=df_guest.to_dict("split")["data"]
    for guest in data_guest:
        guest_obj=Guest(guest[0],guest[1],guest[2])
        guest_obj.status=guest[3]
        guest_obj.room=hotel.find_room(guest[4])
        guest_obj.time_in=datetime.fromisoformat(guest[5]) if pd.notna(guest[5]) else None
        guest_obj.time_out=datetime.fromisoformat(guest[6]) if pd.notna(guest[6]) else None
        guest_obj._extra_charge=guest[7]
        hotel._guest_list.append(guest_obj)
