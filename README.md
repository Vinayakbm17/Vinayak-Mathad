 What the code does:
Creates a Room class to store:
Room number
Room type
Price per night
Booking status
Guest name
Stay duration
Creates a HotelManagementSystem class with preloaded rooms:
101, 102 → Standard ($100)
201, 202 → Deluxe ($200)
301 → Suite ($500)
Main Functions:
display_available_rooms()
Shows all available rooms.
book_room(room_number, guest_name, nights)
Books a room for a guest.
check_in(room_number)
Checks guest into booked room.
check_out(room_number)
Calculates total bill.
Prints invoice.
Makes room available again.
Example Run in File:
Show rooms
Book Room 201 for John Doe (3 nights)
Check-in
Check-out
Show rooms again
