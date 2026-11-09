from abc import ABC,abstractmethod
from exception import Invalid_status_Change
            
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
        elif self._status=="checked_in":
            if new_status=="checked_out":
                self._status=new_status
            else:
                raise Invalid_status_Change("Invalid status chenge")
        else:
            raise Invalid_status_Change("Booking cannot be changed")
    def __str__(self):
        return f"Booking_id : {self._booking_id} guest : {self._guest.get_name()}, room:{self._room.room_no} status:{self._status}"
        

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