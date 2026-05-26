import hashlib
import os
import json

students_db = {}
exams_db = {}
submissions_db = {}

def register_student(student_id, name, password):
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    students_db[student_id] = {
        "name": name,
        "salt": salt.hex(),
        "password_hash": hashed.hex()
    }
    print(f"Student '{name}' registered successfully.")

def login_student(student_id, password):
    if student_id not in students_db:
        print("Student not found.")
        return False
    student = students_db[student_id]
    salt = bytes.fromhex(student["salt"])
    new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    if new_hash.hex() == student["password_hash"]:
        print(f"Login successful. Welcome, {student['name']}!")
        return True
    else:
        print("Incorrect password. Access denied.")
        return False

def upload_exam(exam_id, exam_content):
    exam_hash = hashlib.sha256(exam_content.encode()).hexdigest()
    exams_db[exam_id] = {
        "content": exam_content,
        "original_hash": exam_hash
    }
    print(f"Exam '{exam_id}' uploaded.")
    print(f"Original Hash: {exam_hash}")

def verify_exam(exam_id):
    if exam_id not in exams_db:
        print("Exam not found.")
        return False
    exam = exams_db[exam_id]
    current_hash = hashlib.sha256(exam["content"].encode()).hexdigest()
    if current_hash == exam["original_hash"]:
        print("Exam Integrity CHECK PASSED - Exam is original and untampered.")
        return True
    else:
        print("ALERT: Exam has been TAMPERED! Hash mismatch detected.")
        return False

def submit_answers(student_id, exam_id, answers):
    combined = student_id + exam_id + json.dumps(answers, sort_keys=True)
    fingerprint = hashlib.sha256(combined.encode()).hexdigest()
    submissions_db[student_id + "_" + exam_id] = {
        "student_id": student_id,
        "exam_id": exam_id,
        "answers": answers,
        "fingerprint": fingerprint
    }
    print(f"Answers submitted by {student_id}.")
    print(f"Answer Sheet Fingerprint: {fingerprint}")

def verify_submission(student_id, exam_id):
    key = student_id + "_" + exam_id
    if key not in submissions_db:
        print("Submission not found.")
        return False
    sub = submissions_db[key]
    combined = student_id + exam_id + json.dumps(sub["answers"], sort_keys=True)
    current_fp = hashlib.sha256(combined.encode()).hexdigest()
    if current_fp == sub["fingerprint"]:
        print("Submission Integrity CHECK PASSED - Answers are original.")
        return True
    else:
        print("ALERT: Answer sheet has been MODIFIED after submission!")
        return False


print("=" * 55)
print("        SECURE EXAM SYSTEM - DEMO")
print("=" * 55)

print("\n--- Student Registration ---")
register_student("S001", "Ali Hassan", "ali_secure_pass")
register_student("S002", "Sara Khan", "sara_secure_pass")

print("\n--- Student Login ---")
login_student("S001", "ali_secure_pass")
login_student("S002", "wrong_password")

print("\n--- Exam Upload ---")
exam_paper = """
CSC232 Information Security - Final Exam
Q1: What is a hash function? (5 marks)
Q2: Explain collision resistance. (5 marks)
Q3: What is a rainbow table attack? (5 marks)
Q4: Why is salt used in password hashing? (5 marks)
"""
upload_exam("EXAM_CSC232", exam_paper)

print("\n--- Exam Integrity Verification ---")
verify_exam("EXAM_CSC232")

print("\n--- Answer Submission ---")
answers = {
    "Q1": "A hash function maps input data to a fixed-size output called a digest.",
    "Q2": "Collision resistance means it is hard to find two inputs with the same hash.",
    "Q3": "A rainbow table attack uses precomputed hashes to crack passwords.",
    "Q4": "Salt makes each hash unique and prevents rainbow table attacks."
}
submit_answers("S001", "EXAM_CSC232", answers)

print("\n--- Submission Integrity Verification ---")
verify_submission("S001", "EXAM_CSC232")

print("\n--- SHA Algorithm Comparison ---")
message = "Secure Exam System"
for algo in ['md5', 'sha1', 'sha256', 'sha512']:
    h = hashlib.new(algo, message.encode()).hexdigest()
    print(f"  {algo.upper():8} ({len(h)*4:3} bits): {h[:45]}...")

print("\n" + "=" * 55)
print("  System secured with SHA-256 + PBKDF2 + Salt")
print("=" * 55)
