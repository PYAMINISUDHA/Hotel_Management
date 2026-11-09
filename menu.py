from datetime import datetime, date
import os
from database import (conn,cursor,save_guest,save_booking,view_bookings,get_guest_data,get_rooms_by_type,get_all_bookings,update_booking_status,cancel_booking)
from reports import (occupancy_report,revenue_report,export_bookings)
from pricing import (calculate_amount,calculate_refund,get_refund_amount)
from modules import (StandardRoom,Deluxe,Suite,Booking_room,Guest)
def read_date(message):
    while True:
        try:
            value=input(message)
            return datetime.strptime(value,"%d-%m-%Y").date()
        except ValueError:
            print("Enter date in DD-MM-YYYY format")
def validate_dates(check_in,check_out):
    today=date.today()
    if check_in<today:
        raise ValueError("Check-in date cannot be in the past")
    if (check_in - today).days > 180:
        raise ValueError("Check-in date cannot be more than 180 days away")
    if check_out<=check_in:
        raise ValueError("Check-out must be after check-in")
    nights=(check_out-check_in).days
    if nights>30:
        raise ValueError("Maximum stay is 30 nights")
def get_room_object(room_data):
    room_no=room_data[0]
    room_type=room_data[1]
    floor=room_data[2]
    if room_type=="Standard":
        return StandardRoom(room_no,room_type,floor)
    elif room_type=="Deluxe":
        return Deluxe(room_no,room_type,floor)
    elif room_type=="Suite":
        return Suite(room_no,room_type,floor)
def find_available_room(room_type,check_in,check_out,guests):
    rooms=get_rooms_by_type(room_type)
    bookings=get_all_bookings()
    available_rooms=[]
    for room_data in rooms:
        room=get_room_object(room_data)
        if guests>room.maximum_guests():
            continue
        room_available=True
        for booking in bookings:
            booked_room=booking[0]
            booked_check_in=datetime.strptime(booking[1],"%d-%m-%Y").date()
            booked_check_out=datetime.strptime(booking[2],"%d-%m-%Y").date()
            status=booking[3]
            if status in ["cancelled","checked_out"]:
                continue
            if room_data[0]==booked_room:
                if check_in<booked_check_out and check_out>booked_check_in:
                    room_available=False
                    break
        if room_available:
            available_rooms.append(room_data)
    if not available_rooms:
        return None
    available_rooms.sort(key=lambda row: int(row[0]))
    return available_rooms[0]
def show_alternative_rooms(check_in,check_out,guests,requested_type):
    room_types={"Standard":2,"Deluxe":3,"Suite":4}
    print("Other available room types:")
    found = False
    for room_type,capacity in room_types.items():
        if room_type==requested_type:
            continue
        if guests<=capacity:
            room=find_available_room(room_type,check_in,check_out, guests)
            if room:
                print(room_type,"- Room number:",room[0])
                found=True
    if not found:
        print("No alternative rooms available")
def search_room_availability():
    check_in=read_date("Enter check-in date: ")
    check_out=read_date("Enter check-out date: ")
    validate_dates(check_in,check_out)
    room_type=input("Enter room type: ").strip().title()
    guests=int(input("Enter number of guests: "))
    if guests <= 0:
        print("guest count must be greater than zero")
        return
    if room_type not in ["Standard","Deluxe","Suite"]:
        print("invalid room type")
        return
    room = find_available_room(room_type,check_in,check_out,guests)
    if room:
        print("Room available")
        print("Room number:",room[0])
        print("Room type:",room[1])
        print("Floor:",room[2])
    else:
        print("Requested room is not available")
        show_alternative_rooms(check_in,check_out,guests,room_type)

