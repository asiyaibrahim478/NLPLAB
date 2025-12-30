#!/usr/bin/env python3
"""
HostelHelper - Girls' Hostel Management Chatbot
A complete offline chatbot system for hostel management
"""

import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional


# ============================================================================
# DATA MODELS
# ============================================================================

class User:
    """User model for authentication and role management"""
    
    def __init__(self, username: str, password: str, role: str, 
                 room_number: Optional[str] = None, full_name: str = ""):
        self.username = username
        self.password = password
        self.role = role  # 'resident', 'warden', 'admin'
        self.room_number = room_number
        self.full_name = full_name
    
    def to_dict(self) -> Dict:
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'room_number': self.room_number,
            'full_name': self.full_name
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data['username'],
            data['password'],
            data['role'],
            data.get('room_number'),
            data.get('full_name', '')
        )


class Complaint:
    """Complaint model for tracking issues"""
    
    def __init__(self, complaint_id: str, username: str, category: str,
                 description: str, status: str = "Open", 
                 submitted_date: str = None):
        self.complaint_id = complaint_id
        self.username = username
        self.category = category
        self.description = description
        self.status = status
        self.submitted_date = submitted_date or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.resolved_date = None
    
    def to_dict(self) -> Dict:
        return {
            'complaint_id': self.complaint_id,
            'username': self.username,
            'category': self.category,
            'description': self.description,
            'status': self.status,
            'submitted_date': self.submitted_date,
            'resolved_date': self.resolved_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        complaint = cls(
            data['complaint_id'],
            data['username'],
            data['category'],
            data['description'],
            data['status'],
            data['submitted_date']
        )
        complaint.resolved_date = data.get('resolved_date')
        return complaint


class Event:
    """Event model for hostel activities"""
    
    def __init__(self, event_id: str, title: str, description: str,
                 date: str, time: str, venue: str):
        self.event_id = event_id
        self.title = title
        self.description = description
        self.date = date
        self.time = time
        self.venue = venue
    
    def to_dict(self) -> Dict:
        return {
            'event_id': self.event_id,
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'time': self.time,
            'venue': self.venue
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data['event_id'],
            data['title'],
            data['description'],
            data['date'],
            data['time'],
            data['venue']
        )


class Room:
    """Room model for allocation management"""
    
    def __init__(self, room_number: str, capacity: int, 
                 occupied: int = 0, residents: List[str] = None):
        self.room_number = room_number
        self.capacity = capacity
        self.occupied = occupied
        self.residents = residents or []
    
    def is_available(self) -> bool:
        return self.occupied < self.capacity
    
    def to_dict(self) -> Dict:
        return {
            'room_number': self.room_number,
            'capacity': self.capacity,
            'occupied': self.occupied,
            'residents': self.residents
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data['room_number'],
            data['capacity'],
            data['occupied'],
            data.get('residents', [])
        )


# ============================================================================
# DATA MANAGER
# ============================================================================

class DataManager:
    """Handles all file I/O operations for persistence"""
    
    def __init__(self):
        self.data_dir = "hostel_data"
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.complaints_file = os.path.join(self.data_dir, "complaints.json")
        self.events_file = os.path.join(self.data_dir, "events.json")
        self.rooms_file = os.path.join(self.data_dir, "rooms.json")
        self.menu_file = os.path.join(self.data_dir, "menu.json")
        self.attendance_file = os.path.join(self.data_dir, "attendance.json")
        self.feedback_file = os.path.join(self.data_dir, "feedback.json")
        
        self._ensure_data_dir()
        self._initialize_default_data()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _initialize_default_data(self):
        """Initialize default data if files don't exist"""
        # Default users
        if not os.path.exists(self.users_file):
            default_users = [
                User("admin", "admin123", "admin", None, "Admin User"),
                User("warden1", "warden123", "warden", None, "Warden Mary"),
                User("sarah", "sarah123", "resident", "101", "Sarah Ahmed"),
                User("fatima", "fatima123", "resident", "101", "Fatima Khan"),
            ]
            self.save_users([u.to_dict() for u in default_users])
        
        # Default rooms
        if not os.path.exists(self.rooms_file):
            default_rooms = [
                Room("101", 2, 2, ["sarah", "fatima"]),
                Room("102", 2, 1, ["aisha"]),
                Room("103", 2, 0, []),
                Room("201", 3, 0, []),
                Room("202", 3, 0, []),
            ]
            self.save_rooms([r.to_dict() for r in default_rooms])
        
        # Default menu
        if not os.path.exists(self.menu_file):
            default_menu = {
                "Monday": {"breakfast": "Paratha & Chai", "lunch": "Chicken Biryani", "dinner": "Daal & Roti"},
                "Tuesday": {"breakfast": "Halwa Puri", "lunch": "Beef Curry & Rice", "dinner": "Vegetable Karahi"},
                "Wednesday": {"breakfast": "Omelette & Toast", "lunch": "Fish Curry", "dinner": "Chicken Korma"},
                "Thursday": {"breakfast": "Nihari", "lunch": "Pulao & Raita", "dinner": "Mix Vegetable"},
                "Friday": {"breakfast": "Aloo Paratha", "lunch": "Biryani Special", "dinner": "BBQ Night"},
                "Saturday": {"breakfast": "French Toast", "lunch": "Pasta & Salad", "dinner": "Grilled Chicken"},
                "Sunday": {"breakfast": "Pancakes", "lunch": "Home Style Curry", "dinner": "Karahi & Naan"}
            }
            self.save_menu(default_menu)
        
        # Initialize empty files for other data
        for file_path in [self.complaints_file, self.events_file, 
                         self.attendance_file, self.feedback_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)
    
    def load_json(self, file_path: str) -> List[Dict]:
        """Load JSON data from file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_json(self, file_path: str, data: List[Dict]):
        """Save JSON data to file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_users(self) -> List[User]:
        """Load all users"""
        data = self.load_json(self.users_file)
        return [User.from_dict(u) for u in data]
    
    def save_users(self, users: List[Dict]):
        """Save users"""
        self.save_json(self.users_file, users)
    
    def load_complaints(self) -> List[Complaint]:
        """Load all complaints"""
        data = self.load_json(self.complaints_file)
        return [Complaint.from_dict(c) for c in data]
    
    def save_complaints(self, complaints: List[Dict]):
        """Save complaints"""
        self.save_json(self.complaints_file, complaints)
    
    def load_events(self) -> List[Event]:
        """Load all events"""
        data = self.load_json(self.events_file)
        return [Event.from_dict(e) for e in data]
    
    def save_events(self, events: List[Dict]):
        """Save events"""
        self.save_json(self.events_file, events)
    
    def load_rooms(self) -> List[Room]:
        """Load all rooms"""
        data = self.load_json(self.rooms_file)
        return [Room.from_dict(r) for r in data]
    
    def save_rooms(self, rooms: List[Dict]):
        """Save rooms"""
        self.save_json(self.rooms_file, rooms)
    
    def load_menu(self) -> Dict:
        """Load mess menu"""
        try:
            with open(self.menu_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_menu(self, menu: Dict):
        """Save mess menu"""
        with open(self.menu_file, 'w') as f:
            json.dump(menu, f, indent=2)
    
    def load_attendance(self) -> List[Dict]:
        """Load attendance records"""
        return self.load_json(self.attendance_file)
    
    def save_attendance(self, attendance: List[Dict]):
        """Save attendance records"""
        self.save_json(self.attendance_file, attendance)
    
    def load_feedback(self) -> List[Dict]:
        """Load feedback"""
        return self.load_json(self.feedback_file)
    
    def save_feedback(self, feedback: List[Dict]):
        """Save feedback"""
        self.save_json(self.feedback_file, feedback)


# ============================================================================
# CHATBOT ENGINE
# ============================================================================

class HostelHelper:
    """Main chatbot class"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.current_user: Optional[User] = None
        self.running = True
        
        # Motivational quotes for girls
        self.quotes = [
            "She believed she could, so she did. 💪",
            "Strong women lift each other up. 🌟",
            "Be a girl with a mind, a woman with attitude, and a lady with class. ✨",
            "Empowered women empower women. 👑",
            "You are braver than you believe, stronger than you seem. 💖",
            "Well-behaved women seldom make history. 🔥",
            "She is clothed in strength and dignity. 🌸",
            "A woman is like a tea bag - you never know how strong she is until she gets in hot water. ☕",
        ]
        
        # Health and wellness tips
        self.wellness_tips = [
            "💧 Drink at least 8 glasses of water daily!",
            "🧘 Take 10-minute meditation breaks to reduce stress.",
            "🥗 Include iron-rich foods in your diet (spinach, dates, lentils).",
            "😴 Aim for 7-8 hours of sleep for better concentration.",
            "🚶 Take a 20-minute walk to boost your mood.",
            "📚 Take regular study breaks - your brain needs rest too!",
            "🌺 During periods, rest well and use a heating pad for cramps.",
            "🧠 Practice gratitude - write 3 things you're thankful for daily.",
            "🤗 Connect with friends - social support is essential for mental health.",
            "🎵 Listen to music to elevate your mood and reduce anxiety.",
        ]
    
    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, text: str):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)
    
    def print_separator(self):
        """Print separator line"""
        print("-" * 60)
    
    def get_input(self, prompt: str) -> str:
        """Get user input with prompt"""
        return input(f"\n{prompt}: ").strip()
    
    def show_welcome(self):
        """Display welcome message"""
        self.clear_screen()
        print("\n" + "=" * 60)
        print("  ✨ WELCOME TO HOSTELHELPER ✨")
        print("  Your Virtual Assistant for Girls' Hostel Management")
        print("=" * 60)
        print("\n  'In a world full of trends, remain a classic.' 💖")
        print("\n  Type 'help' anytime for assistance | Type 'exit' to quit")
        print("=" * 60)
    
    def authenticate(self) -> bool:
        """Handle user authentication"""
        self.print_header("LOGIN")
        
        username = self.get_input("Username")
        if username.lower() in ['exit', 'quit']:
            return False
        
        password = self.get_input("Password")
        if password.lower() in ['exit', 'quit']:
            return False
        
        users = self.data_manager.load_users()
        for user in users:
            if user.username == username and user.password == password:
                self.current_user = user
                print(f"\n✅ Welcome back, {user.full_name or username}! ")
                input("\nPress Enter to continue...")
                return True
        
        print("\n❌ Invalid credentials. Please try again.")
        input("\nPress Enter to continue...")
        return False
    
    def show_main_menu(self):
        """Display role-based main menu"""
        self.clear_screen()
        print(f"\n👋 Hey {self.current_user.full_name or self.current_user.username}!")
        print(f"   Role: {self.current_user.role.capitalize()}")
        if self.current_user.room_number:
            print(f"   Room: {self.current_user.room_number}")
        
        # Random daily quote
        print(f"\n💫 {random.choice(self.quotes)}")
        
        self.print_header("MAIN MENU")
        
        common_options = [
            "1. View Hostel Information",
            "2. View Mess Menu",
            "3. View Events",
            "4. Emergency Contacts",
            "5. Wellness Tips",
            "6. Daily Motivation",
        ]
        
        if self.current_user.role == "resident":
            print("\n".join(common_options))
            print("7. Submit Complaint")
            print("8. View My Complaints")
            print("9. Mark Attendance")
            print("10. View My Room Details")
            print("11. Submit Feedback")
            print("12. Logout")
        
        elif self.current_user.role == "warden":
            print("\n".join(common_options))
            print("7. View All Complaints")
            print("8. Resolve Complaints")
            print("9. View Attendance Report")
            print("10. View Room Allocation")
            print("11. View Feedback")
            print("12. Statistics Dashboard")
            print("13. Logout")
        
        elif self.current_user.role == "admin":
            print("\n".join(common_options))
            print("7. Manage Users")
            print("8. Manage Rooms")
            print("9. Update Mess Menu")
            print("10. Add Event")
            print("11. View All Complaints")
            print("12. View Feedback")
            print("13. Statistics Dashboard")
            print("14. Logout")
        
        self.print_separator()
    
    def view_hostel_info(self):
        """Display hostel information"""
        self.clear_screen()
        self.print_header("HOSTEL INFORMATION")
        
        info = """
📋 HOSTEL RULES & REGULATIONS:

🕐 Curfew Time: 10:00 PM (Weekdays) | 11:00 PM (Weekends)
✅ Visitors allowed between 2:00 PM - 6:00 PM
🚫 No outside food after 8:00 PM
📵 Silence hours: 11:00 PM - 7:00 AM
🧹 Room inspection: Every Saturday
🔐 Keep your room locked when away

🏢 FACILITIES AVAILABLE:

📡 High-Speed Wi-Fi (24/7)
🧺 Laundry Service (Mon, Wed, Fri)
💪 Gym & Fitness Center
📚 Study Rooms (Open 24/7)
🏥 Medical Room with Nurse
🍽️ Mess Hall (Breakfast, Lunch, Dinner)
🎮 Recreation Room
☕ Common Room with TV
🖨️ Printing & Photocopying
🔒 24/7 Security

📞 WARDEN OFFICE: Extension 100
🆘 SECURITY: Extension 200
🏥 MEDICAL ROOM: Extension 300
        """
        
        print(info)
        input("\n\nPress Enter to return to menu...")
    
    def view_mess_menu(self):
        """Display mess menu"""
        self.clear_screen()
        self.print_header("MESS MENU")
        
        menu = self.data_manager.load_menu()
        
        # Show today's menu highlighted
        today = datetime.now().strftime("%A")
        
        print(f"\n🌟 TODAY'S MENU ({today}):")
        if today in menu:
            print(f"   🌅 Breakfast: {menu[today]['breakfast']}")
            print(f"   🍱 Lunch: {menu[today]['lunch']}")
            print(f"   🌙 Dinner: {menu[today]['dinner']}")
        
        print("\n📅 WEEKLY MENU:\n")
        for day, meals in menu.items():
            highlight = ">>> " if day == today else "    "
            print(f"{highlight}{day}:")
            print(f"     Breakfast: {meals['breakfast']}")
            print(f"     Lunch: {meals['lunch']}")
            print(f"     Dinner: {meals['dinner']}")
            print()
        
        input("\nPress Enter to return to menu...")
    
    def view_events(self):
        """Display upcoming events"""
        self.clear_screen()
        self.print_header("UPCOMING EVENTS")
        
        events = self.data_manager.load_events()
        
        if not events:
            print("\n📅 No upcoming events scheduled at the moment.")
        else:
            for i, event in enumerate(events, 1):
                print(f"\n{i}. 🎉 {event.title}")
                print(f"   📅 Date: {event.date} | ⏰ Time: {event.time}")
                print(f"   📍 Venue: {event.venue}")
                print(f"   📝 {event.description}")
                self.print_separator()
        
        input("\nPress Enter to return to menu...")
    
    def show_emergency_contacts(self):
        """Display emergency contact information"""
        self.clear_screen()
        self.print_header("EMERGENCY CONTACTS")
        
        contacts = """
🆘 EMERGENCY NUMBERS:

🚨 Emergency Services: 15
🚓 Police: 15
🚑 Ambulance: 1122
🔥 Fire Brigade: 16

🏨 HOSTEL CONTACTS:

👮 Security Control Room: 0300-1234567
👩‍⚕️ Hostel Nurse: 0300-2345678
👨‍💼 Chief Warden: 0300-3456789
🏥 Nearest Hospital: 0512345678

🆘 HELPLINES:

💙 Mental Health Helpline: 0800-12345
👩 Women Helpline: 1099
🏥 Medical Emergency: 1122

⚠️ SAFETY TIPS:

• Always inform the warden before leaving campus
• Travel in groups after dark
• Keep your room locked
• Don't share personal information with strangers
• Trust your instincts - if something feels wrong, seek help
• Save these numbers in your phone
        """
        
        print(contacts)
        input("\n\nPress Enter to return to menu...")
    
    def show_wellness_tips(self):
        """Display random wellness tips"""
        self.clear_screen()
        self.print_header("WELLNESS TIPS FOR YOU")
        
        # Show 5 random tips
        tips = random.sample(self.wellness_tips, min(5, len(self.wellness_tips)))
        
        print("\n💖 Here are some wellness tips to keep you healthy and happy:\n")
        for tip in tips:
            print(f"   {tip}\n")
        
        print("\n🌸 Remember: Self-care is not selfish, it's essential!")
        
        input("\n\nPress Enter to return to menu...")
    
    def show_daily_motivation(self):
        """Display motivational message"""
        self.clear_screen()
        self.print_header("DAILY MOTIVATION")
        
        quote = random.choice(self.quotes)
        
        print(f"\n\n   {quote}\n")
        print("   Remember: You are capable of amazing things! 🌟")
        print("   Every day is a new opportunity to grow and shine. ✨")
        
        input("\n\n\nPress Enter to return to menu...")
    
    def submit_complaint(self):
        """Handle complaint submission (Resident)"""
        self.clear_screen()
        self.print_header("SUBMIT COMPLAINT")
        
        print("\n📋 Complaint Categories:")
        print("1. Maintenance (Electrical, Plumbing, Furniture)")
        print("2. Food/Mess Issues")
        print("3. Cleanliness")
        print("4. Noise/Disturbance")
        print("5. Security Concerns")
        print("6. Wi-Fi/Internet")
        print("7. Other")
        
        category_map = {
            '1': 'Maintenance',
            '2': 'Food/Mess',
            '3': 'Cleanliness',
            '4': 'Noise/Disturbance',
            '5': 'Security',
            '6': 'Wi-Fi/Internet',
            '7': 'Other'
        }
        
        choice = self.get_input("\nSelect category (1-7)")
        
        if choice not in category_map:
            print("\n❌ Invalid choice.")
            input("\nPress Enter to continue...")
            return
        
        category = category_map[choice]
        description = self.get_input("\nDescribe your complaint in detail")
        
        if not description:
            print("\n❌ Complaint description cannot be empty.")
            input("\nPress Enter to continue...")
            return
        
        # Generate complaint ID
        complaints = self.data_manager.load_complaints()
        complaint_id = f"C{len(complaints) + 1:04d}"
        
        new_complaint = Complaint(
            complaint_id,
            self.current_user.username,
            category,
            description
        )
        
        complaints.append(new_complaint)
        self.data_manager.save_complaints([c.to_dict() for c in complaints])
        
        print(f"\n✅ Complaint submitted successfully!")
        print(f"   Complaint ID: {complaint_id}")
        print(f"   Status: Open")
        print("\n   Your complaint will be reviewed by the warden soon.")
        
        input("\nPress Enter to return to menu...")
    
    def view_my_complaints(self):
        """View user's complaints (Resident)"""
        self.clear_screen()
        self.print_header("MY COMPLAINTS")
        
        complaints = self.data_manager.load_complaints()
        my_complaints = [c for c in complaints if c.username == self.current_user.username]
        
        if not my_complaints:
            print("\n📝 You haven't submitted any complaints yet.")
        else:
            for complaint in my_complaints:
                status_emoji = "✅" if complaint.status == "Resolved" else "⏳"
                print(f"\n{status_emoji} ID: {complaint.complaint_id}")
                print(f"   Category: {complaint.category}")
                print(f"   Description: {complaint.description}")
                print(f"   Status: {complaint.status}")
                print(f"   Submitted: {complaint.submitted_date}")
                if complaint.resolved_date:
                    print(f"   Resolved: {complaint.resolved_date}")
                self.print_separator()
        
        input("\nPress Enter to return to menu...")
    
    def mark_attendance(self):
        """Mark daily attendance (Resident)"""
        self.clear_screen()
        self.print_header("MARK ATTENDANCE")
        
        today = datetime.now().strftime("%Y-%m-%d")
        attendance_records = self.data_manager.load_attendance()
        
        # Check if already marked today
        already_marked = any(
            record['username'] == self.current_user.username and record['date'] == today
            for record in attendance_records
        )
        
        if already_marked:
            print(f"\n✅ You have already marked attendance for today ({today}).")
        else:
            new_record = {
                'username': self.current_user.username,
                'date': today,
                'time': datetime.now().strftime("%H:%M:%S"),
                'status': 'Present'
            }
            attendance_records.append(new_record)
            self.data_manager.save_attendance(attendance_records)
            
            print(f"\n✅ Attendance marked successfully for {today}!")
            print(f"   Time: {new_record['time']}")
        
        input("\nPress Enter to return to menu...")
    
    def view_room_details(self):
        """View room details (Resident)"""
        self.clear_screen()
        self.print_header("MY ROOM DETAILS")
        
        if not self.current_user.room_number:
            print("\n❌ No room assigned to you yet.")
            input("\nPress Enter to return to menu...")
            return
        
        rooms = self.data_manager.load_rooms()
        room = next((r for r in rooms if r.room_number == self.current_user.room_number), None)
        
        if not room:
            print("\n❌ Room information not found.")
            input("\nPress Enter to return to menu...")
            return
        
        print(f"\n🏠 Room Number: {room.room_number}")
        print(f"👥 Capacity: {room.capacity}")
        print(f"👤 Occupied: {room.occupied}")
        print(f"🛏️ Available Beds: {room.capacity - room.occupied}")
        
        if room.residents:
            print(f"\n👭 Roommates:")
            users = self.data_manager.load_users()
            for resident_username in room.residents:
                user = next((u for u in users if u.username == resident_username), None)
                if user and user.username != self.current_user.username:
                    print(f"   • {user.full_name or resident_username}")
        
        input("\n\nPress Enter to return to menu...")
    
    def submit_feedback(self):
        """Submit feedback (Resident)"""
        self.clear_screen()
        self.print_header("SUBMIT FEEDBACK")
        
        print("\n💬 We value your feedback! Please share your thoughts.")
        print("\nFeedback Categories:")
        print("1. Hostel Facilities")
        print("2. Food Quality")
        print("3. Staff Behavior")
        print("4. Cleanliness")
        print("5. Security")
        print("6. General Suggestions")
        
        category_map = {
            '1': 'Facilities',
            '2': 'Food',
            '3': 'Staff',
            '4': 'Cleanliness',
            '5': 'Security',
            '6': 'General'
        }
        
        choice = self.get_input("\nSelect category (1-6)")
        
        if choice not in category_map:
            print("\n❌ Invalid choice.")
            input("\nPress Enter to continue...")
            return
        
        feedback_text = self.get_input("\nYour feedback")
        
        if not feedback_text:
            print("\n❌ Feedback cannot be empty.")
            input("\nPress Enter to continue...")
            return
        
        rating = self.get_input("Rate your experience (1-5)")
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except ValueError:
            print("\n❌ Invalid rating. Please enter a number between 1-5.")
            input("\nPress Enter to continue...")
            return
        
        feedback_records = self.data_manager.load_feedback()
        
        new_feedback = {
            'username': self.current_user.username,
            'category': category_map[choice],
            'feedback': feedback_text,
            'rating': rating,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        feedback_records.append(new_feedback)
        self.data_manager.save_feedback(feedback_records)
        
        print("\n✅ Thank you for your feedback! We appreciate your input.")
        
        input("\nPress Enter to return to menu...")
    
    def view_all_complaints_warden(self):
        """View all complaints (Warden)"""
        self.clear_screen()
        self.print_header("ALL COMPLAINTS")
        
        complaints = self.data_manager.load_complaints()
        
        if not complaints:
            print("\n📝 No complaints registered yet.")
        else:
            # Separate by status
            open_complaints = [c for c in complaints if c.status == "Open"]
            resolved_complaints = [c for c in complaints if c.status == "Resolved"]
            
            print(f"\n⏳ OPEN COMPLAINTS ({len(open_complaints)}):\n")
            for complaint in open_complaints:
                print(f"ID: {complaint.complaint_id} | Category: {complaint.category}")
                print(f"User: {complaint.username} | Date: {complaint.submitted_date}")
                print(f"Description: {complaint.description}")
                self.print_separator()
            
            print(f"\n✅ RESOLVED COMPLAINTS ({len(resolved_complaints)}):\n")
            for complaint in resolved_complaints[:5]:  # Show last 5
                print(f"ID: {complaint.complaint_id} | Category: {complaint.category}")
                print(f"Resolved: {complaint.resolved_date}")
                self.print_separator()
        
        input("\nPress Enter to return to menu...")
    
    def resolve_complaints(self):
        """Resolve complaints (Warden)"""
        self.clear_screen()
        self.print_header("RESOLVE COMPLAINTS")
        
        complaints = self.data_manager.load_complaints()
        open_complaints = [c for c in complaints if c.status == "Open"]
        
        if not open_complaints:
            print("\n✅ No open complaints at the moment.")
            input("\nPress Enter to return to menu...")
            return
        
        print("\n⏳ OPEN COMPLAINTS:\n")
        for i, complaint in enumerate(open_complaints, 1):
            print(f"{i}. ID: {complaint.complaint_id}")
            print(f"   Category: {complaint.category} | User: {complaint.username}")
            print(f"   Description: {complaint.description}")
            self.print_separator()
        
        choice = self.get_input("\nEnter complaint number to resolve (or 0 to cancel)")
        
        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            if choice_num < 1 or choice_num > len(open_complaints):
                raise ValueError
            
            selected_complaint = open_complaints[choice_num - 1]
            selected_complaint.status = "Resolved"
            selected_complaint.resolved_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            self.data_manager.save_complaints([c.to_dict() for c in complaints])
            
            print(f"\n✅ Complaint {selected_complaint.complaint_id} marked as resolved!")
            
        except ValueError:
            print("\n❌ Invalid choice.")
        
        input("\nPress Enter to return to menu...")
    
    def view_attendance_report(self):
        """View attendance report (Warden)"""
        self.clear_screen()
        self.print_header("ATTENDANCE REPORT")
        
        attendance_records = self.data_manager.load_attendance()
        
        if not attendance_records:
            print("\n📝 No attendance records found.")
            input("\nPress Enter to return to menu...")
            return
        
        # Get last 7 days
        today = datetime.now()
        last_7_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        
        print("\n📅 LAST 7 DAYS ATTENDANCE:\n")
        
        users = self.data_manager.load_users()
        residents = [u for u in users if u.role == "resident"]
        
        for date in last_7_days:
            present_count = sum(1 for r in attendance_records if r['date'] == date)
            print(f"{date}: {present_count}/{len(residents)} present")
        
        print("\n\n👥 TODAY'S ATTENDANCE:\n")
        today_str = today.strftime("%Y-%m-%d")
        today_records = [r for r in attendance_records if r['date'] == today_str]
        
        if today_records:
            for record in today_records:
                user = next((u for u in users if u.username == record['username']), None)
                name = user.full_name if user else record['username']
                print(f"✅ {name} - {record['time']}")
        else:
            print("No attendance marked today yet.")
        
        input("\n\nPress Enter to return to menu...")
    
    def view_room_allocation(self):
        """View room allocation (Warden)"""
        self.clear_screen()
        self.print_header("ROOM ALLOCATION")
        
        rooms = self.data_manager.load_rooms()
        users = self.data_manager.load_users()
        
        print("\n🏠 ROOM STATUS:\n")
        
        for room in rooms:
            status = "Available" if room.is_available() else "Full"
            status_emoji = "🟢" if room.is_available() else "🔴"
            
            print(f"{status_emoji} Room {room.room_number}: {room.occupied}/{room.capacity} - {status}")
            
            if room.residents:
                print("   Residents:")
                for resident_username in room.residents:
                    user = next((u for u in users if u.username == resident_username), None)
                    name = user.full_name if user else resident_username
                    print(f"   • {name}")
            
            self.print_separator()
        
        input("\nPress Enter to return to menu...")
    
    def view_feedback_warden(self):
        """View all feedback (Warden)"""
        self.clear_screen()
        self.print_header("USER FEEDBACK")
        
        feedback_records = self.data_manager.load_feedback()
        
        if not feedback_records:
            print("\n💬 No feedback submitted yet.")
        else:
            print(f"\n📊 Total Feedback: {len(feedback_records)}\n")
            
            for i, feedback in enumerate(feedback_records[-10:], 1):  # Show last 10
                stars = "⭐" * feedback['rating']
                print(f"{i}. {feedback['username']} - {feedback['category']}")
                print(f"   Rating: {stars} ({feedback['rating']}/5)")
                print(f"   Feedback: {feedback['feedback']}")
                print(f"   Date: {feedback['date']}")
                self.print_separator()
        
        input("\nPress Enter to return to menu...")
    
    def show_statistics_dashboard(self):
        """Show statistics dashboard (Warden/Admin)"""
        self.clear_screen()
        self.print_header("STATISTICS DASHBOARD")
        
        complaints = self.data_manager.load_complaints()
        attendance_records = self.data_manager.load_attendance()
        feedback_records = self.data_manager.load_feedback()
        rooms = self.data_manager.load_rooms()
        users = self.data_manager.load_users()
        
        residents = [u for u in users if u.role == "resident"]
        
        # Complaint statistics
        open_complaints = [c for c in complaints if c.status == "Open"]
        resolved_complaints = [c for c in complaints if c.status == "Resolved"]
        
        # Room statistics
        total_capacity = sum(r.capacity for r in rooms)
        total_occupied = sum(r.occupied for r in rooms)
        
        # Attendance statistics (today)
        today = datetime.now().strftime("%Y-%m-%d")
        today_attendance = sum(1 for r in attendance_records if r['date'] == today)
        
        # Feedback statistics
        if feedback_records:
            avg_rating = sum(f['rating'] for f in feedback_records) / len(feedback_records)
        else:
            avg_rating = 0
        
        print("\n📊 HOSTEL STATISTICS:\n")
        print(f"👥 Total Residents: {len(residents)}")
        print(f"🏠 Total Rooms: {len(rooms)}")
        print(f"🛏️  Room Occupancy: {total_occupied}/{total_capacity} ({(total_occupied/total_capacity*100):.1f}%)")
        print(f"\n📋 Complaints:")
        print(f"   Total: {len(complaints)}")
        print(f"   Open: {len(open_complaints)}")
        print(f"   Resolved: {len(resolved_complaints)}")
        
        if complaints:
            resolution_rate = (len(resolved_complaints) / len(complaints)) * 100
            print(f"   Resolution Rate: {resolution_rate:.1f}%")
        
        print(f"\n📅 Attendance (Today):")
        print(f"   Present: {today_attendance}/{len(residents)}")
        if residents:
            attendance_rate = (today_attendance / len(residents)) * 100
            print(f"   Attendance Rate: {attendance_rate:.1f}%")
        
        print(f"\n💬 Feedback:")
        print(f"   Total Submissions: {len(feedback_records)}")
        print(f"   Average Rating: {avg_rating:.1f}/5.0 {'⭐' * int(avg_rating)}")
        
        # Category breakdown
        if complaints:
            print(f"\n📊 Complaint Categories:")
            from collections import Counter
            categories = Counter(c.category for c in complaints)
            for category, count in categories.most_common():
                print(f"   {category}: {count}")
        
        input("\n\nPress Enter to return to menu...")
    
    def manage_users_admin(self):
        """Manage users (Admin)"""
        self.clear_screen()
        self.print_header("USER MANAGEMENT")
        
        print("\n1. Add New User")
        print("2. View All Users")
        print("3. Delete User")
        print("4. Back to Main Menu")
        
        choice = self.get_input("\nSelect option (1-4)")
        
        if choice == '1':
            self.add_new_user()
        elif choice == '2':
            self.view_all_users()
        elif choice == '3':
            self.delete_user()
    
    def add_new_user(self):
        """Add new user (Admin)"""
        self.clear_screen()
        self.print_header("ADD NEW USER")
        
        username = self.get_input("Username")
        password = self.get_input("Password")
        full_name = self.get_input("Full Name")
        
        print("\nRole:")
        print("1. Resident")
        print("2. Warden")
        print("3. Admin")
        
        role_choice = self.get_input("Select role (1-3)")
        role_map = {'1': 'resident', '2': 'warden', '3': 'admin'}
        
        if role_choice not in role_map:
            print("\n❌ Invalid role.")
            input("\nPress Enter to continue...")
            return
        
        role = role_map[role_choice]
        room_number = None
        
        if role == 'resident':
            room_number = self.get_input("Room Number (optional, press Enter to skip)")
            if not room_number:
                room_number = None
        
        users = self.data_manager.load_users()
        
        # Check if username exists
        if any(u.username == username for u in users):
            print(f"\n❌ Username '{username}' already exists.")
            input("\nPress Enter to continue...")
            return
        
        new_user = User(username, password, role, room_number, full_name)
        users.append(new_user)
        self.data_manager.save_users([u.to_dict() for u in users])
        
        print(f"\n✅ User '{username}' added successfully!")
        
        input("\nPress Enter to continue...")
    
    def view_all_users(self):
        """View all users (Admin)"""
        self.clear_screen()
        self.print_header("ALL USERS")
        
        users = self.data_manager.load_users()
        
        for role in ['admin', 'warden', 'resident']:
            role_users = [u for u in users if u.role == role]
            if role_users:
                print(f"\n👤 {role.upper()}S ({len(role_users)}):\n")
                for user in role_users:
                    room_info = f" | Room: {user.room_number}" if user.room_number else ""
                    print(f"   • {user.full_name or user.username} ({user.username}){room_info}")
                self.print_separator()
        
        input("\nPress Enter to continue...")
    
    def delete_user(self):
        """Delete user (Admin)"""
        self.clear_screen()
        self.print_header("DELETE USER")
        
        username = self.get_input("Enter username to delete")
        
        users = self.data_manager.load_users()
        user_to_delete = next((u for u in users if u.username == username), None)
        
        if not user_to_delete:
            print(f"\n❌ User '{username}' not found.")
            input("\nPress Enter to continue...")
            return
        
        if user_to_delete.username == self.current_user.username:
            print("\n❌ You cannot delete yourself!")
            input("\nPress Enter to continue...")
            return
        
        confirm = self.get_input(f"Are you sure you want to delete '{username}'? (yes/no)")
        
        if confirm.lower() == 'yes':
            users = [u for u in users if u.username != username]
            self.data_manager.save_users([u.to_dict() for u in users])
            print(f"\n✅ User '{username}' deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")
        
        input("\nPress Enter to continue...")
    
    def manage_rooms_admin(self):
        """Manage rooms (Admin)"""
        self.clear_screen()
        self.print_header("ROOM MANAGEMENT")
        
        print("\n1. Add New Room")
        print("2. View All Rooms")
        print("3. Allocate Room to User")
        print("4. Back to Main Menu")
        
        choice = self.get_input("\nSelect option (1-4)")
        
        if choice == '1':
            self.add_new_room()
        elif choice == '2':
            self.view_all_rooms()
        elif choice == '3':
            self.allocate_room()
    
    def add_new_room(self):
        """Add new room (Admin)"""
        self.clear_screen()
        self.print_header("ADD NEW ROOM")
        
        room_number = self.get_input("Room Number")
        capacity = self.get_input("Capacity (number of beds)")
        
        try:
            capacity = int(capacity)
            if capacity < 1:
                raise ValueError
        except ValueError:
            print("\n❌ Invalid capacity.")
            input("\nPress Enter to continue...")
            return
        
        rooms = self.data_manager.load_rooms()
        
        if any(r.room_number == room_number for r in rooms):
            print(f"\n❌ Room '{room_number}' already exists.")
            input("\nPress Enter to continue...")
            return
        
        new_room = Room(room_number, capacity)
        rooms.append(new_room)
        self.data_manager.save_rooms([r.to_dict() for r in rooms])
        
        print(f"\n✅ Room '{room_number}' added successfully!")
        
        input("\nPress Enter to continue...")
    
    def view_all_rooms(self):
        """View all rooms (Admin)"""
        self.view_room_allocation()
    
    def allocate_room(self):
        """Allocate room to user (Admin)"""
        self.clear_screen()
        self.print_header("ALLOCATE ROOM")
        
        username = self.get_input("Enter username")
        room_number = self.get_input("Enter room number")
        
        users = self.data_manager.load_users()
        rooms = self.data_manager.load_rooms()
        
        user = next((u for u in users if u.username == username), None)
        room = next((r for r in rooms if r.room_number == room_number), None)
        
        if not user:
            print(f"\n❌ User '{username}' not found.")
            input("\nPress Enter to continue...")
            return
        
        if not room:
            print(f"\n❌ Room '{room_number}' not found.")
            input("\nPress Enter to continue...")
            return
        
        if not room.is_available():
            print(f"\n❌ Room '{room_number}' is full.")
            input("\nPress Enter to continue...")
            return
        
        # Update user
        user.room_number = room_number
        
        # Update room
        if username not in room.residents:
            room.residents.append(username)
            room.occupied += 1
        
        self.data_manager.save_users([u.to_dict() for u in users])
        self.data_manager.save_rooms([r.to_dict() for r in rooms])
        
        print(f"\n✅ Room '{room_number}' allocated to '{username}'!")
        
        input("\nPress Enter to continue...")
    
    def update_mess_menu_admin(self):
        """Update mess menu (Admin)"""
        self.clear_screen()
        self.print_header("UPDATE MESS MENU")
        
        print("\nSelect day to update:")
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for i, day in enumerate(days, 1):
            print(f"{i}. {day}")
        
        choice = self.get_input("\nSelect day (1-7)")
        
        try:
            day_index = int(choice) - 1
            if day_index < 0 or day_index >= 7:
                raise ValueError
            
            selected_day = days[day_index]
            
            print(f"\nUpdating menu for {selected_day}:")
            breakfast = self.get_input("Breakfast")
            lunch = self.get_input("Lunch")
            dinner = self.get_input("Dinner")
            
            menu = self.data_manager.load_menu()
            menu[selected_day] = {
                'breakfast': breakfast,
                'lunch': lunch,
                'dinner': dinner
            }
            self.data_manager.save_menu(menu)
            
            print(f"\n✅ Menu for {selected_day} updated successfully!")
            
        except ValueError:
            print("\n❌ Invalid choice.")
        
        input("\nPress Enter to continue...")
    
    def add_event_admin(self):
        """Add new event (Admin)"""
        self.clear_screen()
        self.print_header("ADD NEW EVENT")
        
        title = self.get_input("Event Title")
        description = self.get_input("Event Description")
        date = self.get_input("Event Date (YYYY-MM-DD)")
        time = self.get_input("Event Time (HH:MM)")
        venue = self.get_input("Venue")
        
        events = self.data_manager.load_events()
        event_id = f"E{len(events) + 1:04d}"
        
        new_event = Event(event_id, title, description, date, time, venue)
        events.append(new_event)
        self.data_manager.save_events([e.to_dict() for e in events])
        
        print(f"\n✅ Event '{title}' added successfully!")
        print(f"   Event ID: {event_id}")
        
        input("\nPress Enter to continue...")
    
    def handle_menu_choice(self, choice: str):
        """Handle menu selection based on user role"""
        
        # Common options (1-6)
        if choice == '1':
            self.view_hostel_info()
        elif choice == '2':
            self.view_mess_menu()
        elif choice == '3':
            self.view_events()
        elif choice == '4':
            self.show_emergency_contacts()
        elif choice == '5':
            self.show_wellness_tips()
        elif choice == '6':
            self.show_daily_motivation()
        
        # Role-specific options
        elif self.current_user.role == "resident":
            if choice == '7':
                self.submit_complaint()
            elif choice == '8':
                self.view_my_complaints()
            elif choice == '9':
                self.mark_attendance()
            elif choice == '10':
                self.view_room_details()
            elif choice == '11':
                self.submit_feedback()
            elif choice == '12':
                return False  # Logout
        
        elif self.current_user.role == "warden":
            if choice == '7':
                self.view_all_complaints_warden()
            elif choice == '8':
                self.resolve_complaints()
            elif choice == '9':
                self.view_attendance_report()
            elif choice == '10':
                self.view_room_allocation()
            elif choice == '11':
                self.view_feedback_warden()
            elif choice == '12':
                self.show_statistics_dashboard()
            elif choice == '13':
                return False  # Logout
        
        elif self.current_user.role == "admin":
            if choice == '7':
                self.manage_users_admin()
            elif choice == '8':
                self.manage_rooms_admin()
            elif choice == '9':
                self.update_mess_menu_admin()
            elif choice == '10':
                self.add_event_admin()
            elif choice == '11':
                self.view_all_complaints_warden()
            elif choice == '12':
                self.view_feedback_warden()
            elif choice == '13':
                self.show_statistics_dashboard()
            elif choice == '14':
                return False  # Logout
        
        return True  # Continue in menu
    
    def run(self):
        """Main chatbot loop"""
        self.show_welcome()
        
        while self.running:
            # Authentication loop
            if not self.current_user:
                if not self.authenticate():
                    break
                continue
            
            # Main menu loop
            self.show_main_menu()
            choice = self.get_input("\nEnter your choice")
            
            if choice.lower() in ['exit', 'quit']:
                print("\n👋 Thank you for using HostelHelper! Take care, sister! 💖")
                break
            
            elif choice.lower() == 'help':
                self.clear_screen()
                print("\n📖 HELP MENU")
                print("\n• Navigate using the menu numbers")
                print("• Type 'exit' or 'quit' to leave the chatbot")
                print("• Type 'help' anytime to see this message")
                print("• Your data is saved automatically")
                print("\n💡 Tips:")
                print("  - Check daily for new events and announcements")
                print("  - Submit complaints for quick resolution")
                print("  - Mark attendance daily")
                print("  - Share feedback to help us improve!")
                input("\n\nPress Enter to continue...")
                continue
            
            # Handle menu choice
            continue_menu = self.handle_menu_choice(choice)
            
            if not continue_menu:
                self.current_user = None
                print("\n✅ Logged out successfully!")
                input("\nPress Enter to continue...")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        chatbot = HostelHelper()
        chatbot.run()
    except KeyboardInterrupt:
        print("\n\n👋 HostelHelper terminated. Stay safe and empowered! 💪✨")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please restart the application.")
