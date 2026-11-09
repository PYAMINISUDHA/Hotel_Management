import sqlite3
import csv
from datetime import datetime, timedelta
conn = sqlite3.connect("database.db")
cursor=conn.cursor()
def occupancy_report(start_date, end_date):
    cursor.execute("select count(*) from rooms")
    total_rooms=cursor.fetchone()[0]
    cursor.execute("""
    select room_no,check_in,check_out,status
    from bookings
    where status != ?
    """,("cancelled",))
    bookings=cursor.fetchall()
    current_date=start_date
    while current_date<=end_date:
        occupied_rooms=set()
        for booking in bookings:
            room_no=booking[0]
            check_in = datetime.strptime(booking[1], "%d-%m-%Y").date()
            check_out=datetime.strptime(booking[2], "%d-%m-%Y").date()
            if check_in<=current_date<check_out:
                occupied_rooms.add(room_no)
        occupied_count=len(occupied_rooms)
        available_count=total_rooms-occupied_count
        if total_rooms>0:
            occupancy_perc=(occupied_count/total_rooms)*100
        else:
            occupancy_perc=0
        print("Date:",current_date)
        print("Total rooms:",total_rooms)
        print("Occupied rooms:",occupied_count)
        print("Available rooms:",available_count)
        print("Occupancy:",round(occupancy_perc,2),"%")
        current_date=current_date+timedelta(days=1)
def revenue_report():
    cursor.execute("""
        select rooms.room_type,sum(bookings.amount_paid)
        from bookings
        join rooms ON bookings.room_no=rooms.room_no
        where bookings.status != ?
        group by  rooms.room_type
    """, ("cancelled",))
    result = cursor.fetchall()
    total_revenue = 0
    for row in result:
        room_type=row[0]
        revenue=row[1]
        print(room_type,"Revenue:",revenue)
        total_revenue+=revenue
    print("Total Revenue:",total_revenue)
def export_bookings():
    conn_export=sqlite3.connect("database.db")
    cursor_export=conn_export.cursor()
    cursor_export.execute("""select booking_id,mobile,room_no,check_in,check_out,no_of_guests,status,total_amount from bookings""")
    bookings=cursor_export.fetchall()
    conn_export.close()
    with open("bookings_export.csv","w") as file:
        writer=csv.writer(file)
        writer.writerow(["Booking ID","Mobile","Room No","Check In","Check Out","Guests","Status","Total Amount"])
        writer.writerows(bookings)
    print("bookings exported successfully")
