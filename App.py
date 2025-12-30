import streamlit as st
import json
import os
from datetime import datetime, date
import random

# ============================================================================
# CONFIGURATION & DATA INITIALIZATION
# ============================================================================

# File paths for persistent storage
COMPLAINTS_FILE = "complaints.json"
ATTENDANCE_FILE = "attendance.json"
EVENTS_FILE = "events.json"

# Hardcoded data
HOSTEL_RULES = [
    "🕐 Curfew time is 10:00 PM on weekdays and 11:00 PM on weekends",
    "🔇 Maintain silence after 11:00 PM to respect others' study time",
    "👭 Visitors are allowed only in the common room between 4:00 PM - 8:00 PM",
    "🧹 Keep your room and common areas clean and tidy",
    "🍽️ Inform the mess in-charge 2 hours in advance if you'll miss a meal",
    "💧 Report any maintenance issues immediately to the warden",
    "🚫 Smoking, alcohol, and drugs are strictly prohibited",
    "🎵 Use headphones when listening to music or watching videos",
    "👗 Proper attire must be worn in common areas",
    "💝 Be kind, supportive, and respectful to all hostel sisters"
]

WEEKLY_MENU = {
    "Monday": {
        "Breakfast": "Aloo Paratha, Curd, Pickle, Tea/Coffee",
        "Lunch": "Dal Makhani, Jeera Rice, Roti, Mix Veg, Salad",
        "Dinner": "Rajma, Rice, Roti, Paneer Butter Masala, Gulab Jamun"
    },
    "Tuesday": {
        "Breakfast": "Poha, Banana, Tea/Coffee",
        "Lunch": "Chole, Rice, Roti, Aloo Gobi, Raita",
        "Dinner": "Dal Fry, Rice, Roti, Bhindi Masala, Curd"
    },
    "Wednesday": {
        "Breakfast": "Idli Sambhar, Coconut Chutney, Tea/Coffee",
        "Lunch": "Kadhi Pakora, Rice, Roti, Baingan Bharta, Salad",
        "Dinner": "Chana Masala, Rice, Roti, Palak Paneer, Kheer"
    },
    "Thursday": {
        "Breakfast": "Bread Butter Jam, Boiled Eggs, Tea/Coffee",
        "Lunch": "Dal Tadka, Veg Pulao, Roti, Mix Veg, Pickle",
        "Dinner": "Rajma, Rice, Chapati, Aloo Matar, Fruit Custard"
    },
    "Friday": {
        "Breakfast": "Upma, Apple, Tea/Coffee",
        "Lunch": "Sambar, Rice, Roti, Cabbage Sabzi, Papad",
        "Dinner": "Special Biryani, Raita, Paneer Tikka, Ice Cream"
    },
    "Saturday": {
        "Breakfast": "Puri Bhaji, Sweet, Tea/Coffee",
        "Lunch": "Chole Bhature, Rice, Salad, Lassi",
        "Dinner": "Dal Makhani, Jeera Rice, Naan, Kadai Paneer, Gajar Halwa"
    },
    "Sunday": {
        "Breakfast": "Sandwich, Cornflakes, Milk, Tea/Coffee",
        "Lunch": "Special Thali - Dal, Rice, Puri, 3 Sabzis, Sweet",
        "Dinner": "Chinese Special - Fried Rice, Manchurian, Spring Rolls, Soup"
    }
}

EMERGENCY_CONTACTS = [
    {"name": "Warden - Ms. Priya Sharma", "number": "📞 +91-98765-43210"},
    {"name": "Assistant Warden", "number": "📞 +91-98765-43211"},
    {"name": "Security Office", "number": "📞 +91-98765-43212"},
    {"name": "Medical Emergency", "number": "🚑 +91-98765-43213"},
    {"name": "Mess In-charge", "number": "📞 +91-98765-43214"},
    {"name": "Maintenance", "number": "🔧 +91-98765-43215"},
    {"name": "Police Emergency", "number": "🚨 100"},
    {"name": "Women's Helpline", "number": "📞 1091"},
]

