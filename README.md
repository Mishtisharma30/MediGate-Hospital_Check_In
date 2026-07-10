# MediGate - Contactless Hospital Check-In System

# Overview:
A Flask and MySQL based backend application for hospital patient registration, contactless check-in, and administration using face recognition.

The system allows patients to register with their personal details and facial data. During hospital visits, patients can check in using facial recognition, while administrators can securely manage patient records through a dedicated dashboard.

---

# Features

## Patient Registration

- Register patients using personal information
- Upload patient photograph
- Face encoding generation using `face_recognition`
- Prevent duplicate registrations
- Store patient details and face encoding in MySQL

## Contactless Check-In

- Webcam image capture
- Facial recognition against registered patients
- Automatic patient identification
- Appointment confirmation with generated token
- Handles unknown or unregistered faces

## Hospital Admin

- Admin registration and login
- Session-based authentication
- View all registered patients
- View individual patient information

---

# Tech Stack

### Backend

- Python
- Flask
- MySQL
- face_recognition
- dlib
- NumPy

### Database

- MySQL

### Frontend

- HTML
- CSS
- JavaScript

> The frontend templates are pre-built and are used only to demonstrate backend functionality.

---

# Project Structure

```text
Hospital_CheckIn/
│
├── registration/
│   ├── registration.py
│   ├── create_person_group_person.py
│   ├── templates/
│   └── static/
│
├── face_recognition/
│   ├── check_in.py
│   ├── identify.py
│   ├── templates/
│   └── static/
│
├── hospital_admin/
│   ├── hospital_admin.py
│   ├── templates/
│   └── static/
│
├── images/
├── setup/
├── requirements.txt
├── setup_db.sql
└── README.md
```

---

# Workflow

## 1. Patient Registration

- Patient enters personal information
- Uploads facial image
- Face encoding is generated
- Patient information is stored in MySQL

## 2. Patient Check-In

- Patient captures image using webcam
- Stored face encodings are compared
- Matching patient is identified
- Appointment details and token number are displayed

## 3. Admin Dashboard

- Admin logs in securely
- View all registered patients
- Access detailed patient information

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Mishtisharma30/MediGate.git
cd MediGate
```

## Create Virtual Environment

### Windows

```bash
python -m venv myenv
myenv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Database

Execute:

```text
setup_db.sql
```

using MySQL to create the required database and tables.

---

# Running the Project

## Registration Module

```bash
python registration\registration.py -u <username> -p <password>
```

---

## Patient Check-In Module

```bash
python face_recognition\check_in.py -u <username> -p <password>
```

---

## Hospital Admin Module

```bash
python hospital_admin\hospital_admin_.py -u <username> -p <password>
```

---

# Known Limitations

- Passwords stored as plaintext — admin account passwords in the accounts table are not hashed. A production system must use bcrypt or argon2.
- Single-threaded dev server — app.run(debug=True) is Flask's development server and is not suitable for concurrent users. Production deployment would require Gunicorn.
- Three separate apps — registration, check-in, and admin run as independent Flask processes. A cleaner architecture would merge them using Flask Blueprints with a single    entry point.
- No face liveness detection — the system cannot distinguish a real face from a photograph of a face held up to the camera.

---

# Future Improvements

- Password hashing
- REST API support
- Docker deployment
- JWT authentication
- Email/SMS notifications
- Appointment scheduling
- Audit logging

---
---
