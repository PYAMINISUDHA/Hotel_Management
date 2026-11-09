import sqlite3
import csv 
conn=sqlite3.connect("database.db")
conn.execute("PRAGMA foreign_keys=ON")
cursor=conn.cursor()
def create_tables():
    cursor.execute("""
create table if not exists rooms(
room_no text primary key,
room_type text not null,
floor integer not null)
""")
    cursor.execute("""
create table if not exists guests(
mobile text primary key,
name text not null,
email text not null
)
""")
    cursor.execute("""
create table if not exists bookings(
booking_id text primary key,
mobile text not null,
room_no text not null,
check_in text not null,
check_out text not null,
no_of_guests integer not null,
breakfast integer not null,
status text not null,
total_amount real not null,
amount_paid real not null,
refund real default 0,
foreign key(mobile) references guests(mobile),
foreign key(room_no) references rooms(room_no))
""")
    conn.commit()
def load_rooms():
    room_numbers=set()
    valid_room_types=["Standard","Deluxe","Suite"]
    try:
        with open("room.csv","r") as file:
            reader=csv.DictReader(file)
            for row in reader:
                try:
                    room_no=row["room_no"].strip()
                    room_type=row["room_type"].strip()
                    floor=int(row["floor"])
                    if not room_no:
                        raise ValueError("room is empty")
                    if room_no in room_numbers:
                        raise ValueError("enter unic room numbers")
                    if room_type not in valid_room_types:
                        raise ValueError("invalid room type")
                    if floor<=0:
                        raise ValueError("Invalid floor number")
                    cursor.execute("""insert into rooms(room_no,room_type,floor)
                        values(?,?,?)
                    """,(room_no,room_type,floor))
                    room_numbers.add(room_no)
                except(ValueError,KeyError,sqlite3.IntegrityError) as error:
                    with open("app.log","a") as error_file:
                        error_file.write(str(error))
            conn.commit()
            print("room data entered ")
    except FileNotFoundError:
        print("file not found")

def save_guest(mobile,name,email):
    cursor.execute("select mobile from guests where mobile=?",(mobile,))
    guest=cursor.fetchone()
    if guest:
        print("returning guest")
    else:
        cursor.execute("""
 insert into guests(mobile,name,email) values(?,?,?)""",(mobile,name,email))
    conn.commit()

def save_booking(booking_id,mobile,room_no,check_in,check_out,no_of_guests,breakfast,status,total_amount):
    try:
        cursor.execute("""
insert into bookings(booking_id,mobile,room_no,check_in,check_out,no_of_guests,breakfast,status,total_amount,amount_paid,refund)
values(?,?,?,?,?,?,?,?,?,?,?)
""",(
    booking_id,mobile,room_no,check_in.strftime("%d-%m-%Y"),check_out.strftime("%d-%m-%Y"),no_of_guests,int(breakfast),status,total_amount,total_amount,0))
        conn.commit()
        print("booking successfully")
        return True
    except sqlite3.Error as error:
        conn.rollback()
        print("unavailable to save booking :" ,error)
        return False
    
def view_bookings(booking_id):
    cursor.execute("""
select bookings.booking_id,
guests.name,
guests.mobile,
guests.email,
bookings.room_no,
bookings.check_in,
bookings.check_out,
bookings.no_of_guests,
bookings.breakfast,
bookings.status,
bookings.total_amount,
bookings.amount_paid,
bookings.refund
from bookings
join guests
on bookings.mobile=guests.mobile
where bookings.booking_id=?
""",(booking_id,))
    booking=cursor.fetchone()
    if booking is None:
        print("booking not found")
        return []
    return booking

def get_guest_data(mobile):
    cursor.execute("""
select name,mobile,email from guests where mobile=?
""",(mobile,))
    guest=cursor.fetchone()
    if guest is None:
        print("guest not found")
        return None, [], 0

    cursor.execute("""
select booking_id,room_no,check_in,check_out,status,total_amount
from bookings where mobile=?
""",(mobile,))
    bookings = cursor.fetchall()
    cursor.execute("""
select count(*) from bookings where mobile=? and status=?
""",(mobile,"checked_out"))
    completed_stays = cursor.fetchone()[0]
    return guest, bookings, completed_stays
def get_rooms_by_type(room_type):
    cursor.execute("""
select room_no,room_type,floor
from rooms
where room_type=?
""",(room_type,))
    return cursor.fetchall()
def get_all_bookings():
    cursor.execute("""
select room_no,check_in,check_out,status
from bookings
""")
    return cursor.fetchall()
def update_booking_status(booking_id,new_status):
    try:
        cursor.execute("""
update bookings set status=? where booking_id=?
""",(new_status,booking_id))
        if cursor.rowcount==0:
            print("booking not found")
            return False
        conn.commit()
        print("booking status updated successfully")
        return True
    except sqlite3.Error as error:
        conn.rollback()
        print("unable to update booking:",error)
        return False
def cancel_booking(booking_id,refund_amount):
    try:
        cursor.execute("""
update bookings
set status=?,refund=?
where booking_id=?and status=?
""",("cancelled",refund_amount,booking_id,"confirmed"))
        if cursor.rowcount == 0:
            print("booking not found or cannot be cancelled")
            return False
        conn.commit()
        print("booking cancelled")
        return True
    except sqlite3.Error as error:
        conn.rollback()
        print("unable to cancel booking:",error)
        return False