def create_booking():
    name=input("Enter guest name: ").strip()
    mobile=input("Enter mobile number: ").strip()
    email=input("Enter email: ").strip()
    if not mobile.isdigit() or len(mobile) != 10 or mobile[0] not in "6789":
        print("Invalid mobile number")
        return
    if not name or "@" not in email or "." not in email:
        print("Invalid guest name or email")
        return
    guests=int(input("Enter number of guests: "))
    if guests<=0:
        print("Guest count must be greater than zero")
        return
    room_type=input("Enter room type: ").strip().title()
    if room_type not in ["Standard","Deluxe","Suite"]:
        print("invalid room type")
        return
    check_in=read_date("Enter check-in date: ")
    check_out=read_date("Enter check-out date: ")
    validate_dates(check_in,check_out)
    breakfast=input("Breakfast required? (yes/no): ").strip().lower()=="yes"
    room_data=find_available_room(room_type, check_in, check_out, guests)
    if room_data is None:
        print("Requested room is not available")
        show_alternative_rooms(check_in, check_out, guests, room_type)
        return
    room=get_room_object(room_data)
    guest=Guest(name,mobile,email,guests)
    save_guest(mobile,name,email)
    guest_data,bookings,completed_stays=get_guest_data(mobile)
    amount_details=calculate_amount(room,guests,check_in,check_out,breakfast,completed_stays)
    cursor.execute("select count(*) from bookings")
    booking_count=cursor.fetchone()[0] + 1
    booking_id="BK" + str(booking_count).zfill(4)
    booking=Booking_room(booking_id,guest,room,check_in,check_out)
    booking.set_total(amount_details["total_amount"])
    booking.set_amount_paid(amount_details["total_amount"])
    saved=save_booking(booking_id,mobile,room_data[0],check_in,check_out,guests,breakfast,booking.get_status(),amount_details["total_amount"])
    if saved:
        print("Booking successful!")
        print("Booking ID:",booking_id)
        print("Room number:",room_data[0])
        print("Total amount:",round(amount_details["total_amount"], 2))
        print("Full payment received")

def check_in():
    booking_id=input("Enter booking ID: ").strip()
    booking=view_bookings(booking_id)
    if booking is None:
        return
    if booking[9]!="confirmed":
        print("Booking is not in confirmed status")
        return
    check_in_date=datetime.strptime(booking[5],"%d-%m-%Y").date()
    if date.today()!=check_in_date:
        print("Check-in is allowed only on the check-in date")
        return
    update_booking_status(booking_id,"checked_in")

def check_out():
    booking_id=input("Enter booking ID: ").strip()
    booking=view_bookings(booking_id)
    if booking is None:
        return
    if booking[9]!="checked_in":
        print("Guest is not checked in")
        return
    update_result=update_booking_status(booking_id,"checked_out")
    if not update_result:
        return
    room_data_cursor=conn.cursor()
    room_data_cursor.execute("""select room_type,floor from rooms where room_no=?""", (booking[4],))
    room_details=room_data_cursor.fetchone()
    room=get_room_object((booking[4],room_details[0],room_details[1]))
    check_in_date=datetime.strptime(booking[5],"%d-%m-%Y").date()
    check_out_date=datetime.strptime(booking[6],"%d-%m-%Y").date()
    guest_data,guest_bookings,completed_stays=get_guest_data(booking[2])
    previous_stays=completed_stays-1
    amount_details=calculate_amount(room,booking[7],check_in_date,check_out_date,bool(booking[8]),previous_stays)
    os.makedirs("invoices",exist_ok=True)
    invoice_name=os.path.join("invoices",booking_id+".txt")
    with open(invoice_name, "w") as file:
        file.write("----------Invoice----------")
        file.write("Booking ID: "+booking[0]+"\n")
        file.write("Guest Name: "+booking[1]+"\n")
        file.write("Mobile: "+booking[2]+"\n")
        file.write("Email: "+booking[3]+"\n")
        file.write("Room Number: "+booking[4] + "\n")
        file.write("Check-in: "+booking[5] + "\n")
        file.write("Check-out: "+booking[6] + "\n")
        file.write("Number of guests: " + str(booking[7]) + "\n")
        file.write("\n---------- Night Details ----------\n")
        for row in amount_details["night_details"]:
            file.write(
                str(row["date"]) +
                " | Room: " + str(round(row["room_tariff"], 2)) +
                " | Extra guest: " + str(round(row["extra_guest"], 2)) +
                " | Breakfast: " + str(round(row["breakfast"], 2)) +
                "\n"
            )
        file.write("\nRoom amount: " + str(round(amount_details["room_amount"], 2)))
        file.write("\nExtra guest amount: " + str(round(amount_details["guest_amount"], 2)))
        file.write("\nBreakfast amount: " + str(round(amount_details["breakfast_amount"], 2)))
        file.write("\nStay discount: " + str(round(amount_details["stay_discount"], 2)))
        file.write("\nLoyalty discount: " + str(round(amount_details["loyalty_discount"], 2)))
        file.write("\nGST: " + str(round(amount_details["gst_amount"], 2)))
        file.write("\nTotal amount: " + str(round(booking[10], 2)))
        file.write("\nAmount paid: " + str(round(booking[11], 2)))
        file.write("\n=====================================\n")
    print("Checkout successful")
    print("Invoice generated:", invoice_name)
