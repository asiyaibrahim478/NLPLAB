"""
Girls' Hostel Chatbot - Complete Console Application
A friendly, supportive chatbot system for managing hostel activities
Run with: python app.py
"""

import json
import os
from datetime import datetime
import random

# ============================================================================
# DATA PERSISTENCE FUNCTIONS
# ============================================================================

def load_json_file(filename):
    """Load data from a JSON file, return empty list if file doesn't exist"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_json_file(filename, data):
    """Save data to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ============================================================================
# HARDCODED DATA
# ============================================================================

HOSTEL_RULES = [
    "🕐 Curfew time is 9:00 PM on weekdays and 10:00 PM on weekends",
    "🔇 Maintain silence after 10:00 PM",
    "🚫 No outside guests allowed in rooms",
    "🧹 Keep your room and common areas clean",
    "💡 Switch off lights and fans when leaving the room",
    "🍽️ Mess timings: Breakfast (7-9 AM), Lunch (12-2 PM), Dinner (7-9 PM)",
    "👗 Dress modestly in common areas",
    "🚿 Use water responsibly",
    "📱 Keep valuables secure - hostel is not responsible for lost items",
    "💞 Be respectful and kind to your hostel mates"
]

EMERGENCY_CONTACTS = {
    "🏥 Hostel Warden": "0300-1234567",
    "👮 Security Guard": "0300-7654321",
    "🚑 Medical Emergency": "0300-9876543",
    "🔥 Fire Emergency": "115",
    "👮 Police": "15",
    "🏥 Campus Clinic": "0300-1112223",
    "🔧 Maintenance": "0300-3334445"
}

WEEKLY_MESS_MENU = {
    "Monday": {
        "Breakfast": "Paratha, Yogurt, Tea ☕",
        "Lunch": "Rice, Daal, Chicken Curry, Salad 🍛",
        "Dinner": "Roti, Mixed Vegetables, Raita 🥗"
    },
    "Tuesday": {
        "Breakfast": "Halwa Puri, Chanay, Tea ☕",
        "Lunch": "Biryani, Raita, Salad 🍚",
        "Dinner": "Roti, Daal Mash, Fried Fish 🐟"
    },
    "Wednesday": {
        "Breakfast": "Omelet, Bread, Tea ☕",
        "Lunch": "Rice, Daal, Vegetable Qorma, Salad 🥘",
        "Dinner": "Roti, Palak Gosht, Raita 🍲"
    },
    "Thursday": {
        "Breakfast": "Paratha, Fried Egg, Tea ☕",
        "Lunch": "Pulao, Chicken Karahi, Salad 🍗",
        "Dinner": "Roti, Mixed Daal, Potato Curry 🥔"
    },
    "Friday": {
        "Breakfast": "Nihari, Naan, Tea ☕",
        "Lunch": "Rice, Daal, Beef Qeema, Salad 🍖",
        "Dinner": "Roti, Chicken Jalfrezi, Raita 🌶️"
    },
    "Saturday": {
        "Breakfast": "Aloo Paratha, Yogurt, Tea ☕",
        "Lunch": "Fried Rice, Manchurian, Salad 🍜",
        "Dinner": "Pizza/Pasta Night 🍕"
    },
    "Sunday": {
        "Breakfast": "Pancakes, Honey, Tea ☕",
        "Lunch": "Chicken Biryani, Raita, Salad 🍛",
        "Dinner": "Roti, Daal, Mixed Vegetables 🥗"
    }
}

MOTIVATIONAL_QUOTES = [
    "💪 You are stronger than you think! Keep pushing forward!",
    "✨ Believe in yourself and all that you are. You're capable of amazing things!",
    "🌟 Every day is a new opportunity to be better than yesterday!",
    "💖 You are enough, just as you are. Keep shining!",
    "🦋 Difficult roads often lead to beautiful destinations!",
    "🌈 Your potential is endless. Keep going!",
    "👑 Be a girl with a mind, a woman with attitude, and a lady with class!",
    "💝 She believed she could, so she did!",
    "🌸 Strong women lift each other up!",
    "⭐ You are the author of your own story. Make it inspiring!",
    "🎯 Focus on your goals, not your fear!",
    "💕 Be fearless in the pursuit of what sets your soul on fire!",
    "🌺 Empower yourself! You have the power to change your life!",
    "🎓 Education is the most powerful weapon you can use to change the world!",
    "💎 You are precious, unique, and irreplaceable!"
]

