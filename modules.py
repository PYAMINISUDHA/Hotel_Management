from abc import ABC,abstractmethod
from collections import defaultdict
from datetime import date,datetime,timedelta
import csv

room_available=defaultdict(list)
room_numbers=set()
today=datetime.today()
Booking_id=1

with open("room.csv","r") as file:
    reader=csv.DictReader(file)
    for row in reader:
        try:
            room_no = row["room_no"].strip()
            if not room_no or room_no in room_numbers:
                raise ValueError("Room number cannot be empty .")
            room_type = row["room_type"].strip()
            if not room_type or room_type not in ("Standard","Deluxe","Suite"):
                raise ValueError("room_type must be (Standard,Deluxe,Suite)")
            floor = row["floor"].strip()
            if not floor:
                raise ValueError("floor cannot be empty")
      
            room_available[room_type].append({
                "room_no":room_no,
                "floor":floor,
                "status":"available"
            })
            room_numbers.add(room_no)
        except ValueError as e:
            with open ("errors.log","a") as error:
                error.write(str(e)+"\n")
            
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
    def cost_breakfast(self,no_guest):
        pass
    @abstractmethod
    def maximum_guests(self):
        pass
    

class StandardRoom(Room):
    def get_tariff(self):
        return 2500
    def guest_charges(self,no_guest):
        return 0
    def cost_breakfast(self,no_guest):
        return 350*no_guest
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
    def cost_breakfast(self,no_guest):
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
    def cost_breakfast(self,no_guest):
        return 0
    def maximum_guests(self):
        return 4


class Booking_room():
    def __init__(self,booking_id,guest,check_in,check_out):
        self.booking_id=booking_id
        self.guest=guest
        self.check_in=check_in
        self.check_out=check_out
        self.status="confirmed"

    def __str__(self):
        return f"bookig_id : {self.booking_id} guest : {self.guest} check_in :{self.check_in} check_out : {self.check_out} status : {self.status}"

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

def get_booking_dates():
    while True:
        check_in=input("Enter check-in date (DD-MM-YYYY) :").strip()
        try:
            check_in=datetime.strptime(check_in,"%d-%m-%Y").date()
        except ValueError:
            print("Invalid check-in  date ")
            continue
        if check_in<today:
            print("check in cannot be in the past ")
        if check_in>today+timedelta(days=180):
            print("check - in must be with in180 days")
        break
    while True:
        check_out=input("enter your check out time ").strip()
        try :
            check_out=datetime.strptime(check_out,"%d-%m-%Y").date()
        except ValueError:
            print("Invalid check-out date")
        if check_out<=check_in:
            print("check-out must be after check-in.")

        nights=(check_out-check_in).days
        if nights>30:
            print("maximum 30 nights are allowed")
            continue
        break
    return check_in,check_out
