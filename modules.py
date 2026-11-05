from abc import ABC,abstractmethod
from exception import Invalid_status_Change

# from collections import defaultdict
# from datetime import date,datetime,timedelta
# import csv

# room_available=defaultdict(list)
# room_numbers=set()
# today=datetime.today()
# Booking_id=1

# with open("room.csv","r") as file:
#     reader=csv.DictReader(file)
#     for row in reader:
#         try:
#             room_no = row["room_no"].strip()
#             if not room_no or room_no in room_numbers:
#                 raise ValueError("Room number cannot be empty .")
#             room_type = row["room_type"].strip()
#             if not room_type or room_type not in ("Standard","Deluxe","Suite"):
#                 raise ValueError("room_type must be (Standard,Deluxe,Suite)")
#             floor = row["floor"].strip()
#             if not floor:
#                 raise ValueError("floor cannot be empty")
      
#             room_available[room_type].append({
#                 "room_no":room_no,
#                 "floor":floor,
#                 "status":"available"
#             })
#             room_numbers.add(room_no)
#         except ValueError as e:
#             with open ("errors.log","a") as error:
#                 error.write(str(e)+"\n")
            
class Room(ABC):
    def __init__(self,room_no,room_type,floor):
        self.room_type=room_type
        self.room_no=room_no
        self.floor=floor
        self.lock="available"

    @abstractmethod
    def get_tariff(self):
        pass
    @abstractmethod
    def guest_charges(self,no_guest):
        pass
    @abstractmethod
    def cost_breakfast(self,no_guest,breakfast):
        pass
    @abstractmethod
    def maximum_guests(self):
        pass
    def __str__(self):
        return f"Room no:{self.room_no},type:{self.room_type}"
    

class StandardRoom(Room):
    def get_tariff(self):
        return 2500
    def guest_charges(self,no_guest):
        return 0
    def cost_breakfast(self,no_guest,breakfast):
        if breakfast:
            return 350*no_guest
        return 0
    def maximum_guests(self):
        return 2

class Deluxe(Room): 

    def get_tariff(self):
        return 4000
    def guest_charges(self,no_guest):
        if no_guest<=2:
            charge =0
        else :
            guest=no_guest-2
            charge= guest*800
        return charge
    def cost_breakfast(self,no_guest,breakfast):
        return 0
    def maximum_guests(self):
        return 3

class Suite(Room):   
    def get_tariff(self):
        return 7500
    def guest_charges(self,no_guest):
        if no_guest<=2:
            charge =0
        else :
            guest=no_guest-2
            charge= guest*800
        return charge
    def cost_breakfast(self,no_guest,breakfast):
        return 0
    def maximum_guests(self):
        return 4


class Booking_room():
    def __init__(self,booking_id,guest,room,check_in,check_out):
        self._booking_id=booking_id
        self._guest=guest
        self._room=room
        self._check_in=check_in
        self._check_out=check_out
        self._status="confirmed"
        self._total=0
        self._amount_paid=0
        self._refund=0

    def get_booking_id(self):
        return self._booking_id
    def get_guest(self):
        return self._guest
    def get_room(self):
        return self._room
    def get_check_in(self):
        return self._check_in
    def get_check_out(self):
        return self._check_out
    def get_status(self):
        return self._status
    def set_total(self,amount):
        self._total=amount
    def get_total(self):
        return self._total
    def set_amount_paid(self,amount):
        self._amount_paid=amount
    def get_amount_paid(self):
        return self._amount_paid
    def set_refund(self,amount):
        self._refund=amount
    def get_refund(self):
        return self._refund
    def change_status(self,new_status):
        if self._status=="confirmed":
            if new_status=="checked_in" or new_status=="cancelled":
                self._status=new_status
            else:
                raise Invalid_status_Change("Invalid status change")
        elif self._status=="checked_out":
            if new_status=="checked_out":
                self._status=new_status
            else:
                raise Invalid_status_Change("Invalid status chenge")
        else:
            raise Invalid_status_Change("Booking cannot be changed")

    def __str__(self):
        return f"Booking_id : {self._booking_id} guest : {self._guest.get_name()}, room:{self._room.room_no} status:{self._status}"
        


    def __str__(self):
        return f"bookig_id : {self._booking_id} guest : {self._guest} check_in :{self._check_in} check_out : {self._check_out} status : {self._status}"