def cancel_booking_menu():
    booking_id=input("Enter booking ID: ").strip()
    booking=view_bookings(booking_id)
    if booking is None:
        return
    if booking[9]!="confirmed":
        print("confirmed bookings can be cancelled")
        return
    check_in_date=datetime.strptime(booking[5],"%d-%m-%Y").date()
    refund_perc=calculate_refund(check_in_date)
    refund_amount=get_refund_amount(booking[11],refund_perc)
    result=cancel_booking(booking_id,refund_amount)
    if result:
        print("Refund percentage:",refund_perc, "%")
        print("Refund amount:",round(refund_amount, 2))
def booking_details():
    booking_id=input("Enter booking ID: ").strip()
    booking=view_bookings(booking_id)
    if booking:
        print("Booking ID:",booking[0])
        print("Guest Name:",booking[1])
        print("Mobile:",booking[2])
        print("Email:",booking[3])
        print("Room Number:",booking[4])
        print("Check-in:",booking[5])
        print("Check-out:",booking[6])
        print("Guests:",booking[7])
        print("Breakfast:",bool(booking[8]))
        print("Status:",booking[9])
        print("Total amount:",booking[10])
        print("Amount paid:",booking[11])
        print("Refund:",booking[12])
def guest_history():
    mobile=input("enter mobile number: ").strip()
    guest,bookings,completed_stays=get_guest_data(mobile)
    if guest is None:
        return
    print("Guest Name:",guest[0])
    print("Mobile:",guest[1])
    print("Email:",guest[2])
    print("Completed stays:",completed_stays)
    print("Booking History:")
    for booking in bookings:
        print(booking)
def occupancy():
    start_date =read_date("enter the start date:")
    end_date =read_date("enter the end date:")
    if end_date<=start_date:
        print("Enddate must be after start date")
        return
    occupancy_report(start_date,end_date)
def revenue():
    revenue_report()
def export_data():
    export_bookings()
def show_menu():
    while True:
        print("1.Search Room Availability")
        print("2.Create Booking")
        print("3.Check In")
        print("4.Check Out")
        print("5.Cancel Booking")
        print("6.Booking Details")
        print("7.Guest History")
        print("8.Occupancy Report")
        print("9.Revenue Report")
        print("10.Export Bookings")
        print("11.Exit")
        choice = input("Enter your choice: ")
        try:
            if choice=="1":
                search_room_availability()
            elif choice=="2":
                create_booking()
            elif choice=="3":
                check_in()
            elif choice=="4":
                check_out()
            elif choice=="5":
                cancel_booking_menu()
            elif choice=="6":
                booking_details()
            elif choice=="7":
                guest_history()
            elif choice=="8":
                occupancy()
            elif choice=="9":
                revenue()
            elif choice=="10":
                export_data()
            elif choice=="11":
                print("thankyou")
                break
            else:
                print("invalid choice")
        except Exception as e:
            print("Error:", e)
