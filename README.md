# Secure Exam System Using Hash Functions

A Python-based secure exam management system built using cryptographic hash functions (SHA-256 & PBKDF2). This project was developed as part of the **CSC232 - Information Security** course at COMSATS University Islamabad, Attock Campus.

---

## Project Info

| Field       | Detail                              |
|-------------|--------------------------------------|
| Course      | CSC232 — Information Security        |
| Lab         | Lab 06 — Secure Hash Function        |
| Semester    | Spring 2026                          |
| Class       | SE IV                                |
| University  | COMSATS University Islamabad         |

---

## What This Project Does

This system solves a real-world problem — **exam papers getting leaked or tampered with**. It uses SHA-256 hash functions to:

- Securely store and verify student passwords (PBKDF2 + Salt)
- Lock the exam paper with a SHA-256 fingerprint at upload time
- Detect any modification to the exam paper before distribution
- Fingerprint student answer sheets after submission
- Detect any post-submission tampering with answers

---

## How It Works

### 1. Student Registration & Login
- Password is hashed using **PBKDF2-HMAC-SHA256** with a random 16-byte salt
- The real password is **never stored** — only the hash
- Login works by re-hashing the entered password and comparing

### 2. Exam Paper Security
- When the teacher uploads the exam, a **SHA-256 hash** (digital fingerprint) is generated
- Before distribution, the system re-hashes the paper and compares
- If even **one character** was changed, the hash is completely different — tampering is instantly detected

### 3. Answer Sheet Fingerprinting
- After a student submits answers, a SHA-256 fingerprint of `StudentID + ExamID + Answers` is saved
- Any modification after submission changes the fingerprint — **proving tampering**

---

## Functions

| Function | Description |
|----------|-------------|
| `register_student()` | Hashes and stores student password securely |
| `login_student()` | Verifies login by comparing hashes |
| `upload_exam()` | Uploads exam and stores its SHA-256 fingerprint |
| `verify_exam()` | Re-hashes exam and checks for tampering |
| `submit_answers()` | Fingerprints and stores student answer sheet |
| `verify_submission()` | Verifies answer sheet was not modified |

---

## Technologies Used

- **Language:** Python 3
- **Libraries:** `hashlib`, `os`, `json` (all built-in — no installation needed)
- **Algorithm:** SHA-256, PBKDF2-HMAC-SHA256

---

## How to Run

```bash
python secure_exam_system.py
