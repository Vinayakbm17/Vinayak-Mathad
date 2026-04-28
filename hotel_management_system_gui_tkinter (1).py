import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    room_number INTEGER PRIMARY KEY,
    room_type TEXT,
    price INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number INTEGER,
    guest_name TEXT,
    nights INTEGER,
    status TEXT,
    checkin_date TEXT
)
""")

# Insert default rooms if empty
cursor.execute("SELECT COUNT(*) FROM rooms")
if cursor.fetchone()[0] == 0:
    rooms_data = [
        (101, "Standard", 100),
        (102, "Standard", 100),
        (201, "Deluxe", 200),
        (202, "Deluxe", 200),
        (301, "Suite", 500)
    ]
    cursor.executemany("INSERT INTO rooms VALUES (?, ?, ?)", rooms_data)
    conn.commit()

# ---------------- GUI ----------------
class HotelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System (Real World)")
        self.root.geometry("900x550")

        ttk.Label(root, text="Hotel Management Dashboard", font=("Arial", 18, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(root, columns=("Room", "Type", "Price", "Status", "Guest"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10)

        # Form
        form = ttk.Frame(root)
        form.pack(pady=10)

        ttk.Label(form, text="Room No").grid(row=0, column=0)
        self.room_entry = ttk.Entry(form)
        self.room_entry.grid(row=0, column=1)

        ttk.Label(form, text="Guest Name").grid(row=1, column=0)
        self.name_entry = ttk.Entry(form)
        self.name_entry.grid(row=1, column=1)

        ttk.Label(form, text="Nights").grid(row=2, column=0)
        self.nights_entry = ttk.Entry(form)
        self.nights_entry.grid(row=2, column=1)

        ttk.Button(form, text="Book", command=self.book_room).grid(row=0, column=2, padx=10)
        ttk.Button(form, text="Check-In", command=self.checkin).grid(row=1, column=2)
        ttk.Button(form, text="Check-Out", command=self.checkout).grid(row=2, column=2)
        ttk.Button(form, text="Refresh", command=self.load_rooms).grid(row=3, column=2, pady=5)

        self.load_rooms()

    def load_rooms(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()

        for room in rooms:
            room_no, rtype, price = room

            cursor.execute("SELECT guest_name, status FROM bookings WHERE room_number=? ORDER BY id DESC LIMIT 1", (room_no,))
            booking = cursor.fetchone()

            if booking:
                guest, status = booking
            else:
                guest, status = "", "Available"

            self.tree.insert("", "end", values=(room_no, rtype, f"${price}", status, guest))

    def book_room(self):
        try:
            room = int(self.room_entry.get())
            name = self.name_entry.get()
            nights = int(self.nights_entry.get())

            cursor.execute("INSERT INTO bookings (room_number, guest_name, nights, status) VALUES (?, ?, ?, ?)",
                           (room, name, nights, "Reserved"))
            conn.commit()

            messagebox.showinfo("Success", "Room Reserved")
            self.load_rooms()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def checkin(self):
        try:
            room = int(self.room_entry.get())
            date = datetime.now().strftime("%Y-%m-%d %H:%M")

            cursor.execute("UPDATE bookings SET status=?, checkin_date=? WHERE room_number=? AND status='Reserved'",
                           ("Occupied", date, room))
            conn.commit()

            messagebox.showinfo("Success", "Checked In")
            self.load_rooms()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def checkout(self):
        try:
            room = int(self.room_entry.get())

            cursor.execute("SELECT guest_name, nights FROM bookings WHERE room_number=? AND status='Occupied' ORDER BY id DESC LIMIT 1", (room,))
            data = cursor.fetchone()

            if not data:
                messagebox.showerror("Error", "No active booking")
                return

            guest, nights = data

            cursor.execute("SELECT price FROM rooms WHERE room_number=?", (room,))
            price = cursor.fetchone()[0]

            total = nights * price

            cursor.execute("UPDATE bookings SET status='Completed' WHERE room_number=? AND status='Occupied'", (room,))
            conn.commit()

            messagebox.showinfo("Invoice", f"Guest: {guest}\nNights: {nights}\nTotal: ${total}")
            self.load_rooms()
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelGUI(root)
    root.mainloop()