# 🔒 Secure File Management System 🗂️
A secure web-based file management system built with **Flask** and **SQLite** that allows users to register, log in, and manage their files in a private storage space. ✨

---

## 📋 Table of Contents
- [🌟 Features](#-features)
- [⚙️ Installation](#️-installation)
- [🚀 Usage](#-usage)
- [📂 Project Structure](#-project-structure)
- [🔐 Security Measures](#-security-measures)
- [🔮 Future Enhancements](#-future-enhancements)
- [👥 Contributors](#-contributors)


---

## 🌟 Features
- **🔑 User Authentication**  
  Secure registration and login with password hashing
- **📁 File Management**  
  - ⬆️ Upload files with allowed extensions (.txt, .pdf, .png, .jpg, .zip)  
  - ⬇️ Download files from private storage  
  - 🗑️ Delete unwanted files  
- **👤 User Isolation**  
  Each user gets a private directory for file storage  
- **🛡️ Session Management**  
  Protected access to user dashboard  

---

## ⚙️ Installation

### Prerequisites
- Python 3.x 🐍
- pip (Python package manager)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Ayushv366/Secure_file_management_system.git
   cd Secure_file_management_system
Create and activate a virtual environment (recommended):

bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install required packages:

bash
pip install -r requirements.txt
If you don't have a requirements.txt file:

bash
pip install flask werkzeug
🚀 Usage
Initialize the database:

bash
python init_db.py
Run the application:

bash
python app.py
Access the application:

http://localhost:5000
Use the system:

📝 Register a new account

🔑 Log in with your credentials

⬆️⬇️🗑️ Manage files through the dashboard




📂 Project Structure
📁 project-folder/
    ├── 📄 app.py                # Main application
    ├── 📦 users.db              # Database
    ├── 📂 templates/            # HTML pages
    │   ├── 📄 login.html        # Login
    │   ├── 📄 register.html     # Registration
    │   └── 📄 index.html        # Dashboard
    ├── 📂 uploads/              # File storage
        ├── 📂 [username]/       # User folders
            ├── 📄 [files]      # User files



            
🔐 Security Measures
🔒 Password hashing with Werkzeug

🛡️ Secure filename handling

⏱️ Session-based access control

📁 User-specific file isolation

⚠️ Restricted file types






🔮 Future Enhancements
✉️ Email verification

🦠 Malware scanning

👁️ File previews

👨‍💼 Admin panel

🗃️ PostgreSQL/MySQL support

👥 Contributors
Ayush Verma	

Contact:
Geraltthewitcher661@gmail.com


📜 License
MIT License - Feel free to use and contribute! 🎉
