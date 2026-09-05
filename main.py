import tkinter as tk
from tkinter import messagebox, simpledialog

# --------------------USER_CLASS--------------------
class User:
    def __init__(self, name, acc, pwd, bal, has_credit=False, credit_limit=0):
        self.name = name
        self.acc = acc
        self.pwd = pwd
        self.balance = bal
        self.has_credit = has_credit
        self.credit_limit = credit_limit
        self.credit_used = 0

    def withdraw(self, amount):
        if (amount <= self.balance):
            self.balance -= amount
            return True

        remaining = amount - self.balance
        available_credit = self.credit_limit - self.credit_used

        if (self.has_credit and remaining <= available_credit):
            self.credit_used += remaining
            self.balance = 0
            return True

        return False

    def deposit(self, amount):
        if (self.credit_used > 0):
            if (amount >= self.credit_used):
                amount -= self.credit_used
                self.credit_used = 0
            else:
                self.credit_used -= amount
                return
        self.balance += amount

# -----------------------USERS----------------------
users = [
    User("SHAYAN", "9211", "shayan40404", 41000, True, 20000),
    User("SABOOR", "0345", "pathan1238", 57440),
    User("SHAKILA", "0088", "fawadkishakila", 25000, True, 15000),
    User("AYAN", "1920", "lalokad007", 5000)
]

current_user = None
attempts = 0

# ----------------------GUI------------------------
root = tk.Tk()
root.title("ATM System")
root.geometry("900x500")
root.configure(bg="#0B2C6D")
root.resizable(False, False)

# --------------------FUNCTIONS---------------------------
def login():
    global current_user, attempts
    acc = acc_entry.get()
    pwd = pass_entry.get()

    for u in users:
        if (u.acc == acc and u.pwd == pwd):
            current_user = u
            acc_entry.delete(0, tk.END)
            pass_entry.delete(0, tk.END)
            show_dashboard()
            return

    attempts += 1
    messagebox.showerror("Error", f"Wrong credentials ({attempts}/3)")
    acc_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)
    if (attempts == 3):
        root.destroy()

def show_dashboard():
    login_frame.pack_forget()
    dash_frame.pack(fill="both", expand=True)
    refresh_labels()

def refresh_labels():
    name_lbl.config(text=current_user.name)
    acc_lbl.config(text=f"Account #{current_user.acc}")
    bal_lbl.config(text=f"$ {current_user.balance:,}")

def get_cash():
    amt = simpledialog.askinteger("Withdraw", "Enter amount to withdraw:")
    if (amt and amt > 0):
        if (current_user.withdraw(amt)):
            refresh_labels()
            messagebox.showinfo("Success", f"${amt} withdrawn successfully!")
        else:
            messagebox.showerror("Error", "Insufficient funds or credit limit exceeded.")
    else:
        messagebox.showerror("Error", "Invalid amount.")

def deposit_money():
    amt = simpledialog.askinteger("Deposit", "Enter amount to deposit:")
    if (amt and amt > 0):
        current_user.deposit(amt)
        refresh_labels()
        messagebox.showinfo("Success", f"${amt} deposited successfully!")
    else:
        messagebox.showerror("Error", "Invalid amount.")

def payments():
    messagebox.showinfo("Payments", "Payments feature coming soon!")

def credit_card():
    if (not current_user.has_credit):
        messagebox.showinfo("Credit Card", "No credit card linked to this account.")
        return
    messagebox.showinfo(
        "Credit Card Details",
        f"Credit Limit: ${current_user.credit_limit:,}\n"
        f"Credit Used: ${current_user.credit_used:,}\n"
        f"Available Credit: ${current_user.credit_limit - current_user.credit_used:,}"
    )

def account_settings():
    messagebox.showinfo(
        "Account Settings",
        f"Name: {current_user.name}\n"
        f"Account: {current_user.acc}\n"
        f"Credit Card: {'Yes' if current_user.has_credit else 'No'}\n"
        f"Credit Limit: ${current_user.credit_limit:,}\n"
        f"Credit Used: ${current_user.credit_used:,}"
    )

def other():
    messagebox.showinfo("Other", "Other services feature coming soon!")

def quick_cash():
    if (current_user.withdraw(100)):
        refresh_labels()
        messagebox.showinfo("Quick Cash", "$100 withdrawn successfully!")
    else:
        messagebox.showerror("Error", "Not enough balance or credit.")