MOTIVATIONAL_QUOTES = [
    "You are braver than you believe, stronger than you seem, and smarter than you think. 💪",
    "She believed she could, so she did. Keep shining, sister! ✨",
    "Your education is your superpower. Use it to change the world! 📚",
    "Strong women lift each other up. Be that woman! 🌟",
    "You are capable of amazing things. Never doubt yourself! 💖",
    "Education is the key to unlock the golden door of freedom. 🗝️",
    "Empowered women empower women. Let's grow together! 🌸",
    "Your only limit is you. Break barriers and achieve greatness! 🚀",
    "Be fearless in the pursuit of what sets your soul on fire! 🔥",
    "You are enough, just as you are. Keep being amazing! 💝"
]

HEALTH_TIPS = [
    "💧 Stay hydrated! Drink at least 8 glasses of water daily for glowing skin and better concentration.",
    "🩸 Track your period cycle and maintain good menstrual hygiene. Keep necessary supplies stocked.",
    "🧘‍♀️ Practice 10 minutes of meditation or yoga daily to reduce stress and improve focus.",
    "😴 Get 7-8 hours of sleep for better memory retention and overall health.",
    "🥗 Eat iron-rich foods like spinach, dates, and jaggery, especially during your periods.",
    "📱 Take regular breaks from screens to avoid eye strain and headaches.",
    "🚶‍♀️ Walk for 30 minutes daily - it helps with period cramps and boosts mood!",
    "🧠 Take short study breaks every 45 minutes to improve productivity and retention.",
    "💆‍♀️ Don't ignore persistent pain or discomfort. Consult the medical room immediately.",
    "🌞 Get some sunlight daily for Vitamin D - great for bones and mood!",
    "🍎 Keep healthy snacks handy to avoid junk food during late-night study sessions.",
    "💝 Talk to friends or counselors if you're feeling stressed or anxious. You're not alone!"
]

# ============================================================================
# HELPER FUNCTIONS FOR DATA PERSISTENCE
# ============================================================================

def load_json(filepath, default=None):
    """Load data from JSON file"""
    if default is None:
        default = []
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    except Exception as e:
        st.error(f"Error loading {filepath}: {e}")
        return default

