import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
import os
from PIL import Image
import time
import random
import string
import hashlib

# Page configuration
st.set_page_config(
    page_title="AMO Library Management",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Beautiful Dark Theme CSS (keeping the same)
st.markdown("""
<style>
    /* Main theme - Dark mode */
    .stApp {
        background-color: #0f172a;
        color: #f1f5f9;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.5rem;
        color: #60a5fa;
        font-weight: 800;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid #3b82f6;
        background: linear-gradient(90deg, #60a5fa, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
    }
    
    .sub-header {
        font-size: 1.6rem;
        color: #93c5fd;
        font-weight: 700;
        margin-bottom: 1.2rem;
        padding-left: 0.5rem;
        border-left: 4px solid #3b82f6;
    }
    
    /* Success/Error Messages */
    .stAlert {
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Cards */
    .card {
        padding: 1.5rem;
        border-radius: 12px;
        background: linear-gradient(145deg, #1e293b, #0f172a);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.2rem;
        border: 1px solid #334155;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(59, 130, 246, 0.2);
        border-color: #3b82f6;
    }
    
    /* Statistics Cards */
    .stat-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #334155;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.25);
    }
    
    .stat-number {
        font-size: 2.2rem;
        font-weight: 800;
        color: #60a5fa;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 8px rgba(96, 165, 250, 0.4);
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    
    /* Book Cards */
    .book-card {
        padding: 1.2rem;
        border-radius: 10px;
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .book-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(59, 130, 246, 0.2);
        border-color: #3b82f6;
    }
    
    .book-image-container {
        border-radius: 8px;
        overflow: hidden;
        border: 2px solid #334155;
        transition: all 0.3s ease;
    }
    
    .book-image-container:hover {
        border-color: #3b82f6;
        transform: scale(1.02);
    }
    
    /* Member Items */
    .member-item {
        padding: 1.2rem;
        border-radius: 10px;
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .member-item:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }
    
    /* Activity Items */
    .activity-item {
        padding: 1rem;
        border-radius: 8px;
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border-left: 4px solid #3b82f6;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
    }
    
    .activity-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Badges */
    .success-badge {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(16, 185, 129, 0.3);
    }
    
    .warning-badge {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(245, 158, 11, 0.3);
    }
    
    .error-badge {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(239, 68, 68, 0.3);
    }
    
    .info-badge {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(59, 130, 246, 0.3);
    }
    
    /* ID Badges */
    .available-id-badge {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.2rem;
        box-shadow: 0 2px 5px rgba(16, 185, 129, 0.3);
        border: 2px solid #059669;
    }
    
    .taken-id-badge {
        background: linear-gradient(135deg, #64748b, #475569);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.2rem;
        box-shadow: 0 2px 5px rgba(100, 116, 139, 0.3);
        border: 2px solid #475569;
        opacity: 0.8;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
    }
    
    /* Secondary Buttons */
    .secondary-button > button {
        background: linear-gradient(135deg, #64748b, #475569);
        border: 1px solid #64748b;
    }
    
    .secondary-button > button:hover {
        background: linear-gradient(135deg, #475569, #334155);
    }
    
    /* Text Input Styling */
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: #f1f5f9;
        border: 1px solid #475569;
        border-radius: 6px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
    
    /* Select Box Styling */
    .stSelectbox > div > div > select {
        background-color: #1e293b;
        color: #f1f5f9;
        border: 1px solid #475569;
        border-radius: 6px;
    }
    
    /* Text Area Styling */
    .stTextArea > div > div > textarea {
        background-color: #1e293b;
        color: #f1f5f9;
        border: 1px solid #475569;
        border-radius: 6px;
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #475569;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1e293b;
        color: #f1f5f9;
        border: 1px solid #475569;
        border-radius: 8px;
    }
    
    .streamlit-expanderContent {
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 0 0 8px 8px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        border-radius: 8px 8px 0 0;
        padding: 1rem 2rem;
        border: 1px solid #475569;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3b82f6;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# File paths
USERS_FILE = "users.json"
BOOKS_FILE = "books.json"
IMAGE_DIR = "images"
MEMBER_IDS_FILE = "member_ids.json"
PDF_DIR = "pdfs"
DOWNLOAD_HISTORY_FILE = "download_history.json"

# Create directories if they don't exist
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

def load_users():
    """Load user data from JSON file"""
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    """Save user data to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_books():
    """Load book data from JSON file"""
    try:
        with open(BOOKS_FILE, 'r') as f:
            data = json.load(f)
            return data.get("books", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_books(books):
    """Save book data to JSON file"""
    data = {"books": books}
    with open(BOOKS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_member_ids():
    """Load member IDs from JSON file"""
    try:
        with open(MEMBER_IDS_FILE, 'r') as f:
            data = json.load(f)
            return data.get("available_ids", []), data.get("taken_ids", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return [], {}

def save_member_ids(available_ids, taken_ids):
    """Save member IDs to JSON file"""
    data = {
        "available_ids": available_ids,
        "taken_ids": taken_ids
    }
    with open(MEMBER_IDS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_download_history():
    """Load download history from JSON file"""
    try:
        with open(DOWNLOAD_HISTORY_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_download_history(download_history):
    """Save download history to JSON file"""
    with open(DOWNLOAD_HISTORY_FILE, 'w') as f:
        json.dump(download_history, f, indent=4)

def record_download(book_title, book_author, username):
    """Record a PDF download"""
    download_history = load_download_history()
    
    # Create a unique key for the book
    book_key = f"{book_title}_{book_author}"
    
    if book_key not in download_history:
        download_history[book_key] = {
            "title": book_title,
            "author": book_author,
            "total_downloads": 0,
            "user_downloads": {}
        }
    
    # Update total downloads
    download_history[book_key]["total_downloads"] += 1
    
    # Update user-specific downloads
    if username not in download_history[book_key]["user_downloads"]:
        download_history[book_key]["user_downloads"][username] = 0
    
    download_history[book_key]["user_downloads"][username] += 1
    
    # Add timestamp
    if "download_times" not in download_history[book_key]:
        download_history[book_key]["download_times"] = []
    
    download_history[book_key]["download_times"].append({
        "username": username,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Keep only last 100 download times to prevent file from getting too large
    if len(download_history[book_key]["download_times"]) > 100:
        download_history[book_key]["download_times"] = download_history[book_key]["download_times"][-100:]
    
    save_download_history(download_history)

def generate_member_id():
    """Generate a new member ID"""
    available_ids, taken_ids = load_member_ids()
    
    # If we have available IDs, use one
    if available_ids:
        return available_ids[0]
    
    # Otherwise generate a new one
    while True:
        new_id = "MEM" + ''.join(random.choices(string.digits, k=6))
        if new_id not in taken_ids and new_id not in available_ids:
            return new_id

def create_new_member_ids(count=5):
    """Create new member IDs"""
    available_ids, taken_ids = load_member_ids()
    
    for _ in range(count):
        while True:
            new_id = "MEM" + ''.join(random.choices(string.digits, k=6))
            if new_id not in taken_ids and new_id not in available_ids:
                available_ids.append(new_id)
                break
    
    save_member_ids(available_ids, taken_ids)
    return available_ids

def assign_member_id(member_id, username):
    """Assign a member ID to a user"""
    available_ids, taken_ids = load_member_ids()
    
    if member_id in available_ids:
        available_ids.remove(member_id)
        taken_ids[member_id] = username
        save_member_ids(available_ids, taken_ids)
        return True
    return False

def release_member_id(member_id):
    """Release a member ID when user is deleted"""
    available_ids, taken_ids = load_member_ids()
    
    if member_id in taken_ids:
        del taken_ids[member_id]
        available_ids.append(member_id)
        save_member_ids(available_ids, taken_ids)
        return True
    return False

def delete_member_id(member_id):
    """Delete a member ID (admin function)"""
    available_ids, taken_ids = load_member_ids()
    
    if member_id in available_ids:
        available_ids.remove(member_id)
        save_member_ids(available_ids, taken_ids)
        return True
    elif member_id in taken_ids:
        # Can't delete taken IDs
        return False
    return False

def save_image(image_file, identifier):
    """Save uploaded image"""
    if image_file is not None:
        filename = f"{identifier}_{int(time.time())}.{image_file.name.split('.')[-1]}"
        filepath = os.path.join(IMAGE_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(image_file.getbuffer())
        return filename
    return None

def save_pdf(pdf_file, identifier):
    """Save uploaded PDF file"""
    if pdf_file is not None:
        filename = f"{identifier}_{int(time.time())}.pdf"
        filepath = os.path.join(PDF_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(pdf_file.getbuffer())
        return filename
    return None

def get_image_path(filename):
    """Get image path"""
    if filename and os.path.exists(os.path.join(IMAGE_DIR, filename)):
        return os.path.join(IMAGE_DIR, filename)
    return None

def get_pdf_path(filename):
    """Get PDF path"""
    if filename and os.path.exists(os.path.join(PDF_DIR, filename)):
        return os.path.join(PDF_DIR, filename)
    return None

def display_book_image(book, width=150):
    """Display book image with proper error handling"""
    if book.get('image_filename'):
        img_path = get_image_path(book['image_filename'])
        if img_path and os.path.exists(img_path):
            try:
                image = Image.open(img_path)
                # Create a container with the book-image-container class
                st.markdown(f'<div class="book-image-container">', unsafe_allow_html=True)
                st.image(image, width=width)
                st.markdown(f'</div>', unsafe_allow_html=True)
                return True
            except Exception as e:
                st.error(f"Error loading image: {str(e)}")
                return False
    
    # Display placeholder if no image
    placeholder_html = f'''
    <div class="book-image-container" style="width:{width}px; height:{int(width*1.5)}px; display:flex; align-items:center; justify-content:center; background:linear-gradient(135deg, #334155, #1e293b);">
        <div style="color:#94a3b8; font-size:14px; text-align:center;">
            📚<br>
            <small>No Image</small>
        </div>
    </div>
    '''
    st.markdown(placeholder_html, unsafe_allow_html=True)
    return False

def generate_book_key(book):
    """Generate a unique key for a book based on title, author, and year"""
    # Create a unique string from book data
    key_string = f"{book.get('title', '')}_{book.get('author', '')}_{book.get('year', '')}"
    
    # If book has ISBN, use it
    if book.get('isbn'):
        key_string = book.get('isbn')
    
    # Generate a hash for uniqueness
    return hashlib.md5(key_string.encode()).hexdigest()[:8]

def is_book_duplicate(title, author, isbn=None):
    """Check if a book already exists in the library"""
    books = load_books()
    
    for book in books:
        # Check by ISBN if provided
        if isbn and book.get('isbn') == isbn:
            return True
        
        # Check by title and author (case insensitive)
        book_title = book.get('title', '')
        book_author = book.get('author', '')
        
        if (book_title and title and 
            book_title.strip().lower() == title.strip().lower() and 
            book_author and author and
            book_author.strip().lower() == author.strip().lower()):
            return True
    
    return False

def login_page():
    """Login page"""
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown('<div class="main-header">📚 AMO Physics Library</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="sub-header">🔐 Login</div>', unsafe_allow_html=True)
            
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("Login", type="primary", use_container_width=True):
                    users = load_users()
                    if username in users and users[username]["password"] == password:
                        st.session_state.logged_in = True
                        st.session_state.user = username
                        st.session_state.role = users[username]["role"]
                        st.session_state.user_info = users[username]
                        st.success("Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
            
            with col_btn2:
                if st.button("Register", use_container_width=True):
                    st.session_state.show_register = True
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.session_state.get('show_register', False):
                with st.container():
                    st.markdown('<div class="card" style="margin-top: 2rem;">', unsafe_allow_html=True)
                    st.markdown('<div class="sub-header">📝 Member Registration</div>', unsafe_allow_html=True)
                    
                    # NO MORE MEMBER ID SELECTION IN REGISTRATION
                    # Admin will provide IDs personally
                    reg_name = st.text_input("Full Name*")
                    reg_email = st.text_input("Email")
                    reg_username = st.text_input("Choose Username*")
                    reg_password = st.text_input("Choose Password*", type="password")
                    reg_confirm = st.text_input("Confirm Password*", type="password")
                    reg_member_id = st.text_input("Member ID (Provided by Admin)*", placeholder="Enter ID provided by admin")
                    
                    st.info("ℹ️ Please contact admin to get a Member ID for registration.")
                    
                    col_reg1, col_reg2 = st.columns(2)
                    with col_reg1:
                        if st.button("Create Account", type="primary", use_container_width=True):
                            if reg_password != reg_confirm:
                                st.error("Passwords don't match!")
                            elif not all([reg_username, reg_password, reg_name, reg_member_id]):
                                st.error("Please fill all required fields (*)!")
                            else:
                                users = load_users()
                                if reg_username in users:
                                    st.error("Username already exists!")
                                else:
                                    # Check if member ID is available
                                    available_ids, taken_ids = load_member_ids()
                                    if reg_member_id in available_ids:
                                        # Assign the member ID
                                        if assign_member_id(reg_member_id, reg_username):
                                            users[reg_username] = {
                                                "password": reg_password,
                                                "email": reg_email,
                                                "role": "member",
                                                "name": reg_name,
                                                "member_id": reg_member_id,
                                                "borrowed_books": []
                                            }
                                            save_users(users)
                                            st.success("Account created successfully! Please login.")
                                            st.session_state.show_register = False
                                            time.sleep(1)
                                            st.rerun()
                                        else:
                                            st.error("Failed to assign member ID. Please try again.")
                                    else:
                                        st.error("Invalid or already taken Member ID. Please contact admin.")
                        
                    with col_reg2:
                        if st.button("Cancel", use_container_width=True):
                            st.session_state.show_register = False
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

def admin_dashboard():
    """Admin dashboard"""
    st.sidebar.markdown(f"**👨‍💼 Admin:** {st.session_state.user}")
    st.sidebar.markdown("---")
    
    # Simple menu
    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Book Management", "Member Management", "Reports", "Settings", "Librarian Tools", "PDF Downloads"],
        index=0
    )
    
    if menu == "Dashboard":
        st.markdown('<div class="main-header">📊 Dashboard</div>', unsafe_allow_html=True)
        
        # Statistics cards
        books = load_books()
        users = load_users()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(books)}</div>
                <div class="stat-label">Total Books</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            borrowed = sum(1 for book in books if book.get('status') == 'borrowed')
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{borrowed}</div>
                <div class="stat-label">Books Borrowed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            members = sum(1 for user in users.values() if user.get('role') == 'member')
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{members}</div>
                <div class="stat-label">Total Members</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            available = sum(1 for book in books if book.get('status') == 'available')
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{available}</div>
                <div class="stat-label">Available Books</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent activities
        st.markdown('<div class="sub-header">📈 Recent Activities</div>', unsafe_allow_html=True)
        
        # Get recent activities
        recent_activities = []
        books_sorted = sorted(books, key=lambda x: x.get('added_date', ''), reverse=True)
        
        # Show recently added books
        for book in books_sorted[:3]:
            if book.get('added_date'):
                recent_activities.append({
                    'type': 'New Book Added',
                    'title': book['title'],
                    'date': book['added_date'],
                    'icon': '➕'
                })
        
        # Show recently borrowed books
        borrowed_books = [b for b in books if b.get('status') == 'borrowed']
        for book in borrowed_books[:3]:
            recent_activities.append({
                'type': 'Book Borrowed',
                'title': book['title'],
                'date': book.get('borrowed_date', 'Recent'),
                'icon': '📖',
                'borrower': book.get('borrowed_by', 'Unknown')
            })
        
        # Display activities
        for activity in recent_activities[:5]:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    if activity['type'] == 'Book Borrowed':
                        st.markdown(f"<div class='activity-item'>📖 **{activity['title']}** borrowed by **{activity['borrower']}**</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='activity-item'>➕ **{activity['title']}** added to library</div>", unsafe_allow_html=True)
                with col2:
                    st.caption(activity['date'])
        
        # REMOVED QUICK ACTIONS SECTION
    
    elif menu == "Book Management":
        book_management()
    
    elif menu == "Member Management":
        member_management()
    
    elif menu == "Reports":
        reports_page()
    
    elif menu == "Settings":
        settings_page()
    
    elif menu == "Librarian Tools":
        librarian_tools()
    
    elif menu == "PDF Downloads":
        pdf_downloads_page()

def pdf_downloads_page():
    """PDF downloads tracking page"""
    st.markdown('<div class="main-header">📥 PDF Downloads Tracking</div>', unsafe_allow_html=True)
    
    download_history = load_download_history()
    
    if not download_history:
        st.info("📭 No PDF downloads recorded yet.")
        return
    
    # Summary statistics
    total_downloads = sum(data["total_downloads"] for data in download_history.values())
    unique_books = len(download_history)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Downloads", total_downloads)
    
    with col2:
        st.metric("Unique Books Downloaded", unique_books)
    
    with col3:
        # Get most downloaded book
        if download_history:
            most_downloaded = max(download_history.values(), key=lambda x: x["total_downloads"])
            st.metric("Most Downloaded Book", most_downloaded["total_downloads"])
            st.caption(f"{most_downloaded['title']}")
    
    # Search and filter
    st.markdown('<div class="sub-header">📊 Download Statistics by Book</div>', unsafe_allow_html=True)
    
    search_term = st.text_input("🔍 Search books", placeholder="Search by book title or author")
    
    # Filter books
    filtered_books = {}
    for book_key, data in download_history.items():
        book_title = data.get("title", "")
        book_author = data.get("author", "")
        
        if not search_term:
            filtered_books[book_key] = data
        else:
            search_lower = search_term.lower()
            title_match = book_title and search_lower in book_title.lower()
            author_match = book_author and search_lower in book_author.lower()
            
            if title_match or author_match:
                filtered_books[book_key] = data
    
    if filtered_books:
        # Sort by total downloads (descending)
        sorted_books = sorted(filtered_books.items(), key=lambda x: x[1]["total_downloads"], reverse=True)
        
        for book_key, data in sorted_books:
            with st.expander(f"📚 {data['title']} by {data['author']} - {data['total_downloads']} downloads", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📈 Download Statistics:**")
                    st.write(f"**Total Downloads:** {data['total_downloads']}")
                    
                    # User breakdown
                    st.write("**👥 Downloads by User:**")
                    if data.get('user_downloads'):
                        for user, count in sorted(data['user_downloads'].items(), key=lambda x: x[1], reverse=True):
                            st.write(f"- **{user}**: {count} download(s)")
                    else:
                        st.write("No user-specific data available")
                
                with col2:
                    # Recent downloads
                    st.write("**🕒 Recent Downloads:**")
                    if data.get('download_times'):
                        recent_downloads = sorted(data['download_times'], key=lambda x: x['timestamp'], reverse=True)[:10]
                        for download in recent_downloads:
                            st.write(f"- {download['username']} at {download['timestamp']}")
                    else:
                        st.write("No download times recorded")
                
                # Export button for this book
                if st.button(f"📥 Export Data for {data['title'][:30]}...", key=f"export_{book_key}"):
                    export_book_downloads(data)
    
    else:
        st.info("📭 No books match your search criteria.")

def export_book_downloads(book_data):
    """Export download data for a specific book"""
    df = pd.DataFrame({
        "Metric": ["Book Title", "Author", "Total Downloads"],
        "Value": [book_data["title"], book_data["author"], book_data["total_downloads"]]
    })
    
    # User downloads
    if book_data.get('user_downloads'):
        user_df = pd.DataFrame(list(book_data["user_downloads"].items()), columns=["User", "Downloads"])
        df = pd.concat([df, pd.DataFrame({"Metric": ["---", "User Downloads", "---"], "Value": ["", "", ""]})])
        df = pd.concat([df, user_df])
    
    # Recent downloads
    if book_data.get('download_times'):
        time_df = pd.DataFrame(book_data["download_times"])
        df = pd.concat([df, pd.DataFrame({"Metric": ["---", "Recent Downloads", "---"], "Value": ["", "", ""]})])
        df = pd.concat([df, time_df])
    
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"downloads_{book_data['title'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

def librarian_tools():
    """Librarian tools for manual book operations"""
    st.markdown('<div class="main-header">📚 Librarian Tools</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📖 Manual Book Borrow", "↩️ Manual Book Return"])
    
    with tab1:
        st.markdown('<div class="sub-header">📖 Borrow Book for Member</div>', unsafe_allow_html=True)
        
        books = load_books()
        users = load_users()
        
        # Get available books
        available_books = [b for b in books if b.get('status') == 'available']
        # Get members
        members = {k: v for k, v in users.items() if v.get('role') == 'member'}
        
        if not available_books:
            st.warning("❌ No available books to borrow.")
        elif not members:
            st.warning("❌ No members registered yet.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                # Book selection
                book_options = {}
                for b in available_books:
                    identifier = b.get('isbn') or f"Title: {b['title']}"
                    label = f"{b['title']} by {b.get('author', 'Unknown')} ({identifier})"
                    book_options[label] = b
                
                selected_book_label = st.selectbox("Select Book to Borrow", list(book_options.keys()))
                selected_book = book_options[selected_book_label]
                
                # Display book info
                if selected_book:
                    st.write("**Selected Book Details:**")
                    st.write(f"**Title:** {selected_book['title']}")
                    st.write(f"**Author:** {selected_book.get('author', 'Unknown')}")
                    if selected_book.get('isbn'):
                        st.write(f"**ISBN:** {selected_book['isbn']}")
            
            with col2:
                # Member selection
                member_options = {f"{v['name']} (ID: {v['member_id']})": k for k, v in members.items()}
                selected_member_label = st.selectbox("Select Member", list(member_options.keys()))
                selected_member_username = member_options[selected_member_label]
                selected_member_info = members[selected_member_username]
                
                # Display member info
                if selected_member_info:
                    st.write("**Selected Member Details:**")
                    st.write(f"**Name:** {selected_member_info['name']}")
                    st.write(f"**Member ID:** {selected_member_info['member_id']}")
                    st.write(f"**Currently Borrowed:** {len(selected_member_info.get('borrowed_books', []))} books")
            
            # Borrow button
            if st.button("✅ Borrow Book", type="primary", use_container_width=True):
                if selected_book and selected_member_username:
                    # Borrow the book - use title and author as identifier
                    if borrow_book_admin(selected_book, selected_member_username):
                        st.success(f"✅ Book '{selected_book['title']}' borrowed by {selected_member_info['name']}!")
                        st.balloons()
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("❌ Failed to borrow book. Please try again.")
    
    with tab2:
        st.markdown('<div class="sub-header">↩️ Return Book for Member</div>', unsafe_allow_html=True)
        
        books = load_books()
        users = load_users()
        
        # Get borrowed books
        borrowed_books = [b for b in books if b.get('status') == 'borrowed']
        
        if not borrowed_books:
            st.info("📭 No books currently borrowed.")
        else:
            # Book selection
            book_options = {}
            for book in borrowed_books:
                borrower_username = book.get('borrowed_by')
                if borrower_username in users:
                    borrower_name = users[borrower_username].get('name', borrower_username)
                    identifier = book.get('isbn') or f"Title: {book['title']}"
                    label = f"{book['title']} by {book.get('author', 'Unknown')} ({identifier}) - Borrowed by: {borrower_name}"
                    book_options[label] = book
            
            selected_book_label = st.selectbox("Select Book to Return", list(book_options.keys()))
            selected_book = book_options[selected_book_label]
            
            if selected_book:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Book Details:**")
                    st.write(f"**Title:** {selected_book['title']}")
                    st.write(f"**Author:** {selected_book.get('author', 'Unknown')}")
                    if selected_book.get('isbn'):
                        st.write(f"**ISBN:** {selected_book['isbn']}")
                
                with col2:
                    borrower_username = selected_book.get('borrowed_by')
                    if borrower_username in users:
                        borrower_info = users[borrower_username]
                        st.write("**Borrower Details:**")
                        st.write(f"**Name:** {borrower_info['name']}")
                        st.write(f"**Member ID:** {borrower_info['member_id']}")
                    
                    st.write(f"**Borrowed Date:** {selected_book.get('borrowed_date', 'N/A')}")
                
                # Return button
                if st.button("↩️ Return Book", type="primary", use_container_width=True):
                    if return_book_admin(selected_book):
                        st.success(f"✅ Book '{selected_book['title']}' returned successfully!")
                        st.balloons()
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("❌ Failed to return book. Please try again.")

def book_management():
    """Book management page"""
    st.markdown('<div class="main-header">📚 Book Management</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 View All Books", "➕ Add New Book", "✏️ Update Book"])
    
    with tab1:
        books = load_books()
        
        # Search and filter
        col1, col2 = st.columns([2, 1])
        with col1:
            search_term = st.text_input("🔍 Search books", placeholder="Search by title, author, or ISBN")
        with col2:
            filter_status = st.selectbox("Filter by Status", ["All", "Available", "Borrowed"])
        
        # Filter books
        filtered_books = books
        if search_term:
            search_lower = search_term.lower()
            filtered_books = []
            for b in books:
                # Safely get values with defaults
                title = b.get('title', '') or ''
                author = b.get('author', '') or ''
                isbn = b.get('isbn', '') or ''
                
                # Check if search term matches any field
                title_match = title and search_lower in title.lower()
                author_match = author and search_lower in author.lower()
                isbn_match = isbn and search_lower in str(isbn).lower()
                
                if title_match or author_match or isbn_match:
                    filtered_books.append(b)
        
        if filter_status != "All":
            filtered_books = [b for b in filtered_books if b.get('status', '').lower() == filter_status.lower()]
        
        # Display books
        if filtered_books:
            for idx, book in enumerate(filtered_books):
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        # Display book image
                        display_book_image(book, width=120)
                    
                    with col2:
                        st.write(f"**{book.get('title', 'No Title')}**")
                        st.write(f"by **{book.get('author', 'Unknown')}**")
                        if book.get('isbn'):
                            st.write(f"ISBN: `{book.get('isbn', 'N/A')}`")
                        st.write(f"Type: {book.get('book_type', 'N/A')}")
                        
                        if book.get('status') == 'available':
                            st.markdown('<span class="success-badge">Available</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span class="error-badge">Borrowed</span>', unsafe_allow_html=True)
                            st.write(f"**By:** {book.get('borrowed_by', 'Unknown')}")
                            st.write(f"**Borrowed:** {book.get('borrowed_date', 'N/A')}")
                    
                    with col3:
                        col_edit, col_del = st.columns(2)
                        with col_edit:
                            # Generate unique key for each book
                            book_key = generate_book_key(book)
                            if st.button("✏️", key=f"edit_{book_key}_{idx}", help="Edit book"):
                                st.session_state.edit_book_key = book_key
                                st.session_state.edit_book_index = idx
                                st.rerun()
                        with col_del:
                            if st.button("🗑️", key=f"delete_{book_key}_{idx}", help="Delete book"):
                                delete_book(book)
                                st.success("✅ Book deleted successfully!")
                                time.sleep(1)
                                st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("📭 No books found matching your criteria.")
    
    with tab2:
        with st.form("add_book_form"):
            st.markdown('<div class="sub-header">➕ Add New Physics Book</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Book Title*", placeholder="Enter book title")
                author = st.text_input("Author(s)*", placeholder="Enter author name(s)")
                isbn = st.text_input("ISBN (Optional)", placeholder="Enter ISBN number")
                book_type = st.selectbox("Book Type*", ["Printed", "Original", "E-Book", "Reference Copy"])
                
            with col2:
                publisher = st.text_input("Publisher", placeholder="Enter publisher name")
                year = st.number_input("Publication Year*", min_value=1000, max_value=datetime.now().year, value=2023, step=1)
                image_file = st.file_uploader("Book Cover Image (Optional)", type=['jpg', 'jpeg', 'png', 'webp'])
                pdf_file = st.file_uploader("PDF File (Optional - for E-Books)", type=['pdf'])
            
            # Physics-specific categories (optional)
            physics_categories = [
                "Quantum Mechanics",
                "Classical Mechanics",
                "Electromagnetism",
                "Thermodynamics",
                "Statistical Mechanics",
                "Optics",
                "Astrophysics",
                "Particle Physics",
                "Condensed Matter",
                "Mathematical Physics",
                "Nuclear Physics",
                "Relativity",
                "Atomic Physics",
                "Plasma Physics",
                "Biophysics",
                "Geophysics",
                "Computational Physics",
                "Experimental Physics",
                "Theoretical Physics",
                "General Physics"
            ]
            
            col_cat1, col_cat2 = st.columns(2)
            with col_cat1:
                category = st.selectbox("Physics Category (Optional)", ["Select Category"] + physics_categories)
                if category == "Select Category":
                    category = None
            with col_cat2:
                subcategory = st.text_input("Sub-category (Optional)", placeholder="e.g., Quantum Computing, Nanotechnology")
            
            description = st.text_area("Description", placeholder="Enter book description", height=100)
            remarks = st.text_area("Remarks (Optional)", placeholder="Any additional remarks about the book", height=80)
            
            submitted = st.form_submit_button("📚 Add Book", type="primary", use_container_width=True)
            
            if submitted:
                if title and author and book_type:
                    # Check for duplicate book
                    if is_book_duplicate(title, author, isbn):
                        st.error("❌ This book already exists in the library!")
                    else:
                        books = load_books()
                        
                        # Use ISBN as identifier for image, or title if no ISBN
                        identifier = isbn if isbn else title.replace(" ", "_")[:20]
                        image_filename = save_image(image_file, identifier) if image_file else None
                        pdf_filename = save_pdf(pdf_file, identifier) if pdf_file else None
                        
                        new_book = {
                            "title": title,
                            "author": author,
                            "isbn": isbn if isbn else None,
                            "category": category,
                            "subcategory": subcategory if subcategory else None,
                            "book_type": book_type,
                            "publisher": publisher if publisher else None,
                            "year": int(year),
                            "description": description if description else None,
                            "remarks": remarks if remarks else None,
                            "status": "available",
                            "added_date": datetime.now().strftime("%Y-%m-%d"),
                            "image_filename": image_filename,
                            "pdf_filename": pdf_filename,
                            "borrowed_by": None,
                            "borrowed_date": None
                        }
                        
                        books.append(new_book)
                        save_books(books)
                        st.success(f"✅ Book '{title}' added successfully!")
                        st.balloons()
                        st.rerun()
                else:
                    st.error("⚠️ Please fill in all required fields (*)")
    
    with tab3:
        st.markdown('<div class="sub-header">✏️ Update Book Details</div>', unsafe_allow_html=True)
        
        books = load_books()
        
        if not books:
            st.info("📭 No books available to edit.")
        else:
            # If edit_book_key is set in session state, use it
            if 'edit_book_key' in st.session_state:
                # Find the book by key
                for idx, book in enumerate(books):
                    if generate_book_key(book) == st.session_state.edit_book_key:
                        selected_book = book
                        break
                else:
                    selected_book = books[0]
            else:
                # Book selection
                book_options = {}
                for book in books:
                    identifier = book.get('isbn') or f"Title: {book['title']}"
                    label = f"{book['title']} by {book.get('author', 'Unknown')} ({identifier})"
                    book_options[label] = book
                
                selected_book_label = st.selectbox("Select Book to Edit", list(book_options.keys()))
                selected_book = book_options[selected_book_label]
            
            if selected_book:
                # Generate unique key for the form
                form_key = generate_book_key(selected_book)
                
                with st.form(f"update_form_{form_key}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_title = st.text_input("Book Title", value=selected_book.get('title', ''))
                        new_author = st.text_input("Author(s)", value=selected_book.get('author', ''))
                        new_isbn = st.text_input("ISBN (Optional)", value=selected_book.get('isbn', ''))
                        new_book_type = st.selectbox("Book Type", 
                                                   ["Printed", "Original", "E-Book", "Reference Copy"],
                                                   index=["Printed", "Original", "E-Book", "Reference Copy"].index(
                                                       selected_book.get('book_type', 'Printed')
                                                   ))
                    
                    with col2:
                        new_publisher = st.text_input("Publisher", value=selected_book.get('publisher', ''))
                        # FIXED: Ensure year is integer type
                        current_year = int(selected_book.get('year', 2023))
                        new_year = st.number_input("Publication Year", 
                                                  min_value=1000, 
                                                  max_value=datetime.now().year, 
                                                  value=current_year,
                                                  step=1)
                        new_image_file = st.file_uploader("Update Book Cover Image", 
                                                         type=['jpg', 'jpeg', 'png', 'webp'],
                                                         key=f"image_{form_key}")
                        new_pdf_file = st.file_uploader("Update PDF File", 
                                                       type=['pdf'],
                                                       key=f"pdf_{form_key}")
                    
                    # Physics categories
                    physics_categories = [
                        "Quantum Mechanics",
                        "Classical Mechanics",
                        "Electromagnetism",
                        "Thermodynamics",
                        "Statistical Mechanics",
                        "Optics",
                        "Astrophysics",
                        "Particle Physics",
                        "Condensed Matter",
                        "Mathematical Physics",
                        "Nuclear Physics",
                        "Relativity",
                        "Atomic Physics",
                        "Plasma Physics",
                        "Biophysics",
                        "Geophysics",
                        "Computational Physics",
                        "Experimental Physics",
                        "Theoretical Physics",
                        "General Physics"
                    ]
                    
                    current_category = selected_book.get('category', '')
                    category_index = 0
                    if current_category and current_category in physics_categories:
                        category_index = physics_categories.index(current_category) + 1
                    
                    new_category = st.selectbox("Physics Category (Optional)", 
                                               ["Select Category"] + physics_categories,
                                               index=category_index,
                                               key=f"cat_{form_key}")
                    if new_category == "Select Category":
                        new_category = None
                    
                    new_subcategory = st.text_input("Sub-category (Optional)", 
                                                   value=selected_book.get('subcategory', ''),
                                                   key=f"subcat_{form_key}")
                    new_description = st.text_area("Description", 
                                                  value=selected_book.get('description', ''),
                                                  height=100,
                                                  key=f"desc_{form_key}")
                    new_remarks = st.text_area("Remarks (Optional)", 
                                              value=selected_book.get('remarks', ''),
                                              height=80,
                                              key=f"remarks_{form_key}")
                    
                    col_sub1, col_sub2 = st.columns(2)
                    with col_sub1:
                        submit = st.form_submit_button("💾 Update Book", type="primary", use_container_width=True)
                    with col_sub2:
                        cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                    
                    if submit:
                        # Only validate required fields
                        if new_title and new_author and new_book_type:
                            # Check if this would create a duplicate (excluding current book)
                            current_key = generate_book_key(selected_book)
                            new_key = hashlib.md5(f"{new_title}_{new_author}_{new_year}".encode()).hexdigest()[:8]
                            
                            if new_key != current_key:  # If details changed
                                if is_book_duplicate(new_title, new_author, new_isbn):
                                    st.error("❌ A book with these details already exists!")
                                else:
                                    update_book_success = update_book(selected_book, new_title, new_author, new_isbn, 
                                                                    new_book_type, new_publisher, new_year, 
                                                                    new_image_file, new_pdf_file, new_category, new_subcategory, 
                                                                    new_description, new_remarks)
                                    if update_book_success:
                                        st.success(f"✅ Book '{new_title}' updated successfully!")
                                        st.balloons()
                                        time.sleep(1)
                                        st.rerun()
                            else:
                                # Same book, just update
                                update_book_success = update_book(selected_book, new_title, new_author, new_isbn, 
                                                                new_book_type, new_publisher, new_year, 
                                                                new_image_file, new_pdf_file, new_category, new_subcategory, 
                                                                new_description, new_remarks)
                                if update_book_success:
                                    st.success(f"✅ Book '{new_title}' updated successfully!")
                                    st.balloons()
                                    time.sleep(1)
                                    st.rerun()
                        else:
                            st.error("⚠️ Please fill in all required fields!")
                    
                    if cancel:
                        # Clear edit state
                        if 'edit_book_key' in st.session_state:
                            del st.session_state.edit_book_key
                        if 'edit_book_index' in st.session_state:
                            del st.session_state.edit_book_index
                        st.rerun()

def update_book(selected_book, new_title, new_author, new_isbn, new_book_type, new_publisher, new_year, 
                new_image_file, new_pdf_file, new_category, new_subcategory, new_description, new_remarks):
    """Update book details in the database"""
    books = load_books()
    
    for i, book in enumerate(books):
        # Find the book to update
        book_title = book.get('title', '')
        book_author = book.get('author', '')
        selected_title = selected_book.get('title', '')
        selected_author = selected_book.get('author', '')
        
        if (book_title == selected_title and 
            book_author == selected_author):
            
            # Update image if new one uploaded
            if new_image_file:
                identifier = new_isbn if new_isbn else new_title.replace(" ", "_")[:20]
                new_image_filename = save_image(new_image_file, identifier)
                if new_image_filename:
                    books[i]['image_filename'] = new_image_filename
            
            # Update PDF if new one uploaded
            if new_pdf_file:
                identifier = new_isbn if new_isbn else new_title.replace(" ", "_")[:20]
                new_pdf_filename = save_pdf(new_pdf_file, identifier)
                if new_pdf_filename:
                    books[i]['pdf_filename'] = new_pdf_filename
            
            # Update other fields
            books[i]['title'] = new_title
            books[i]['author'] = new_author
            books[i]['isbn'] = new_isbn if new_isbn else None
            books[i]['book_type'] = new_book_type
            books[i]['publisher'] = new_publisher if new_publisher else None
            books[i]['year'] = int(new_year)
            books[i]['category'] = new_category
            books[i]['subcategory'] = new_subcategory if new_subcategory else None
            books[i]['description'] = new_description if new_description else None
            books[i]['remarks'] = new_remarks if new_remarks else None
            break
    
    save_books(books)
    return True

def member_management():
    """Member management page"""
    st.markdown('<div class="main-header">👥 Member Management</div>', unsafe_allow_html=True)
    
    users = load_users()
    books = load_books()
    members = {k: v for k, v in users.items() if v.get('role') == 'member'}
    
    # Member ID Management Section
    st.markdown('<div class="sub-header">🆔 Member ID Management</div>', unsafe_allow_html=True)
    
    available_ids, taken_ids = load_member_ids()
    
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    
    with col_stats1:
        st.metric("Available IDs", len(available_ids))
    with col_stats2:
        st.metric("Taken IDs", len(taken_ids))
    with col_stats3:
        st.metric("Total Members", len(members))
    
    # Create new IDs
    col_id1, col_id2 = st.columns([2, 1])
    with col_id1:
        new_id_count = st.number_input("Number of new IDs to generate", min_value=1, max_value=50, value=5)
    with col_id2:
        if st.button("🆕 Generate New IDs", use_container_width=True):
            create_new_member_ids(new_id_count)
            st.success(f"✅ Generated {new_id_count} new member IDs!")
            st.rerun()
    
    # Display all member IDs with different colors
    st.markdown("---")
    st.markdown('<div class="sub-header">📋 All Member IDs</div>', unsafe_allow_html=True)
    
    # Combine all IDs
    all_ids = {}
    for mem_id in available_ids:
        all_ids[mem_id] = "available"
    
    for mem_id in taken_ids:
        all_ids[mem_id] = "taken"
    
    if all_ids:
        # Sort IDs
        sorted_ids = sorted(all_ids.keys())
        
        # Display in a grid with different colors
        st.write("**Available IDs are shown in green, Taken IDs in gray:**")
        
        # Create columns for grid layout
        cols_per_row = 6
        rows = []
        
        for i in range(0, len(sorted_ids), cols_per_row):
            rows.append(sorted_ids[i:i + cols_per_row])
        
        for row in rows:
            cols = st.columns(cols_per_row)
            for idx, mem_id in enumerate(row):
                with cols[idx]:
                    if all_ids[mem_id] == "available":
                        st.markdown(f'<div class="available-id-badge">{mem_id}</div>', unsafe_allow_html=True)
                        
                        # Delete button for available IDs
                        if st.button(f"🗑️", key=f"delete_id_{mem_id}", help=f"Delete {mem_id}"):
                            if delete_member_id(mem_id):
                                st.success(f"✅ Member ID {mem_id} deleted!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete member ID.")
                    else:
                        username = taken_ids.get(mem_id, "Unknown")
                        user_info = users.get(username, {})
                        user_name = user_info.get('name', username)
                        st.markdown(f'<div class="taken-id-badge" title="Assigned to: {user_name}">{mem_id}</div>', unsafe_allow_html=True)
    else:
        st.info("📭 No member IDs created yet. Generate some new IDs.")
    
    st.markdown("---")
    st.markdown('<div class="sub-header">👤 Member Management</div>', unsafe_allow_html=True)
    
    if not members:
        st.info("📭 No members registered yet.")
        return
    
    # Search bar
    search_term = st.text_input("🔍 Search members", placeholder="Search by name, username, or member ID")
    
    # Filter members
    filtered_members = members
    if search_term:
        search_lower = search_term.lower()
        filtered_members = {}
        for k, v in members.items():
            name = v.get('name', '') or ''
            username_val = k or ''
            member_id = v.get('member_id', '') or ''
            
            name_match = name and search_lower in name.lower()
            username_match = username_val and search_lower in username_val.lower()
            member_id_match = member_id and search_lower in member_id.lower()
            
            if name_match or username_match or member_id_match:
                filtered_members[k] = v
    
    # Display members
    for idx, (username, info) in enumerate(filtered_members.items()):
        with st.expander(f"👤 {info.get('name', username)} - ID: {info.get('member_id', 'N/A')}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Username:** `{username}`")
                st.write(f"**Name:** {info.get('name', 'N/A')}")
                st.write(f"**Email:** {info.get('email', 'N/A')}")
                st.write(f"**Member ID:** {info.get('member_id', 'N/A')}")
                
                borrowed_isbns = info.get('borrowed_books', [])
                if borrowed_isbns:
                    st.markdown(f'<span class="info-badge">{len(borrowed_isbns)} Books Borrowed</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="success-badge">No Books Borrowed</span>', unsafe_allow_html=True)
            
            with col2:
                # Edit button
                if st.button("✏️ Edit", key=f"edit_{username}_{idx}", use_container_width=True):
                    st.session_state.edit_member = username
                    st.rerun()
                
                # View borrowed books
                if st.button("📚 View Books", key=f"view_{username}_{idx}", use_container_width=True):
                    st.session_state.view_member_books = username
                    st.rerun()
            
            # Show borrowed books if viewing
            if st.session_state.get('view_member_books') == username:
                st.markdown("---")
                st.write("**📚 Currently Borrowed Books:**")
                
                if borrowed_isbns:
                    borrowed_books_details = []
                    for book in books:
                        if book.get('title') and book.get('author'):
                            book_identifier = f"{book['title']} by {book['author']}"
                            if book_identifier in borrowed_isbns:
                                borrowed_books_details.append(book)
                    
                    for book_idx, book in enumerate(borrowed_books_details):
                        with st.container():
                            col_book1, col_book2, col_book3 = st.columns([3, 2, 1])
                            
                            with col_book1:
                                st.write(f"**{book.get('title', 'Unknown')}**")
                                st.write(f"by {book.get('author', 'Unknown')}")
                            
                            with col_book2:
                                st.write(f"**Borrowed:** {book.get('borrowed_date', 'N/A')}")
                            
                            with col_book3:
                                book_identifier = f"{book['title']} by {book['author']}"
                                if st.button("↩️ Return", key=f"return_{book_identifier}_{username}_{book_idx}"):
                                    return_book_admin(book)
                                    st.success(f"✅ Book '{book.get('title')}' returned!")
                                    time.sleep(1)
                                    st.rerun()
                else:
                    st.info("No books currently borrowed.")
    
    # Edit member section
    if st.session_state.get('edit_member'):
        st.markdown("---")
        st.markdown('<div class="sub-header">✏️ Edit Member</div>', unsafe_allow_html=True)
        
        selected_member = st.session_state.edit_member
        member_info = members[selected_member]
        
        # Separate form for editing
        with st.form(f"edit_form_{selected_member}"):
            new_name = st.text_input("Full Name", value=member_info.get('name', ''))
            new_email = st.text_input("Email", value=member_info.get('email', ''))
            new_member_id = st.text_input("Member ID", value=member_info.get('member_id', ''), disabled=True)
            
            col_pass1, col_pass2 = st.columns(2)
            with col_pass1:
                new_password = st.text_input("New Password", type="password", 
                                           placeholder="Leave blank to keep current")
            with col_pass2:
                confirm_password = st.text_input("Confirm Password", type="password")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit = st.form_submit_button("💾 Update", type="primary", use_container_width=True)
            with col_btn2:
                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submit:
                if new_password and new_password != confirm_password:
                    st.error("Passwords don't match!")
                else:
                    # Update user info
                    users[selected_member]['name'] = new_name
                    users[selected_member]['email'] = new_email
                    
                    if new_password:
                        users[selected_member]['password'] = new_password
                    
                    save_users(users)
                    st.success(f"✅ Member '{selected_member}' updated!")
                    st.session_state.edit_member = None
                    time.sleep(1)
                    st.rerun()
            
            if cancel:
                st.session_state.edit_member = None
                st.rerun()

def reports_page():
    """Reports page"""
    st.markdown('<div class="main-header">📊 Reports & Analytics</div>', unsafe_allow_html=True)
    
    books = load_books()
    users = load_users()
    
    # Summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="sub-header">📈 Book Statistics</div>', unsafe_allow_html=True)
        
        total_books = len(books)
        available_books = sum(1 for b in books if b.get('status') == 'available')
        borrowed_books = total_books - available_books
        
        st.write(f"**Total Books:** {total_books}")
        st.write(f"**Available:** {available_books}")
        st.write(f"**Borrowed:** {borrowed_books}")
        
        # Physics categories distribution
        categories = {}
        for book in books:
            cat = book.get('category', 'General Physics')
            if cat:
                categories[cat] = categories.get(cat, 0) + 1
        
        if categories:
            st.write("**📚 Books by Physics Category:**")
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]:
                percentage = (count / total_books) * 100
                st.write(f"- **{cat}:** {count} ({percentage:.1f}%)")
    
    with col2:
        st.markdown('<div class="sub-header">👥 Member Statistics</div>', unsafe_allow_html=True)
        
        members = sum(1 for u in users.values() if u.get('role') == 'member')
        active_borrowers = sum(1 for u in users.values() 
                               if u.get('role') == 'member' and len(u.get('borrowed_books', [])) > 0)
        
        st.write(f"**Total Members:** {members}")
        st.write(f"**Active Borrowers:** {active_borrowers}")
        
        # Book type distribution
        book_types = {}
        for book in books:
            btype = book.get('book_type', 'Unknown')
            book_types[btype] = book_types.get(btype, 0) + 1
        
        if book_types:
            st.write("**📖 Books by Type:**")
            for btype, count in book_types.items():
                st.write(f"- **{btype}:** {count}")
    
    # Export options
    st.markdown("---")
    st.markdown('<div class="sub-header">📥 Export Data</div>', unsafe_allow_html=True)
    
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    
    with col_exp1:
        if st.button("📚 Export Books Data", use_container_width=True):
            export_to_excel()
    
    with col_exp2:
        if st.button("👥 Export Members Data", use_container_width=True):
            export_members_to_excel()
    
    with col_exp3:
        if st.button("📋 Export Borrowing History", use_container_width=True):
            export_borrowing_history()

def settings_page():
    """Settings page"""
    st.markdown('<div class="main-header">⚙️ Settings</div>', unsafe_allow_html=True)
    
    users = load_users()
    admin_info = users.get(st.session_state.user, {})
    
    with st.form("admin_settings_form"):
        st.markdown('<div class="sub-header">🔐 Change Password</div>', unsafe_allow_html=True)
        
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        submitted = st.form_submit_button("🔐 Change Password", type="primary", use_container_width=True)
        
        if submitted:
            if current_password != admin_info.get('password'):
                st.error("❌ Current password is incorrect!")
            elif new_password != confirm_password:
                st.error("❌ New passwords don't match!")
            elif not new_password:
                st.error("⚠️ New password cannot be empty!")
            else:
                users[st.session_state.user]['password'] = new_password
                save_users(users)
                st.success("✅ Password changed successfully!")
                st.rerun()

def member_dashboard():
    """Member dashboard"""
    st.sidebar.markdown(f"**👤 Member:** {st.session_state.user_info.get('name', st.session_state.user)}")
    st.sidebar.markdown("---")
    
    # Simple menu for members
    menu = st.sidebar.radio(
        "Menu",
        ["🔍 Browse Books", "📖 My Books", "👤 Profile", "📥 PDF Downloads"],
        index=0
    )
    
    if menu == "🔍 Browse Books":
        st.markdown('<div class="main-header">🔍 Browse Physics Books</div>', unsafe_allow_html=True)
        
        books = load_books()
        available_books = [b for b in books if b.get('status') == 'available']
        
        if available_books:
            # Search and filter
            col1, col2 = st.columns([2, 1])
            with col1:
                search_term = st.text_input("🔍 Search books", placeholder="Search by title, author, or ISBN")
            with col2:
                # Get unique categories from available books
                unique_categories = []
                for b in available_books:
                    cat = b.get('category')
                    if cat and cat not in unique_categories:
                        unique_categories.append(cat)
                unique_categories.sort()
                category_filter = st.selectbox("Category", ["All Categories"] + unique_categories)
            
            # Filter books
            filtered_books = available_books
            if search_term:
                search_lower = search_term.lower()
                filtered_books = []
                for b in available_books:
                    title = b.get('title', '') or ''
                    author = b.get('author', '') or ''
                    isbn = b.get('isbn', '') or ''
                    
                    title_match = title and search_lower in title.lower()
                    author_match = author and search_lower in author.lower()
                    isbn_match = isbn and search_lower in str(isbn).lower()
                    
                    if title_match or author_match or isbn_match:
                        filtered_books.append(b)
            
            if category_filter != "All Categories":
                filtered_books = [b for b in filtered_books if b.get('category') == category_filter]
            
            # Display books in grid
            if filtered_books:
                cols = st.columns(2)
                for idx, book in enumerate(filtered_books):
                    with cols[idx % 2]:
                        with st.container():
                            st.markdown('<div class="book-card">', unsafe_allow_html=True)
                            
                            # Display book image
                            display_book_image(book, width=180)
                            
                            st.write(f"**{book.get('title', 'No Title')}**")
                            st.write(f"by *{book.get('author', 'Unknown')}*")
                            if book.get('isbn'):
                                st.write(f"**ISBN:** {book.get('isbn')}")
                            if book.get('category'):
                                st.write(f"**Category:** {book.get('category')}")
                            if book.get('subcategory'):
                                st.write(f"**Sub-category:** {book.get('subcategory')}")
                            st.write(f"**Type:** {book.get('book_type', 'N/A')}")
                            
                            # Show description preview
                            if book.get('description'):
                                st.write(f"{book.get('description', '')[:120]}...")
                            
                            # Generate unique key for borrow button
                            book_key = generate_book_key(book)
                            
                            # Show appropriate action based on book type
                            if book.get('book_type') == 'E-Book' and book.get('pdf_filename'):
                                # For E-Books with PDF, show download button
                                if st.button("📥 Download PDF", key=f"download_{book_key}_{idx}", use_container_width=True):
                                    pdf_path = get_pdf_path(book['pdf_filename'])
                                    if pdf_path and os.path.exists(pdf_path):
                                        # Record the download
                                        record_download(book['title'], book['author'], st.session_state.user)
                                        
                                        # Create download link
                                        with open(pdf_path, "rb") as pdf_file:
                                            pdf_data = pdf_file.read()
                                            st.download_button(
                                                label="⬇️ Click to Download PDF",
                                                data=pdf_data,
                                                file_name=f"{book['title'].replace(' ', '_')}.pdf",
                                                mime="application/pdf",
                                                key=f"pdf_download_{book_key}_{idx}"
                                            )
                                        st.success(f"✅ Downloading '{book['title']}' PDF!")
                                    else:
                                        st.error("❌ PDF file not available for download.")
                            else:
                                # For other book types, show borrow button
                                if st.button("📖 Borrow", key=f"borrow_{book_key}_{idx}", use_container_width=True):
                                    if borrow_book(book):
                                        st.success(f"✅ You have successfully borrowed '{book['title']}'!")
                                        st.balloons()
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error("❌ Unable to borrow book. Please try again.")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("📭 No books match your search criteria.")
        else:
            st.info("📚 No books available at the moment. Check back later!")
    
    elif menu == "📖 My Books":
        st.markdown('<div class="main-header">📖 My Borrowed Books</div>', unsafe_allow_html=True)
        
        users = load_users()
        member_info = users.get(st.session_state.user, {})
        borrowed_books_list = member_info.get('borrowed_books', [])
        
        if borrowed_books_list:
            books = load_books()
            borrowed_books = []
            for book in books:
                book_identifier = f"{book['title']} by {book['author']}"
                if book_identifier in borrowed_books_list:
                    borrowed_books.append(book)
            
            st.write(f"You have **{len(borrowed_books)}** book(s) borrowed:")
            
            for idx, book in enumerate(borrowed_books):
                with st.container():
                    st.markdown('<div class="book-card">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.write(f"**{book.get('title', 'No Title')}**")
                        st.write(f"by {book.get('author', 'Unknown')}")
                        st.write(f"**Type:** {book.get('book_type', 'N/A')}")
                    
                    with col2:
                        st.write(f"**📅 Borrowed on:** {book.get('borrowed_date', 'N/A')}")
                    
                    with col3:
                        book_identifier = f"{book['title']} by {book['author']}"
                        # Generate unique key for return button
                        book_key = generate_book_key(book)
                        if st.button("↩️ Return", key=f"return_{book_key}_{idx}", use_container_width=True):
                            if return_book(book):
                                st.success(f"✅ Book '{book['title']}' returned successfully!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ Unable to return book. Please contact admin.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("📭 You haven't borrowed any books yet.")
            st.markdown("---")
            st.write("**Why not browse our physics collection?**")
            if st.button("🔍 Browse Books", use_container_width=True):
                st.session_state.member_selected_tab = "Browse Books"
                st.rerun()
    
    elif menu == "👤 Profile":
        st.markdown('<div class="main-header">👤 My Profile</div>', unsafe_allow_html=True)
        
        users = load_users()
        member_info = users.get(st.session_state.user, {})
        
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### 📋 Personal Information")
                st.write(f"**👤 Name:** {member_info.get('name', 'N/A')}")
                st.write(f"**📧 Email:** {member_info.get('email', 'N/A')}")
                st.write(f"**🆔 Member ID:** {member_info.get('member_id', 'N/A')}")
                st.write(f"**👤 Username:** `{st.session_state.user}`")
                st.write(f"**📚 Books Currently Borrowed:** {len(member_info.get('borrowed_books', []))}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### 🔐 Change Password")
                
                with st.form("member_password_form"):
                    current_pass = st.text_input("Current Password", type="password")
                    new_pass = st.text_input("New Password", type="password")
                    confirm_pass = st.text_input("Confirm New Password", type="password")
                    
                    if st.form_submit_button("🔐 Update Password", type="primary", use_container_width=True):
                        if current_pass != member_info.get('password'):
                            st.error("❌ Current password is incorrect!")
                        elif new_pass != confirm_pass:
                            st.error("❌ New passwords don't match!")
                        elif not new_pass:
                            st.error("⚠️ New password cannot be empty!")
                        else:
                            users[st.session_state.user]['password'] = new_pass
                            save_users(users)
                            st.success("✅ Password updated successfully!")
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    
    elif menu == "📥 PDF Downloads":
        st.markdown('<div class="main-header">📥 My PDF Downloads</div>', unsafe_allow_html=True)
        
        download_history = load_download_history()
        users = load_users()
        member_info = users.get(st.session_state.user, {})
        
        # Filter download history for current user
        user_downloads = {}
        for book_key, data in download_history.items():
            if st.session_state.user in data.get('user_downloads', {}):
                user_downloads[book_key] = {
                    'title': data['title'],
                    'author': data['author'],
                    'download_count': data['user_downloads'][st.session_state.user],
                    'last_download': None
                }
                
                # Find the last download time
                for download in reversed(data.get('download_times', [])):
                    if download['username'] == st.session_state.user:
                        user_downloads[book_key]['last_download'] = download['timestamp']
                        break
        
        if user_downloads:
            st.write(f"You have downloaded **{len(user_downloads)}** PDF book(s):")
            
            # Sort by last download time (newest first)
            sorted_downloads = sorted(user_downloads.items(), 
                                     key=lambda x: x[1]['last_download'] or '', 
                                     reverse=True)
            
            for book_key, data in sorted_downloads:
                with st.container():
                    st.markdown('<div class="book-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**{data['title']}**")
                        st.write(f"by {data['author']}")
                        st.write(f"**Downloads:** {data['download_count']} time(s)")
                        if data['last_download']:
                            st.write(f"**Last Downloaded:** {data['last_download']}")
                    
                    with col2:
                        # Find the book to get PDF filename
                        books = load_books()
                        pdf_book = None
                        for book in books:
                            if book['title'] == data['title'] and book['author'] == data['author']:
                                pdf_book = book
                                break
                        
                        if pdf_book and pdf_book.get('pdf_filename'):
                            pdf_path = get_pdf_path(pdf_book['pdf_filename'])
                            if pdf_path and os.path.exists(pdf_path):
                                with open(pdf_path, "rb") as pdf_file:
                                    pdf_data = pdf_file.read()
                                    st.download_button(
                                        label="📥 Download Again",
                                        data=pdf_data,
                                        file_name=f"{data['title'].replace(' ', '_')}.pdf",
                                        mime="application/pdf",
                                        key=f"redownload_{book_key}"
                                    )
                        else:
                            st.info("PDF not available")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("📭 You haven't downloaded any PDF books yet.")
            st.markdown("---")
            st.write("**Browse our E-Book collection to download PDFs!**")
            if st.button("🔍 Browse E-Books", use_container_width=True):
                st.session_state.member_selected_tab = "Browse Books"
                st.rerun()

def borrow_book(book):
    """Borrow a book (member function)"""
    books = load_books()
    users = load_users()
    
    for i, b in enumerate(books):
        if (b.get('title') == book.get('title') and 
            b.get('author') == book.get('author') and 
            b.get('status') == 'available'):
            
            # Update book status
            books[i]['status'] = 'borrowed'
            books[i]['borrowed_by'] = st.session_state.user
            books[i]['borrowed_date'] = datetime.now().strftime("%Y-%m-%d")
            
            # Update user's borrowed books
            book_identifier = f"{book['title']} by {book['author']}"
            if 'borrowed_books' not in users[st.session_state.user]:
                users[st.session_state.user]['borrowed_books'] = []
            
            # Check if not already borrowed
            if book_identifier not in users[st.session_state.user]['borrowed_books']:
                users[st.session_state.user]['borrowed_books'].append(book_identifier)
                
                save_books(books)
                save_users(users)
                return True
    
    return False

def borrow_book_admin(book, username):
    """Borrow a book (admin function)"""
    books = load_books()
    users = load_users()
    
    for i, b in enumerate(books):
        if (b.get('title') == book.get('title') and 
            b.get('author') == book.get('author') and 
            b.get('status') == 'available'):
            
            # Update book status
            books[i]['status'] = 'borrowed'
            books[i]['borrowed_by'] = username
            books[i]['borrowed_date'] = datetime.now().strftime("%Y-%m-%d")
            
            # Update user's borrowed books
            book_identifier = f"{book['title']} by {book['author']}"
            if 'borrowed_books' not in users[username]:
                users[username]['borrowed_books'] = []
            
            # Check if not already borrowed
            if book_identifier not in users[username]['borrowed_books']:
                users[username]['borrowed_books'].append(book_identifier)
                
                save_books(books)
                save_users(users)
                return True
    
    return False

def return_book(book):
    """Return a book (member function)"""
    books = load_books()
    users = load_users()
    
    for i, b in enumerate(books):
        if (b.get('title') == book.get('title') and 
            b.get('author') == book.get('author') and 
            b.get('borrowed_by') == st.session_state.user):
            
            # Update book status
            books[i]['status'] = 'available'
            books[i]['borrowed_by'] = None
            books[i]['borrowed_date'] = None
            
            # Update user's borrowed books
            book_identifier = f"{book['title']} by {book['author']}"
            if book_identifier in users[st.session_state.user].get('borrowed_books', []):
                users[st.session_state.user]['borrowed_books'].remove(book_identifier)
            
            save_books(books)
            save_users(users)
            return True
    
    return False

def return_book_admin(book):
    """Return a book (admin function)"""
    books = load_books()
    users = load_users()
    
    borrower_username = book.get('borrowed_by')
    
    for i, b in enumerate(books):
        if (b.get('title') == book.get('title') and 
            b.get('author') == book.get('author')):
            
            # Update book status
            books[i]['status'] = 'available'
            books[i]['borrowed_by'] = None
            books[i]['borrowed_date'] = None
            
            # Update user's borrowed books if username provided
            if borrower_username and borrower_username in users:
                book_identifier = f"{book['title']} by {book['author']}"
                if book_identifier in users[borrower_username].get('borrowed_books', []):
                    users[borrower_username]['borrowed_books'].remove(book_identifier)
            
            save_books(books)
            save_users(users)
            return True
    
    return False

def delete_book(book):
    """Delete a book"""
    books = load_books()
    
    # Remove book from users' borrowed lists
    users = load_users()
    book_identifier = f"{book['title']} by {book['author']}"
    
    for user_info in users.values():
        if 'borrowed_books' in user_info and book_identifier in user_info['borrowed_books']:
            user_info['borrowed_books'].remove(book_identifier)
    save_users(users)
    
    # Delete the book
    books = [b for b in books if not (b.get('title') == book.get('title') and 
                                     b.get('author') == book.get('author'))]
    save_books(books)

def export_to_excel():
    """Export books data to Excel"""
    books = load_books()
    
    if books:
        # Create DataFrame
        data = []
        for book in books:
            data.append({
                "Title": book.get('title', ''),
                "Author": book.get('author', ''),
                "ISBN": book.get('isbn', ''),
                "Category": book.get('category', ''),
                "Subcategory": book.get('subcategory', ''),
                "Type": book.get('book_type', ''),
                "Publisher": book.get('publisher', ''),
                "Year": book.get('year', ''),
                "Status": book.get('status', ''),
                "Borrowed By": book.get('borrowed_by', ''),
                "Borrowed Date": book.get('borrowed_date', ''),
                "Added Date": book.get('added_date', ''),
                "Remarks": book.get('remarks', ''),
                "Has PDF": "Yes" if book.get('pdf_filename') else "No"
            })
        
        df = pd.DataFrame(data)
        
        # Create download link
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Books Data (CSV)",
            data=csv,
            file_name=f"amo_physics_library_books_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No books to export!")

def export_members_to_excel():
    """Export members data to Excel"""
    users = load_users()
    books = load_books()
    members = {k: v for k, v in users.items() if v.get('role') == 'member'}
    
    if members:
        data = []
        for username, info in members.items():
            # Get borrowed book titles
            borrowed_titles = []
            for book_identifier in info.get('borrowed_books', []):
                borrowed_titles.append(book_identifier)
            
            data.append({
                "Username": username,
                "Name": info.get('name', ''),
                "Email": info.get('email', ''),
                "Member ID": info.get('member_id', ''),
                "Books Borrowed": len(info.get('borrowed_books', [])),
                "Borrowed Book Titles": ", ".join(borrowed_titles) if borrowed_titles else "None"
            })
        
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Members Data (CSV)",
            data=csv,
            file_name=f"amo_physics_library_members_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No members to export!")

def export_borrowing_history():
    """Export borrowing history"""
    books = load_books()
    borrowed_books = [b for b in books if b.get('status') == 'borrowed']
    
    if borrowed_books:
        data = []
        for book in borrowed_books:
            data.append({
                "Book Title": book.get('title', ''),
                "Author": book.get('author', ''),
                "ISBN": book.get('isbn', ''),
                "Category": book.get('category', ''),
                "Type": book.get('book_type', ''),
                "Borrowed By": book.get('borrowed_by', ''),
                "Borrowed Date": book.get('borrowed_date', '')
            })
        
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Borrowing History (CSV)",
            data=csv,
            file_name=f"amo_physics_library_borrowing_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No borrowing history to export!")

def main():
    """Main application"""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}
    if 'view_member_books' not in st.session_state:
        st.session_state.view_member_books = None
    if 'edit_member' not in st.session_state:
        st.session_state.edit_member = None
    if 'edit_book_key' not in st.session_state:
        st.session_state.edit_book_key = None
    if 'edit_book_index' not in st.session_state:
        st.session_state.edit_book_index = None
    if 'redirect_to' not in st.session_state:
        st.session_state.redirect_to = None
    
    # Check for redirects
    if st.session_state.get('redirect_to'):
        redirect = st.session_state.redirect_to
        st.session_state.redirect_to = None
        if redirect == "Book Management":
            book_management()
        elif redirect == "Member Management":
            member_management()
        return
    
    # Create logout button in sidebar if logged in
    if st.session_state.logged_in:
        with st.sidebar:
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.clear()
                st.rerun()
            st.markdown("---")
            st.caption(f"© {datetime.now().year} AMO Physics Library")
    
    # Show appropriate page based on login status
    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.role == 'admin':
            admin_dashboard()
        else:
            member_dashboard()

if __name__ == "__main__":
    # Initialize member IDs file if it doesn't exist
    try:
        with open(MEMBER_IDS_FILE, 'r') as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        save_member_ids([], {})
    
    # Initialize download history file if it doesn't exist
    try:
        with open(DOWNLOAD_HISTORY_FILE, 'r') as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        save_download_history({})
    
    main()
