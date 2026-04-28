class Room:
    def __init__(self, room_number, room_type, price_per_night):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.is_booked = False
        self.is_checked_in = False
        self.guest_name = None
        self.stay_duration = 0

class HotelManagementSystem:
    def __init__(self):
        # Initializing some rooms
        self.rooms = {
            101: Room(101, "Standard", 100),
            102: Room(102, "Standard", 100),
            201: Room(201, "Deluxe", 200),
            202: Room(202, "Deluxe", 200),
            301: Room(301, "Suite", 500)
        }

    def display_available_rooms(self):
        print("\n--- Available Rooms ---")
        print(f"{'Room #':<10} {'Type':<15} {'Price/Night':<12}")
        for room in self.rooms.values():
            if not room.is_booked:
                print(f"{room.room_number:<10} {room.room_type:<15} ${room.price_per_night:<12}")

    def book_room(self, room_number, guest_name, nights):
        room = self.rooms.get(room_number)
        if room and not room.is_booked:
            room.is_booked = True
            room.guest_name = guest_name
            room.stay_duration = nights
            print(f"Room {room_number} successfully booked for {guest_name} for {nights} nights.")
        else:
            print("Error: Room is either invalid or already booked.")

    def check_in(self, room_number):
        room = self.rooms.get(room_number)
        if room and room.is_booked and not room.is_checked_in:
            room.is_checked_in = True
            print(f"Guest {room.guest_name} has checked into Room {room_number}.")
        else:
            print("Error: Check-in failed. Ensure the room is booked first.")

    def check_out(self, room_number):
        room = self.rooms.get(room_number)
        if room and room.is_checked_in:
            total_cost = room.stay_duration * room.price_per_night
            print(f"\n--- Invoice for Room {room_number} ---")
            print(f"Guest: {room.guest_name}")
            print(f"Stay Duration: {room.stay_duration} nights")
            print(f"Total Amount Due: ${total_cost}")
            
            # Reset room status
            room.is_booked = False
            room.is_checked_in = False
            room.guest_name = None
            room.stay_duration = 0
            print("Check-out complete. Room is now available.")
        else:
            print("Error: Room is not occupied.")

# --- Execution Example ---
hotel = HotelManagementSystem()

# 1. Show available rooms
hotel.display_available_rooms()

# 2. Book a room
hotel.book_room(201, "John Doe", 3)

# 3. Try to check in
hotel.check_in(201)

# 4. Check out and calculate payment
hotel.check_out(201)

# 5. Show rooms again to verify availability
hotel.display_available_rooms()