class Guest():
    def __init__(self,name,mobile_number,email,no_of_guests):
        self._name=name
        self._mobile_number=mobile_number
        self._email=email
        self._no_of_guests=no_of_guests

    def get_name(self):
        return self._name
    def get_mobile_number(self):
        return self._mobile_number
    def get_email(self):
        return self._email
    def get_no_of_guest(self):
        return self._no_of_guests
    def __str__(self):
        return f"Guest name : {self.name}, mobile_number : {self.mobile_number} ,email : {self.email} ,no_of_guest : {self.no_of_guests}"

# def get_booking_dates():
#     while True:
#         check_in=input("Enter check-in date (DD-MM-YYYY) :").strip()
#         try:
#             check_in=datetime.strptime(check_in,"%d-%m-%Y").date()
#         except ValueError:
#             print("Invalid check-in  date ")
#             continue
#         if check_in<today:
#             print("check in cannot be in the past ")
#         if check_in>today+timedelta(days=180):
#             print("check - in must be with in180 days")
#         break
#     while True:
#         check_out=input("enter your check out time ").strip()
#         try :
#             check_out=datetime.strptime(check_out,"%d-%m-%Y").date()
#         except ValueError:
#             print("Invalid check-out date")
#         if check_out<=check_in:
#             print("check-out must be after check-in.")

#         nights=(check_out-check_in).days
#         if nights>30:
#             print("maximum 30 nights are allowed")
#             continue
#         break
#     return check_in,check_out


# def create_booking():
#     global Booking_id
#     while True:
#         name=input("Enter the guest name .").strip()
#         if not name:
#             print("empty name cannot be taken .")
#         else:
#             break
#     while True:
#         mobile_number=input("Enter the Mobile number .").strip()
#         if not mobile_number:
#             print("Enter the mobile number .")
#         elif (len(mobile_number)!=10 or
#             not mobile_number.isdigit() or 
#             mobile_number[0] not in ("6789")):
#             print("Check your mobile number .")
#         else:
#             break
#     while True:
#         email=input("Enter your email .").strip()
#         if not email:
#             print("Enter your email address It cannot be empty.")
#         elif not email.endswith("@gmail.com"):
#             print("This is not valid email address.")
#         else:
#             break
#     while True:
#         no_of_guests=int(input("enter the no of guests"))
#         if not no_of_guests or no_of_guests<=0:
#             print("enter the no_of_guests")
#         else:
#             break

#     while True:
#         try:
#             no_of_guests=int(input("enter number of guests: "))
#             if no_of_guests<=0:
#                 print("enter count must be grater than zero")
#             else:
#                 break
#         except ValueError:
#             print("enter the hole number")

#     guest=Guest(name,mobile_number,email,no_of_guests)
#     while True:
#         room_type=input("enter the roo type (Standard,Deluxe,Suite)").strip().capitalize()
#         if room_type not in ("Standard","Delux","Suite"):
#             print("Invalid room type")
#         else:
#             break

#     if room_type=="Standard":
#         standar_room=StandardRoom("0",room_type,"0")
#         if no_of_guests>standar_room.maximum_guests():
#             print("standard room allows 2 guests")
#     elif room_type == "Delux":
#         deluxe_room=Deluxe("0",room_type,"0")
#         if no_of_guests > deluxe_room.maximum_guests():
#             print("deluxe room can allows 3 guests")
#     elif room_type== "Suite":
#         suite_room=Suite("0",room_type,"0")
#         if no_of_guests>suite_room.maximum_guests():
#             print("suite can allow 4 guests")
#     check_in,check_out=get_booking_dates()

#     available_room=[]
#     for row in room_available["room_type"]:
#         if row["status"]=="available":
#             available_room.append(row)
#     if not available_room:
#         print("no room available")
#     available_room.sort(key=lambda row:int(row["room_no"]))

#     selected_room=available_room[0]
#     room_no=selected_room["room_no"]
#     floor=selected_room["floor"]

#     if room_type=="Standard":
#         room=StandardRoom(room_no,room_type,floor)

#     elif room_type=="Delux":
#         room=Deluxe(room_no,room_type,floor)
#     else:
#         room=Suite(room_no,room_type,floor)
#     booking_id=f"BK{booking_id:4d}"
#     booking=Booking_room(booking_id,guest,room,check_in,check_out)
#     selected_room["status"]="booked"
#     booking_id+=1
#     nights=(check_out-check_in).days
#     total_amount=calculate_amount(room,no_of_guests,nights,breakfast)


    