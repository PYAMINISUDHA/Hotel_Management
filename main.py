from database import create_tables,load_rooms
from menu import show_menu
from modules import StandardRoom,Deluxe,Suite,Booking_room,Guest
def main():
    create_tables()
    load_rooms()
    show_menu()
main()