HEALTH_STUDY_TIPS = [
    "💧 Drink at least 8 glasses of water daily to stay hydrated!",
    "🥗 Eat plenty of fruits and vegetables for better concentration!",
    "😴 Get 7-8 hours of sleep for optimal brain function!",
    "🏃 Exercise for 30 minutes daily - even a walk helps!",
    "📚 Study in 25-minute focused sessions (Pomodoro Technique)!",
    "🧘 Practice meditation or deep breathing to reduce stress!",
    "📝 Make a to-do list every morning to stay organized!",
    "🎧 Listen to calming music while studying for better focus!",
    "👭 Form study groups with friends for better understanding!",
    "📱 Take breaks from screens to protect your eyes!",
    "🍎 Never skip breakfast - it's fuel for your brain!",
    "📖 Read for 20 minutes before bed to improve sleep quality!",
    "🌞 Get some sunlight every day for Vitamin D!",
    "🧠 Practice active recall instead of just re-reading notes!",
    "💆 Take care of your mental health - talk to someone if stressed!"
]

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def print_header(text):
    """Print a decorative header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_separator():
    """Print a separator line"""
    print("-" * 60)

def press_enter():
    """Wait for user to press Enter"""
    input("\n✨ Press Enter to continue...")

# ============================================================================
# FEATURE FUNCTIONS
# ============================================================================

def view_hostel_rules():
    """Display hostel rules"""
    print_header("📋 HOSTEL RULES & REGULATIONS")
    print("\n💝 Dear Resident, please follow these rules for a harmonious living:\n")
    for i, rule in enumerate(HOSTEL_RULES, 1):
        print(f"  {i}. {rule}")
    print("\n💕 Thank you for your cooperation!")
    press_enter()

def show_mess_menu():
    """Display today's mess menu"""
    print_header("🍽️ TODAY'S MESS MENU")
    
    # Get current day of week
    today = datetime.now().strftime("%A")
    
    if today in WEEKLY_MESS_MENU:
        menu = WEEKLY_MESS_MENU[today]
        print(f"\n📅 Day: {today}\n")
        print(f"  🌅 Breakfast: {menu['Breakfast']}")
        print(f"  ☀️ Lunch: {menu['Lunch']}")
        print(f"  🌙 Dinner: {menu['Dinner']}")
        print("\n🥘 Enjoy your meal!")
    else:
        print("\n❌ Menu not available for today.")
    
    press_enter()