def logout():
    global current_user, attempts
    current_user = None
    attempts = 0
    dash_frame.pack_forget()
    login_frame.pack(expand=True)

# ------------------LOGIN_SCREEN-----------------------
login_frame = tk.Frame(root, bg="#0B2C6D")
login_frame.pack(expand=True)

title_label = tk.Label(login_frame, text="ATM LOGIN", fg="white", bg="#0B2C6D", font=("Arial", 28, "bold"))
title_label.pack(pady=40)

acc_label = tk.Label(login_frame, text="Account Number:", fg="white", bg="#0B2C6D", font=("Arial", 14))
acc_label.pack(pady=(10, 5))
acc_entry = tk.Entry(login_frame, font=("Arial", 14), width=25, bd=2, relief="solid")
acc_entry.pack(pady=(0, 20))

pass_label = tk.Label(login_frame, text="Password:", fg="white", bg="#0B2C6D", font=("Arial", 14))
pass_label.pack(pady=(10, 5))
pass_entry = tk.Entry(login_frame, font=("Arial", 14), show="*", width=25, bd=2, relief="solid")
pass_entry.pack(pady=(0, 30))

login_btn = tk.Button(login_frame, text="LOGIN", font=("Arial", 16, "bold"), bg="#17B3F0", fg="white", width=20, height=2, bd=0, activebackground="#149ACD", command=login)
login_btn.pack(pady=20)

# --------------------DASHBOARD--------------------
dash_frame = tk.Frame(root, bg="#0B2C6D")

# Left_Panel____
left = tk.Frame(dash_frame, bg="#0E4DA4", width=250, height=500)
left.pack(side="left", fill="y")
left.pack_propagate(False)  # Prevent resizing

tk.Label(left, text="ATM", bg="#0E4DA4", fg="white", font=("Arial", 20, "bold")).pack(anchor="nw", padx=20, pady=20)

tk.Label(left, text="Welcome", bg="#0E4DA4", fg="#A7C7FF", font=("Arial", 12)).pack(anchor="w", padx=20)

name_lbl = tk.Label(left, bg="#0E4DA4", fg="white", font=("Arial", 16, "bold"))
name_lbl.pack(anchor="w", padx=20, pady=5)

acc_lbl = tk.Label(left, bg="#0E4DA4", fg="#A7C7FF", font=("Arial", 12))
acc_lbl.pack(anchor="w", padx=20, pady=10)

bal_lbl = tk.Label(left, bg="#0E4DA4", fg="white", font=("Arial", 18, "bold"))
bal_lbl.pack(anchor="w", padx=20)

logout_btn = tk.Button(left, text="Logout", font=("Arial", 12), bg="#EF4444", fg="white", width=10, command=logout)
logout_btn.pack(side="bottom", pady=20)

# Right_Panel____
right = tk.Frame(dash_frame, bg="#0B2C6D")
right.pack(expand=True, fill="both", padx=20, pady=20)

def atm_button(text, cmd):
    return tk.Button(
        right, text=text,
        bg="#17B3F0", fg="white",
        font=("Arial", 14),
        width=18, height=3,
        bd=0, activebackground="#149ACD",
        command=cmd
    )

# Buttons_Grid___
atm_button("Get Cash", get_cash).grid(row=0, column=0, padx=15, pady=15)
atm_button("Deposit", deposit_money).grid(row=0, column=1, padx=15, pady=15)

atm_button("Payments", payments).grid(row=1, column=0, padx=15, pady=15)
atm_button("Credit Card", credit_card).grid(row=1, column=1, padx=15, pady=15)

atm_button("Account Settings", account_settings).grid(row=2, column=0, padx=15, pady=15)
atm_button("Other", other).grid(row=2, column=1, padx=15, pady=15)

# Quick_Cash =>(advance option)
quick = tk.Frame(dash_frame, bg="#0B2C6D")
quick.pack(side="bottom", fill="x", pady=20)

tk.Button(
    quick, text="$100     Quick Cash  ➜",
    bg="#E91E63", fg="white",
    font=("Arial", 16, "bold"),
    bd=0, height=2,
    command=quick_cash
).pack(fill="x", padx=200)

root.mainloop()