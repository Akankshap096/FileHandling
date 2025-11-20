import random
import datetime
import os

logged_user = {}
users_file = "users.txt"
score_file = "scores.txt"

# ---------- Helper functions ----------
def read_users():
    if not os.path.exists(users_file):
        open(users_file, 'w').close()
    with open(users_file, "r") as f:
        return [line.strip().split('|') for line in f if line.strip()]

def write_users(users):
    with open(users_file, "w") as f:
        for user in users:
            f.write('|'.join(user) + "\n")

def find_user(enrollment):
    users = read_users()
    for user in users:
        if user[0] == enrollment:
            return user
    return None

# ---------- Registration ----------
def register():
    print("\n--- Registration ---")
    enrollment = input("Enrollment no: ")
    if find_user(enrollment):
        print("User already registered.")
        return

    name = input("Name: ")
    email = input("Email: ")
    branch = input("Branch: ")
    year = input("Year: ")
    contact = input("Contact: ")
    password = input("Password: ")
    role = "user"

    with open(users_file, "a") as f:
        f.write(f"{enrollment}|{name}|{email}|{branch}|{year}|{contact}|{password}|{role}\n")
    print("✅ Registration successful!")

# ---------- Login ----------
def login():
    global logged_user
    print("\n--- Login ---")
    enrollment = input("Enrollment no: ")
    password = input("Password: ")
    users = read_users()
    for user in users:
        if user[0] == enrollment and user[6] == password:
            logged_user = {
                "enrollment": user[0],
                "name": user[1],
                "email": user[2],
                "branch": user[3],
                "year": user[4],
                "contact": user[5],
                "role": user[7]
            }
            print(f"✅ Welcome {user[1]}!")
            return
    print("❌ Invalid credentials!")

# ---------- Profile ----------
def show_profile():
    if not logged_user:
        print("Login first.")
        return
    print("\n--- Profile ---")
    for key, value in logged_user.items():
        print(f"{key.capitalize()}: {value}")

# ---------- Update Profile ----------
def update_profile():
    if not logged_user:
        print("Login first.")
        return
    print("\n--- Update Profile ---")
    users = read_users()
    for user in users:
        if user[0] == logged_user["enrollment"]:
            user[1] = input("Name: ") or user[1]
            user[2] = input("Email: ") or user[2]
            user[3] = input("Branch: ") or user[3]
            user[4] = input("Year: ") or user[4]
            user[5] = input("Contact: ") or user[5]
            logged_user.update({
                "name": user[1], "email": user[2], "branch": user[3],
                "year": user[4], "contact": user[5]
            })
            break
    write_users(users)
    print("✅ Profile updated!")

# ---------- Quiz ----------
def attempt_quiz():
    if not logged_user:
        print("Login first.")
        return
    print("\n--- Quiz Categories ---")
    print("1. DSA\n2. DBMS\n3. PYTHON")
    choice = input("Choose category (1/2/3): ")

    category_map = {"1": "dsa", "2": "dbms", "3": "python"}
    if choice not in category_map:
        print("Invalid category!")
        return

    filename = category_map[choice] + ".txt"
    if not os.path.exists(filename):
        print("No quiz file found for this category.")
        return

    with open(filename, "r") as f:
        questions = [line.strip().split('|') for line in f if line.strip()]
    random.shuffle(questions)

    score = 0
    for i, q in enumerate(questions[:5], 1):
        print(f"\nQ{i}: {q[0]}")
        for j in range(1, 5):
            print(f"{j}. {q[j]}")
        ans = input("Your answer (1-4): ")
        if ans == q[5]:
            score += 1

    print(f"\n✅ Your Score: {score}/{len(questions[:5])}")

    with open(score_file, "a") as f:
        f.write(f"{logged_user['enrollment']}|{category_map[choice]}|{score}/{len(questions[:5])}|{datetime.datetime.now()}\n")

# ---------- Logout ----------
def logout():
    global logged_user
    logged_user = {}
    print("Logged out successfully!")

# ---------- Main Menu ----------
def main():
    while True:
        print("\nWelcome to LNCT Quiz App")
        print("""
        1. Register
        2. Login
        3. Profile
        4. Update Profile
        5. Attempt Quiz
        6. Logout
        7. Exit
        """)
        response = input("Choose option: ")

        if response == '1':
            register()
        elif response == '2':
            login()
        elif response == '3':
            show_profile()
        elif response == '4':
            update_profile()
        elif response == '5':
            attempt_quiz()
        elif response == '6':
            logout()
        elif response == '7':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option!")

main()