def save_json(filepath, data):
    """Save data to JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving {filepath}: {e}")
        return False

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Girls Hostel Assistant",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #ffeef8 0%, #fff5f7 100%);
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%);
        color: white;
        border: none;
        border-radius: 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #fecfef 0%, #ff9a9e 100%);
    }
    h1, h2, h3 {
        color: #d63384;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #fff0f6 0%, #ffe4f1 100%);
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("<h1 style='text-align: center; color: #d63384;'>🏡 Girls Hostel Assistant 🏡</h1>", 
            unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #e685b5;'>Hello Sister! How can I help you today? 😊</h3>", 
            unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.image("https://img.icons8.com/clouds/200/null/home.png", width=150)
st.sidebar.markdown("### 💝 Navigation Menu")
st.sidebar.markdown("---")

menu_options = [
    "🏠 Home / Welcome",
    "📋 Hostel Rules",
    "🍽️ Today's Mess Menu",
    "📝 Submit Complaint",
    "👀 View Complaints",
    "✅ Mark Attendance",
    "🎉 Upcoming Events",
    "➕ Add Event",
    "🚨 Emergency Contacts",
    "✨ Motivational Quote",
    "💖 Health & Study Tips",
    "📊 Statistics Dashboard"
]

selected_menu = st.sidebar.selectbox("Choose an option:", menu_options)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💌 About")
st.sidebar.info("This is your friendly hostel assistant, designed with love to make your hostel life easier and happier! 🌸")

# ============================================================================
# MAIN CONTENT SECTIONS
# ============================================================================

# HOME / WELCOME
if selected_menu == "🏠 Home / Welcome":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🌸 Welcome to Your Home Away From Home!")
        st.markdown("""
        Dear Sister,
        
        We're so happy to have you here! This hostel assistant is designed to make your life 
        easier and more comfortable. Whether you need to check the mess menu, submit a complaint, 
        mark attendance, or just need some motivation - we're here for you! 💝
        
        **Quick Access:**
        - 📋 Check our hostel rules to stay updated
        - 🍽️ See what's cooking in the mess today
        - 📝 Submit any complaints or suggestions
        - ✅ Mark your daily attendance
        - 🎉 Stay updated with upcoming events
        - 🚨 Quick access to emergency contacts
        
        Remember, we're all sisters here. Let's support each other and make this hostel 
        feel like home! 🏡
        
        *With love,*  
        *Your Hostel Team* 💕
        """)
    
    with col2:
        st.markdown("### 🎯 Quick Stats")
        
        # Load data for stats
        complaints = load_json(COMPLAINTS_FILE, [])
        attendance = load_json(ATTENDANCE_FILE, [])
        events = load_json(EVENTS_FILE, [])
        
        # Today's attendance
        today = str(date.today())
        today_attendance = [a for a in attendance if a.get('date') == today]
        
        st.metric("Total Complaints", len(complaints))
        st.metric("Today's Attendance", len(today_attendance))
        st.metric("Upcoming Events", len(events))
        
        st.markdown("---")
        st.markdown("### 🌟 Quote of the Day")
        st.success(random.choice(MOTIVATIONAL_QUOTES))

# HOSTEL RULES
elif selected_menu == "📋 Hostel Rules":
    st.markdown("## 📋 Hostel Rules & Regulations")
    st.markdown("Please follow these rules to maintain a harmonious living environment for everyone 💝")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    for idx, rule in enumerate(HOSTEL_RULES):
        if idx % 2 == 0:
            with col1:
                st.info(f"**{idx + 1}.** {rule}")
        else:
            with col2:
                st.info(f"**{idx + 1}.** {rule}")
    
    st.markdown("---")
    st.success("💝 Remember: These rules are for your safety and comfort. Let's all be responsible sisters!")

# TODAY'S MESS MENU
elif selected_menu == "🍽️ Today's Mess Menu":
    st.markdown("## 🍽️ Today's Delicious Menu")
    
    # Get current day
    today_day = datetime.now().strftime("%A")
    
    if today_day in WEEKLY_MENU:
        menu = WEEKLY_MENU[today_day]
        
        st.markdown(f"### 📅 {today_day}'s Special Menu")
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🌅 Breakfast")
            st.success(menu["Breakfast"])
        
        with col2:
            st.markdown("### ☀️ Lunch")
            st.info(menu["Lunch"])
        
        with col3:
            st.markdown("### 🌙 Dinner")
            st.warning(menu["Dinner"])
        
        st.markdown("---")
        
        # Show full week menu in expander
        with st.expander("📅 View Full Week Menu"):
            for day, meals in WEEKLY_MENU.items():
                st.markdown(f"#### {day}")
                st.markdown(f"**Breakfast:** {meals['Breakfast']}")
                st.markdown(f"**Lunch:** {meals['Lunch']}")
                st.markdown(f"**Dinner:** {meals['Dinner']}")
                st.markdown("---")
        
        st.info("💡 **Tip:** Inform the mess in-charge 2 hours in advance if you'll miss a meal!")

# SUBMIT COMPLAINT
elif selected_menu == "📝 Submit Complaint":
    st.markdown("## 📝 Submit Your Complaint or Suggestion")
    st.markdown("We value your feedback! Let us know how we can improve. 💝")
    st.markdown("---")
    
    with st.form("complaint_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Your Name (Optional)", placeholder="Enter your name")
            room_number = st.text_input("Room Number", placeholder="e.g., 101")
        
        with col2:
            category = st.selectbox("Complaint Category", 
                                   ["Select", "Mess/Food", "Maintenance", "Cleanliness", 
                                    "Security", "Facilities", "Other"])
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
        
        complaint_text = st.text_area("Describe your complaint/suggestion", 
                                      placeholder="Please provide details...",
                                      height=150)
        
        submit_button = st.form_submit_button("📤 Submit Complaint")
        
        if submit_button:
            if not room_number or not complaint_text or category == "Select":
                st.error("⚠️ Please fill in Room Number, Category, and Complaint details!")
            else:
                # Load existing complaints
                complaints = load_json(COMPLAINTS_FILE, [])
                
                # Create new complaint
                new_complaint = {
                    "id": len(complaints) + 1,
                    "name": name if name else "Anonymous",
                    "room_number": room_number,
                    "category": category,
                    "priority": priority,
                    "complaint": complaint_text,
                    "status": "Pending",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                complaints.append(new_complaint)
                
                # Save to file
                if save_json(COMPLAINTS_FILE, complaints):
                    st.success("✅ Your complaint has been submitted successfully! We'll look into it soon. 💝")
                    st.balloons()
                else:
                    st.error("❌ Failed to submit complaint. Please try again.")

# VIEW COMPLAINTS
elif selected_menu == "👀 View Complaints":
    st.markdown("## 👀 All Complaints & Suggestions")
    st.markdown("---")
    
    complaints = load_json(COMPLAINTS_FILE, [])
    
    if not complaints:
        st.info("🎉 No complaints yet! Everything is running smoothly!")
    else:
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox("Filter by Status", 
                                        ["All", "Pending", "In Progress", "Resolved"])
        
        with col2:
            category_filter = st.selectbox("Filter by Category", 
                                          ["All", "Mess/Food", "Maintenance", "Cleanliness", 
                                           "Security", "Facilities", "Other"])
        
        with col3:
            priority_filter = st.selectbox("Filter by Priority",
                                          ["All", "Low", "Medium", "High", "Urgent"])
        
        # Apply filters
        filtered_complaints = complaints
        if status_filter != "All":
            filtered_complaints = [c for c in filtered_complaints if c.get('status') == status_filter]
        if category_filter != "All":
            filtered_complaints = [c for c in filtered_complaints if c.get('category') == category_filter]
        if priority_filter != "All":
            filtered_complaints = [c for c in filtered_complaints if c.get('priority') == priority_filter]
        
        st.markdown(f"**Showing {len(filtered_complaints)} complaint(s)**")
        st.markdown("---")
        
        # Display complaints
        for complaint in reversed(filtered_complaints):  # Show latest first
            with st.expander(f"🎫 Complaint #{complaint['id']} - {complaint['category']} ({complaint['status']})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Name:** {complaint['name']}")
                    st.markdown(f"**Room:** {complaint['room_number']}")
                    st.markdown(f"**Category:** {complaint['category']}")
                    st.markdown(f"**Priority:** {complaint['priority']}")
                    st.markdown(f"**Date:** {complaint['timestamp']}")
                    st.markdown("---")
                    st.markdown(f"**Complaint:**")
                    st.write(complaint['complaint'])
                
                with col2:
                    # Admin controls to update status
                    new_status = st.selectbox(f"Status###{complaint['id']}", 
                                             ["Pending", "In Progress", "Resolved"],
                                             index=["Pending", "In Progress", "Resolved"].index(complaint['status']))
                    
                    if st.button(f"Update###{complaint['id']}"):
                        complaint['status'] = new_status
                        if save_json(COMPLAINTS_FILE, complaints):
                            st.success("✅ Status updated!")
                            st.rerun()

# MARK ATTENDANCE
elif selected_menu == "✅ Mark Attendance":
    st.markdown("## ✅ Mark Your Daily Attendance")
    st.markdown("Please mark your attendance before 10:00 PM daily! 💝")
    st.markdown("---")
    
    # Load attendance data
    attendance = load_json(ATTENDANCE_FILE, [])
    today = str(date.today())
    
    # Show today's stats
    today_attendance = [a for a in attendance if a.get('date') == today]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Today's Date", datetime.now().strftime("%B %d, %Y"))
    with col2:
        st.metric("Marked Present Today", len(today_attendance))
    with col3:
        attendance_percentage = (len(today_attendance) / 100) * 100  # Assuming 100 residents
        st.metric("Attendance Rate", f"{attendance_percentage:.0f}%")
    
    st.markdown("---")
    
    # Attendance form
    with st.form("attendance_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            student_name = st.text_input("Your Name", placeholder="Enter your full name")
        
        with col2:
            room_number = st.text_input("Room Number", placeholder="e.g., 101")
        
        submit_attendance = st.form_submit_button("✅ Mark Present")
        
        if submit_attendance:
            if not student_name or not room_number:
                st.error("⚠️ Please enter both Name and Room Number!")
            else:
                # Check if already marked today
                already_marked = any(
                    a.get('name') == student_name and 
                    a.get('room_number') == room_number and 
                    a.get('date') == today 
                    for a in attendance
                )
                
                if already_marked:
                    st.warning("⚠️ You've already marked attendance today!")
                else:
                    new_attendance = {
                        "name": student_name,
                        "room_number": room_number,
                        "date": today,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    attendance.append(new_attendance)
                    
                    if save_json(ATTENDANCE_FILE, attendance):
                        st.success(f"✅ Attendance marked successfully for {student_name}! 🎉")
                        st.balloons()
                    else:
                        st.error("❌ Failed to mark attendance. Please try again.")
    
    st.markdown("---")
    
    # Show today's attendance list
    with st.expander("📋 View Today's Attendance List"):
        if today_attendance:
            for idx, record in enumerate(today_attendance, 1):
                st.markdown(f"{idx}. **{record['name']}** - Room {record['room_number']} ✅")
        else:
            st.info("No one has marked attendance yet today!")

# UPCOMING EVENTS
elif selected_menu == "🎉 Upcoming Events":
    st.markdown("## 🎉 Upcoming Events & Activities")
    st.markdown("Stay connected with hostel happenings! 💝")
    st.markdown("---")
    
    events = load_json(EVENTS_FILE, [])
    
    if not events:
        st.info("📅 No upcoming events scheduled yet. Stay tuned!")
    else:
        # Sort events by date
        events_sorted = sorted(events, key=lambda x: x.get('date', ''))
        
        for event in events_sorted:
            event_date = datetime.strptime(event['date'], "%Y-%m-%d")
            days_until = (event_date.date() - date.today()).days
            
            if days_until >= 0:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### 🎊 {event['name']}")
                    st.markdown(f"**📅 Date:** {event_date.strftime('%B %d, %Y')}")
                    st.markdown(f"**📝 Description:** {event['description']}")
                
                with col2:
                    if days_until == 0:
                        st.error("🔥 TODAY!")
                    elif days_until == 1:
                        st.warning("⏰ Tomorrow")
                    else:
                        st.info(f"📆 In {days_until} days")
                
                st.markdown("---")
    
    st.success("💡 **Tip:** Check back regularly for updates on events and activities!")

# ADD EVENT
elif selected_menu == "➕ Add Event":
    st.markdown("## ➕ Add New Event")
    st.markdown("Schedule a new hostel event or activity! 🎉")
    st.markdown("---")
    
    with st.form("event_form"):
        event_name = st.text_input("Event Name", placeholder="e.g., Cultural Night")
        
        col1, col2 = st.columns(2)
        
        with col1:
            event_date = st.date_input("Event Date", min_value=date.today())
        
        with col2:
            event_type = st.selectbox("Event Type", 
                                     ["Cultural", "Sports", "Educational", "Festival", "Social", "Other"])
        
        event_description = st.text_area("Event Description", 
                                        placeholder="Provide details about the event...",
                                        height=120)
        
        submit_event = st.form_submit_button("🎉 Add Event")
        
        if submit_event:
            if not event_name or not event_description:
                st.error("⚠️ Please fill in Event Name and Description!")
            else:
                events = load_json(EVENTS_FILE, [])
                
                new_event = {
                    "id": len(events) + 1,
                    "name": event_name,
                    "date": str(event_date),
                    "type": event_type,
                    "description": event_description,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                events.append(new_event)
                
                if save_json(EVENTS_FILE, events):
                    st.success("✅ Event added successfully! 🎊")
                    st.balloons()
                else:
                    st.error("❌ Failed to add event. Please try again.")

# EMERGENCY CONTACTS
elif selected_menu == "🚨 Emergency Contacts":
    st.markdown("## 🚨 Emergency Contacts")
    st.markdown("Save these numbers! Your safety is our priority. 💝")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    for idx, contact in enumerate(EMERGENCY_CONTACTS):
        if idx % 2 == 0:
            with col1:
                st.error(f"**{contact['name']}**\n\n{contact['number']}")
        else:
            with col2:
                st.error(f"**{contact['name']}**\n\n{contact['number']}")
    
    st.markdown("---")
    st.warning("⚠️ **Important:** In case of any emergency, don't hesitate to call. Your safety matters!")
    
    st.info("""
    **When to call:**
    - 🚨 Any immediate danger or threat
    - 🤒 Medical emergencies
    - 🔧 Urgent maintenance issues (water leak, electrical problems)
    - 🔒 Security concerns
    - 💔 If you need someone to talk to
    
    Remember, no problem is too small. We're here to help! 💝
    """)

# MOTIVATIONAL QUOTE
elif selected_menu == "✨ Motivational Quote":
    st.markdown("## ✨ Get Inspired, Sister!")
    st.markdown("Need a little boost? Click the button below! 💝")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🌟 Give Me Motivation!", use_container_width=True):
            quote = random.choice(MOTIVATIONAL_QUOTES)
            st.session_state['current_quote'] = quote
    
    if 'current_quote' in st.session_state:
        st.markdown("---")
        st.success(f"### {st.session_state['current_quote']}")
        st.markdown("---")
        st.markdown("*You're doing amazing! Keep going!* 💪")
    
    st.markdown("---")
    
    # Show all quotes in expander
    with st.expander("📚 View All Quotes"):
        for idx, quote in enumerate(MOTIVATIONAL_QUOTES, 1):
            st.markdown(f"{idx}. {quote}")

# HEALTH & STUDY TIPS
elif selected_menu == "💖 Health & Study Tips":
    st.markdown("## 💖 Health & Study Tips for You")
    st.markdown("Taking care of yourself is important, sister! 🌸")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("💡 Get a Random Tip!", use_container_width=True):
            tip = random.choice(HEALTH_TIPS)
            st.session_state['current_tip'] = tip
    
    if 'current_tip' in st.session_state:
        st.markdown("---")
        st.info(f"### {st.session_state['current_tip']}")
        st.markdown("---")
    
    st.markdown("---")
    
    # Categories of tips
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("🩺 Health Tips"):
            health_tips = [tip for tip in HEALTH_TIPS if any(word in tip for word in 
                          ["health", "water", "sleep", "period", "pain", "medical", "sunlight"])]
            for tip in health_tips:
                st.markdown(f"• {tip}")
    
    with col2:
        with st.expander("📚 Study Tips"):
            study_tips = [tip for tip in HEALTH_TIPS if any(word in tip for word in 
                         ["study", "break", "screen", "productivity", "retention"])]
            for tip in study_tips:
                st.markdown(f"• {tip}")
    
    st.markdown("---")
    st.success("💝 Remember: Your health and well-being come first. Take care of yourself!")

# STATISTICS DASHBOARD
elif selected_menu == "📊 Statistics Dashboard":
    st.markdown("## 📊 Hostel Statistics Dashboard")
    st.markdown("Quick overview of hostel activities 📈")
    st.markdown("---")
    
    # Load all data
    complaints = load_json(COMPLAINTS_FILE, [])
    attendance = load_json(ATTENDANCE_FILE, [])
    events = load_json(EVENTS_FILE, [])
    
    # Overall stats
    st.markdown("### 🎯 Overall Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Complaints", len(complaints), 
                 delta=f"{len([c for c in complaints if c.get('status') == 'Pending'])} pending")
    
    with col2:
        today = str(date.today())
    today_attendance = [a for a in attendance if a.get('date') == today]
    st.metric("Today's Attendance", len(today_attendance))

with col3:
    upcoming_events = len([e for e in events if 
                         datetime.strptime(e.get('date', '2000-01-01'), "%Y-%m-%d").date() >= date.today()])
    st.metric("Upcoming Events", upcoming_events)

with col4:
    total_attendance_records = len(attendance)
    st.metric("Total Attendance Records", total_attendance_records)

st.markdown("---")

# Complaints breakdown
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Complaints Status")
    if complaints:
        pending = len([c for c in complaints if c.get('status') == 'Pending'])
        in_progress = len([c for c in complaints if c.get('status') == 'In Progress'])
        resolved = len([c for c in complaints if c.get('status') == 'Resolved'])
        
        st.success(f"✅ Resolved: {resolved}")
        st.warning(f"⏳ In Progress: {in_progress}")
        st.error(f"⏰ Pending: {pending}")
    else:
        st.info("No complaints data available")

with col2:
    st.markdown("### 🏷️ Complaints by Category")
    if complaints:
        categories = {}
        for c in complaints:
            cat = c.get('category', 'Other')
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"**{cat}:** {count}")
    else:
        st.info("No complaints data available")

st.markdown("---")

# Attendance trends
st.markdown("### 📅 Recent Attendance (Last 7 Days)")
if attendance:
    # Get last 7 days
    recent_dates = {}
    for i in range(7):
        check_date = date.today() - __import__('datetime').timedelta(days=i)
        date_str = str(check_date)
        count = len([a for a in attendance if a.get('date') == date_str])
        recent_dates[check_date.strftime("%b %d")] = count
    
    # Display as columns
    cols = st.columns(7)
    for idx, (day, count) in enumerate(reversed(list(recent_dates.items()))):
        with cols[idx]:
            st.metric(day, count)
else:
    st.info("No attendance data available")

st.markdown("---")
st.success("💝 Data is updated in real-time as sisters use the system!")