def submit_complaint():
    """Submit a new complaint"""
    print_header("📝 SUBMIT A COMPLAINT")
    
    print("\n💬 We're here to help! Please share your concern:\n")
    
    try:
        name = input("  👤 Your Name: ").strip()
        if not name:
            print("\n❌ Name cannot be empty!")
            press_enter()
            return
        
        room = input("  🚪 Room Number: ").strip()
        if not room:
            print("\n❌ Room number cannot be empty!")
            press_enter()
            return
        
        complaint = input("  💭 Your Complaint: ").strip()
        if not complaint:
            print("\n❌ Complaint cannot be empty!")
            press_enter()
            return
        
        # Load existing complaints
        complaints = load_json_file('complaints.json')
        
        # Create new complaint
        new_complaint = {
            "id": len(complaints) + 1,
            "name": name,
            "room": room,
            "complaint": complaint,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Pending"
        }
        
        complaints.append(new_complaint)
        save_json_file('complaints.json', complaints)
        
        print("\n✅ Your complaint has been submitted successfully!")
        print("📌 We'll address it as soon as possible.")
        print("💝 Thank you for bringing this to our attention!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    press_enter()

def view_upcoming_events():
    """Display upcoming events"""
    print_header("🎉 UPCOMING EVENTS")
    
    events = load_json_file('events.json')
    
    if not events:
        print("\n📅 No upcoming events scheduled at the moment.")
        print("💭 Check back later for exciting updates!")
    else:
        print("\n🌟 Here's what's coming up:\n")
        for i, event in enumerate(events, 1):
            print(f"  {i}. 🎊 {event['name']}")
            print(f"     📅 Date: {event['date']}")
            print(f"     📝 Details: {event['details']}")
            print_separator()
    
    press_enter()

def mark_attendance():
    """Mark daily attendance"""
    print_header("✅ MARK ATTENDANCE")
    
    print("\n📋 Daily attendance system\n")
    
    try:
        name = input("  👤 Your Name: ").strip()
        if not name:
            print("\n❌ Name cannot be empty!")
            press_enter()
            return
        
        room = input("  🚪 Room Number: ").strip()
        if not room:
            print("\n❌ Room number cannot be empty!")
            press_enter()
            return
        
        # Load existing attendance
        attendance_records = load_json_file('attendance.json')
        
        # Check if already marked today
        today = datetime.now().strftime("%Y-%m-%d")
        already_marked = any(
            record['name'].lower() == name.lower() and 
            record['date'] == today 
            for record in attendance_records
        )
        
        if already_marked:
            print("\n⚠️ You've already marked your attendance today!")
            print("💝 See you tomorrow!")
        else:
            # Create new attendance record
            new_record = {
                "name": name,
                "room": room,
                "date": today,
                "time": datetime.now().strftime("%H:%M:%S")
            }
            
            attendance_records.append(new_record)
            save_json_file('attendance.json', attendance_records)
            
            print("\n✅ Attendance marked successfully!")
            print(f"📅 Date: {today}")
            print(f"⏰ Time: {new_record['time']}")
            print("💕 Have a wonderful day!")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    press_enter()

def show_emergency_contacts():
    """Display emergency contacts"""
    print_header("🚨 EMERGENCY CONTACTS")
    
    print("\n📞 Save these numbers for emergencies:\n")
    
    for contact, number in EMERGENCY_CONTACTS.items():
        print(f"  {contact}: {number}")
    
    print("\n💝 Stay safe! Don't hesitate to call if you need help.")
    press_enter()

def show_motivational_quote():
    """Display a random motivational quote"""
    print_header("💖 MOTIVATION BOOST")
    
    quote = random.choice(MOTIVATIONAL_QUOTES)
    
    print("\n" + "🌟" * 20)
    print(f"\n  {quote}\n")
    print("🌟" * 20)
    
    print("\n💕 You've got this, girl! Keep shining!")
    press_enter()

def show_health_tip():
    """Display a random health/study tip"""
    print_header("🌸 HEALTH & STUDY TIP")
    
    tip = random.choice(HEALTH_STUDY_TIPS)
    
    print("\n" + "💚" * 20)
    print(f"\n  {tip}\n")
    print("💚" * 20)
    
    print("\n🌺 Take care of yourself - you deserve it!")
    press_enter()

def view_all_complaints():
    """Admin view - display all complaints"""
    print_header("📊 ALL COMPLAINTS (Admin View)")
    
    complaints = load_json_file('complaints.json')
    
    if not complaints:
        print("\n✨ No complaints submitted yet!")
        print("💝 Everything is running smoothly!")
    else:
        print(f"\n📋 Total Complaints: {len(complaints)}\n")
        for complaint in complaints:
            print(f"  ID: {complaint['id']}")
            print(f"  👤 Name: {complaint['name']}")
            print(f"  🚪 Room: {complaint['room']}")
            print(f"  💭 Complaint: {complaint['complaint']}")
            print(f"  📅 Date: {complaint['date']}")
            print(f"  📌 Status: {complaint['status']}")
            print_separator()
    
    press_enter()

def add_new_event():
    """Admin function - add a new event"""
    print_header("➕ ADD NEW EVENT (Admin)")
    
    print("\n🎉 Let's add an exciting event!\n")
    
    try:
        event_name = input("  🎊 Event Name: ").strip()
        if not event_name:
            print("\n❌ Event name cannot be empty!")
            press_enter()
            return
        
        event_date = input("  📅 Event Date (e.g., 2025-01-15): ").strip()
        if not event_date:
            print("\n❌ Event date cannot be empty!")
            press_enter()
            return
        
        event_details = input("  📝 Event Details: ").strip()
        if not event_details:
            print("\n❌ Event details cannot be empty!")
            press_enter()
            return
        
        # Load existing events
        events = load_json_file('events.json')
        
        # Create new event
        new_event = {
            "name": event_name,
            "date": event_date,
            "details": event_details,
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        events.append(new_event)
        save_json_file('events.json', events)
        
        print("\n✅ Event added successfully!")
        print("🎊 Students will be excited to see this!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    press_enter()

def show_main_menu():
    """Display the main menu"""
    print_header("🏠 GIRLS' HOSTEL CHATBOT - MAIN MENU")
    
    print("\n💕 Welcome! How can I help you today?\n")
    
    menu_options = [
        "View Hostel Rules",
        "Today's Mess Menu",
        "Submit a Complaint",
        "View Upcoming Events",
        "Mark Attendance",
        "Emergency Contacts",
        "Get Motivational Quote",
        "Health & Study Tip",
        "View All Complaints (Admin)",
        "Add New Event (Admin)",
        "Exit"
    ]
    
    for i, option in enumerate(menu_options, 1):
        emoji = ["📋", "🍽️", "📝", "🎉", "✅", "🚨", "💖", "🌸", "📊", "➕", "👋"][i-1]
        print(f"  {i}. {emoji} {option}")
    
    print("\n" + "=" * 60)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application loop"""
    print("\n" + "🌟" * 30)
    print("  💝 Welcome to Girls' Hostel Management System 💝")
    print("🌟" * 30)
    print("\n✨ Your comfort and safety are our priorities!")
    print("💕 Feel free to use any feature below.\n")
    
    press_enter()
    
    while True:
        show_main_menu()
        
        try:
            choice = input("\n💬 Enter your choice (1-11): ").strip()
            
            if choice == '1':
                view_hostel_rules()
            elif choice == '2':
                show_mess_menu()
            elif choice == '3':
                submit_complaint()
            elif choice == '4':
                view_upcoming_events()
            elif choice == '5':
                mark_attendance()
            elif choice == '6':
                show_emergency_contacts()
            elif choice == '7':
                show_motivational_quote()
            elif choice == '8':
                show_health_tip()
            elif choice == '9':
                view_all_complaints()
            elif choice == '10':
                add_new_event()
            elif choice == '11':
                print_header("👋 GOODBYE!")
                print("\n💕 Thank you for using the Girls' Hostel Chatbot!")
                print("✨ Have a wonderful day!")
                print("🌟 Stay safe and keep shining!\n")
                break
            else:
                print("\n❌ Invalid choice! Please enter a number between 1 and 11.")
                press_enter()
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Take care! 💕\n")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("💭 Please try again!")
            press_enter()

if __name__ == "__main__":
    main()
