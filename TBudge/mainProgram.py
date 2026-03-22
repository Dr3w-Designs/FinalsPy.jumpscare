import pickle, os  # For data persistence
from datetime import datetime  # For date handling
from kivy.app import App  # Main Kivy app class
from kivy.core.window import Window  # Window configuration
from kivy.uix.screenmanager import ScreenManager, Screen  # Screen management
from kivy.uix.boxlayout import BoxLayout  # Vertical/horizontal layouts
from kivy.uix.gridlayout import GridLayout  # Grid layouts
from kivy.uix.scrollview import ScrollView  # Scrollable views
from kivy.uix.label import Label  # Text display
from kivy.uix.button import Button  # Interactive buttons
from kivy.uix.textinput import TextInput  # Text input fields
from kivy.uix.popup import Popup  # Popup dialogs
from kivy.uix.image import Image  # Image widgets for icons
from kivy.uix.spinner import Spinner  # For dropdown categories
from kivy.uix.widget import Widget  # For custom widgets
from kivy.graphics import Color, RoundedRectangle, Rectangle  # Graphics for styling

# ------------------ MOBILE SIZE & BACKGROUND ------------------
Window.size = (360, 640)
Window.clearcolor = (0.95, 0.95, 0.95, 1)

USERS_FILE = "users.dat"

# ------------------- FILE FUNCTIONS -------------------
def load_users():  # Load user data from file
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def save_users(users):  # Save user data to file
    with open(USERS_FILE, "wb") as f:
        pickle.dump(users, f)

def get_expense_file(email):  # Get expense file path for user
    return f"expenses_{email}.dat"

def get_budget_file(email):  # Get budget file path for user
    return f"budget_{email}.dat"

def load_expenses(email):  # Load expenses for user
    file = get_expense_file(email)
    if os.path.exists(file):
        with open(file, "rb") as f:
            return pickle.load(f)
    return []

def save_expenses(email, data):  # Save expenses for user
    file = get_expense_file(email)
    with open(file, "wb") as f:
        pickle.dump(data, f)

def load_budget(email):  # Load budget for user
    file = get_budget_file(email)
    if os.path.exists(file):
        with open(file, "rb") as f:
            return pickle.load(f)
    return 0.0

def save_budget(email, amount):  # Save budget for user
    file = get_budget_file(email)
    with open(file, "wb") as f:
        pickle.dump(amount, f)

# ------------------- LOGIN SCREEN -------------------
class LoginScreen(Screen):
    def __init__(self, sm, nav_bar, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm  # Reference to screen manager
        self.nav_bar = nav_bar  # Reference to navigation bar
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(Image(source="icons/TBudge.png", size_hint_y=None, height=180, fit_mode='contain'))
        layout.add_widget(Label(text="Budge a goal today in Budgeting with TBudge", size_hint_y=None, height=40, color=(0,0,0,1)))
        layout.add_widget(Label(text="Login Now!", size_hint_y=None, height=40, color=(0.15,0.4,0.9,1), bold=True))

        self.email_input = TextInput(hint_text="Email", size_hint_y=None, height=40, foreground_color=(0,0,0,1))
        self.pwd_input = TextInput(hint_text="Password", password=True, size_hint_y=None, height=40, foreground_color=(0,0,0,1))

        login_btn = Button(text="Login", size_hint_y=None, height=45, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        login_btn.bind(on_press=self.login)  # Bind login button

        register_btn = Button(text="Register", size_hint_y=None, height=45, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        register_btn.bind(on_press=self.register)  # Bind register button

        layout.add_widget(self.email_input)
        layout.add_widget(self.pwd_input)
        layout.add_widget(login_btn)
        layout.add_widget(register_btn)
        self.add_widget(layout)

    def login(self, instance):  # Handle login attempt
        email = self.email_input.text.strip()
        pwd = self.pwd_input.text.strip()
        users = load_users()
        if email in users and users[email] == pwd:
            self.sm.current_user = email
            self.sm.current = "home"
            self.email_input.text = ""
            self.pwd_input.text = ""
            # Show nav bar
            self.nav_bar.height = 60
            self.nav_bar.opacity = 1
            self.nav_bar.disabled = False
        else:
            Popup(title="Error", content=Label(text="Invalid credentials", color=(0,0,0,1)), size_hint=(0.6,0.3)).open()

    def register(self, instance):  # Switch to register screen
        self.sm.current = "register"

# ------------------- REGISTER SCREEN -------------------
class RegisterScreen(Screen):
    def __init__(self, sm, nav_bar, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm  # Reference to screen manager
        self.nav_bar = nav_bar  # Reference to navigation bar
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(Image(source="icons/TBudge.png", size_hint_y=None, height=180, fit_mode='contain'))
        layout.add_widget(Label(text="Budge a goal today in Budgeting with TBudge", size_hint_y=None, height=40, color=(0,0,0,1)))
        layout.add_widget(Label(text="Register Now", size_hint_y=None, height=40, color=(0.15,0.4,0.9,1), bold=True))

        self.email_input = TextInput(hint_text="Email", size_hint_y=None, height=40, foreground_color=(0,0,0,1))
        self.pwd_input = TextInput(hint_text="Password", password=True, size_hint_y=None, height=40, foreground_color=(0,0,0,1))

        register_btn = Button(text="Register", size_hint_y=None, height=45, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        register_btn.bind(on_press=self.register)  # Bind register button

        back_btn = Button(text="Back to Login", size_hint_y=None, height=45, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        back_btn.bind(on_press=lambda x: self.sm.switch_to_login())  # Bind back button

        layout.add_widget(self.email_input)
        layout.add_widget(self.pwd_input)
        layout.add_widget(register_btn)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def register(self, instance):  # Handle registration
        email = self.email_input.text.strip()
        pwd = self.pwd_input.text.strip()
        if not email or not pwd:
            Popup(title="Error", content=Label(text="Please fill all fields", color=(0,0,0,1)), size_hint=(0.6,0.3)).open()
            return
        users = load_users()
        if email in users:
            Popup(title="Error", content=Label(text="User already exists", color=(0,0,0,1)), size_hint=(0.6,0.3)).open()
            return
        users[email] = pwd
        save_users(users)
        Popup(title="Success", content=Label(text="Registered! Please login.", color=(0,0,0,1)), size_hint=(0.6,0.3)).open()
        self.sm.switch_to_login()

# ------------------- HOME SCREEN -------------------
class HomeScreen(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm  # Reference to screen manager
        self.expenses = []  # List of expenses
        self.budget = 0.0  # User's budget

        main = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Wallet Card - displays budget info with Logo
        self.wallet_card = BoxLayout(orientation='horizontal', size_hint_y=None, height=120, padding=10, spacing=10)
        with self.wallet_card.canvas.before:
            Color(0.15,0.4,0.9,1)
            self.rect = RoundedRectangle(pos=self.wallet_card.pos, size=self.wallet_card.size, radius=[12])
        self.wallet_card.bind(pos=self.update_rect, size=self.update_rect)
        self.wallet_logo = Image(source='icons/Logo.png', size_hint_x=0.3, fit_mode='contain')
        self.wallet_text = Label(text='', markup=True, color=(1,1,1,1), valign='middle', halign='left')
        self.wallet_text.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        self.wallet_card.add_widget(self.wallet_logo)
        self.wallet_card.add_widget(self.wallet_text)
        main.add_widget(self.wallet_card)

        # Add Expense Button
        add_btn = Button(text="Add Expense", size_hint_y=None, height=45, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        add_btn.bind(on_press=self.add_expense_popup)
        main.add_widget(add_btn)

        # Scrollable Expenses List
        scroll = ScrollView()
        self.list_layout = GridLayout(cols=1, size_hint_y=None, spacing=5, padding=5)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        scroll.add_widget(self.list_layout)
        main.add_widget(scroll)

        self.add_widget(main)

    def update_rect(self, instance, value):  # Update rounded rectangle position/size
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_enter(self):  # Called when screen is entered
        self.load_user_data()

    def load_user_data(self):  # Load user's expenses and budget
        email = self.sm.current_user
        self.expenses = load_expenses(email)
        self.budget = load_budget(email)
        self.update_home()

    def update_home(self):  # Refresh home screen display
        total = sum([e["amount"] for e in self.expenses])
        remaining = self.budget - total
        remaining_color = "[color=00FF00]" if remaining >=0 else "[color=FF0000]"
        self.wallet_text.text = f"[b]Wallet[/b]\nTotal Spent: ₱{total:.2f}\nBudget: ₱{self.budget:.2f}\nRemaining: {remaining_color}₱{remaining:.2f}[/color]"

        # Expenses list with Edit/Delete buttons
        self.list_layout.clear_widgets()
        for idx, e in enumerate(self.expenses):
            box = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
            box.add_widget(Label(text=f"{e['category']}", size_hint_x=0.3, color=(0,0,0,1)))
            box.add_widget(Label(text=f"₱{e['amount']}", size_hint_x=0.3, color=(0,0,0,1)))
            box.add_widget(Label(text=e['date'], size_hint_x=0.2, color=(0,0,0,1)))
            edit_btn = Button(background_normal='icons/Edit.png', background_down='icons/Edit.png', size_hint_x=None, width=30, height=30, background_color=(0.15,0.4,0.9,1))
            edit_btn.bind(on_press=lambda x, i=idx: self.edit_expense_popup(i))
            delete_btn = Button(background_normal='icons/Trash.png', background_down='icons/Trash.png', size_hint_x=None, width=30, height=30, background_color=(1,0,0,1))
            delete_btn.bind(on_press=lambda x, i=idx: self.delete_expense(i))
            box.add_widget(edit_btn)
            box.add_widget(delete_btn)
            self.list_layout.add_widget(box)
            # Gold separator
            separator = Widget(size_hint_y=None, height=2)
            with separator.canvas:
                Color(1,0.85,0,1)
                Rectangle(pos=separator.pos, size=separator.size)
            self.list_layout.add_widget(separator)

    def add_expense_popup(self, instance):  # Show popup to add new expense
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        # Spacer to remove grey area
        layout.add_widget(Widget(size_hint_y=None, height=20))
        # Category input with dropdown
        cat_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
        self.cat_input = TextInput(hint_text="Category", size_hint_x=0.8, foreground_color=(0,0,0,1))
        dropdown_btn = Button(text="▼", size_hint_x=0.2, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        dropdown_btn.bind(on_press=self.show_category_dropdown)
        cat_layout.add_widget(self.cat_input)
        cat_layout.add_widget(dropdown_btn)
        layout.add_widget(cat_layout)
        amt_input = TextInput(hint_text="Amount", size_hint_y=None, height=40, foreground_color=(0,0,0,1))
        add_btn = Button(text="Add", size_hint_y=None, height=40, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        close_btn = Button(text="X", size_hint_y=None, height=40, background_color=(1,1,1,1), color=(0,0,0,1), size_hint_x=0.2)
        btn_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
        btn_layout.add_widget(add_btn)
        btn_layout.add_widget(close_btn)
        layout.add_widget(amt_input)
        layout.add_widget(btn_layout)
        popup = Popup(title="Add Expense", content=layout, size_hint=(0.8,0.5))
        add_btn.bind(on_press=lambda x: self.save_expense(self.cat_input.text, amt_input.text, popup))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def show_category_dropdown(self, instance):
        categories = list(set(e['category'] for e in self.expenses))
        if categories:
            dropdown = DropDown()
            for cat in categories:
                btn = Button(text=cat, size_hint_y=None, height=40, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
                btn.bind(on_release=lambda btn, cat=cat: (dropdown.select(cat), setattr(self.cat_input, 'text', cat)))
                dropdown.add_widget(btn)
            dropdown.open(instance)

    def save_expense(self, category, amount, popup):  # Save new expense
        try:
            amt = float(amount)
            if not category or category == 'Select Category':
                raise ValueError
            e = {"category": category, "amount": amt, "date": datetime.now().strftime("%Y-%m-%d")}
            self.expenses.append(e)
            save_expenses(self.sm.current_user, self.expenses)
            popup.dismiss()
            self.update_home()
        except:
            Popup(title="Error", content=Label(text="Invalid input", color=(0,0,0,1)), size_hint=(0.6,0.3)).open()

    def edit_expense_popup(self, idx):  # Show popup to edit expense
        e = self.expenses[idx]
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        # Spacer
        layout.add_widget(Widget(size_hint_y=None, height=20))
        # Category input with dropdown
        cat_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
        self.edit_cat_input = TextInput(text=e['category'], size_hint_x=0.8, foreground_color=(0,0,0,1))
        dropdown_btn = Button(text="▼", size_hint_x=0.2, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        dropdown_btn.bind(on_press=self.show_edit_category_dropdown)
        cat_layout.add_widget(self.edit_cat_input)
        cat_layout.add_widget(dropdown_btn)
        layout.add_widget(cat_layout)
        amt_input = TextInput(text=str(e['amount']), size_hint_y=None, height=40, foreground_color=(0,0,0,1))
        save_btn = Button(text="Save", size_hint_y=None, height=40, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        close_btn = Button(text="X", size_hint_y=None, height=40, background_color=(1,1,1,1), color=(0,0,0,1), size_hint_x=0.2)
        btn_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(close_btn)
        layout.add_widget(amt_input)
        layout.add_widget(btn_layout)
        popup = Popup(title="Edit Expense", content=layout, size_hint=(0.8,0.5))
        save_btn.bind(on_press=lambda x: self.save_edit(idx, self.edit_cat_input.text, amt_input.text, popup))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def show_edit_category_dropdown(self, instance):
        categories = list(set(e['category'] for e in self.expenses))
        if categories:
            dropdown = DropDown()
            for cat in categories:
                btn = Button(text=cat, size_hint_y=None, height=40, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
                btn.bind(on_release=lambda btn, cat=cat: (dropdown.select(cat), setattr(self.edit_cat_input, 'text', cat)))
                dropdown.add_widget(btn)
            dropdown.open(instance)

    def save_edit(self, idx, category, amount, popup):  # Save edited expense
        try:
            amt = float(amount)
            if not category or category == 'Select Category':
                raise ValueError
            self.expenses[idx]['category'] = category
            self.expenses[idx]['amount'] = amt
            save_expenses(self.sm.current_user, self.expenses)
            popup.dismiss()
            self.update_home()
        except:
            Popup(title="Error", content=Label(text="Invalid input", color=(0,0,0,1)), size_hint=(0.6,0.3)).open()

    def delete_expense(self, idx):  # Delete expense
        self.expenses.pop(idx)
        save_expenses(self.sm.current_user, self.expenses)
        self.update_home()

# ------------------- BUDGET SCREEN -------------------
class BudgetScreen(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm  # Reference to screen manager
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(Image(source="icons/SetBudget.png", size_hint_y=None, height=120, fit_mode='contain'))
        layout.add_widget(Label(text="Set Monthly Budget", size_hint_y=None, height=50, color=(0.15,0.4,0.9,1)))
        self.budget_input = TextInput(hint_text="Enter budget", size_hint_y=None, height=40, foreground_color=(0,0,0,1))
        layout.add_widget(self.budget_input)
        save_btn = Button(text="Save Budget", size_hint_y=None, height=45, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        save_btn.bind(on_press=self.save_budget)  # Bind save button
        layout.add_widget(save_btn)
        self.add_widget(layout)

    def on_enter(self):  # Load current budget when entering screen
        self.budget_input.text = str(load_budget(self.sm.current_user))

    def save_budget(self, instance):  # Save new budget
        try:
            amount = float(self.budget_input.text)
            save_budget(self.sm.current_user, amount)
            Popup(title="Success", content=Label(text="Budget saved", color=(0,0,0,1)), size_hint=(0.6,0.3)).open()
        except:
            Popup(title="Error", content=Label(text="Invalid input", color=(0,0,0,1)), size_hint=(0.6,0.3)).open()

# ------------------- PROFILE SCREEN -------------------
class ProfileScreen(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm  # Reference to screen manager
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(Image(source="icons/UserProfile.png", size_hint_y=None, height=120, fit_mode='contain'))
        layout.add_widget(Label(text="Profile", size_hint_y=None, height=50, color=(0.15,0.4,0.9,1)))
        self.info_label = Label(text="", size_hint_y=None, height=60, color=(0,0,0,1))
        layout.add_widget(self.info_label)

        logout_btn = Button(text="Logout", size_hint_y=None, height=45, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        logout_btn.bind(on_press=self.logout)  # Bind logout button
        layout.add_widget(logout_btn)

        delete_btn = Button(text="Delete Account", size_hint_y=None, height=45, background_color=(1,0,0,1), color=(1,1,1,1))
        delete_btn.bind(on_press=self.confirm_delete_account)
        layout.add_widget(delete_btn)

        self.add_widget(layout)

    def on_enter(self):  # Display user info when entering screen
        self.info_label.text = f"User: {self.sm.current_user}"

    def logout(self, instance):  # Handle logout
        self.sm.current_user = None
        self.sm.current = "login"
        # Hide nav bar
        self.sm.nav_bar.height = 0
        self.sm.nav_bar.opacity = 0
        self.sm.nav_bar.disabled = True

    def confirm_delete_account(self, instance):
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        content.add_widget(Label(text="Delete account and all data?", color=(0,0,0,1)))
        action_bar = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=45)
        yes_btn = Button(text="Yes", background_color=(1,0,0,1), color=(1,1,1,1))
        no_btn = Button(text="No", background_color=(0.7,0.7,0.7,1), color=(0,0,0,1))
        action_bar.add_widget(yes_btn)
        action_bar.add_widget(no_btn)
        content.add_widget(action_bar)

        popup = Popup(title="Confirm Delete", content=content, size_hint=(0.8,0.4))
        yes_btn.bind(on_press=lambda x: self.delete_account(popup))
        no_btn.bind(on_press=lambda x: popup.dismiss())
        popup.open()

    def delete_account(self, popup):
        popup.dismiss()
        email = self.sm.current_user
        if email:
            users = load_users()
            if email in users:
                del users[email]
                save_users(users)
            for file in [get_expense_file(email), get_budget_file(email)]:
                if os.path.exists(file):
                    os.remove(file)

        self.sm.current_user = None
        self.sm.current = "login"
        self.sm.nav_bar.height = 0
        self.sm.nav_bar.opacity = 0
        self.sm.nav_bar.disabled = True

        Popup(title="Deleted", content=Label(text="Account deleted.", color=(0,0,0,1)), size_hint=(0.6,0.3)).open()

# ------------------- SCREEN MANAGER -------------------
class FintechSM(ScreenManager):
    def __init__(self, nav_bar, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None  # Current logged-in user
        self.nav_bar = nav_bar  # Reference to navigation bar
        self.login_screen = LoginScreen(self, nav_bar, name="login")
        self.register_screen = RegisterScreen(self, nav_bar, name="register")
        self.home_screen = HomeScreen(self, name="home")
        self.budget_screen = BudgetScreen(self, name="budget")
        self.profile_screen = ProfileScreen(self, name="profile")

        self.add_widget(self.login_screen)
        self.add_widget(self.register_screen)
        self.add_widget(self.home_screen)
        self.add_widget(self.budget_screen)
        self.add_widget(self.profile_screen)

    def switch_to_login(self):  # Switch to login screen and hide nav bar
        self.current = "login"
        self.nav_bar.height = 0
        self.nav_bar.opacity = 0
        self.nav_bar.disabled = True

# ------------------- APP -------------------
class FintechApp(App):
    def build(self):  # Build the main app layout
        root = BoxLayout(orientation="vertical")
        self.nav_bar = BoxLayout(size_hint_y=None, height=60, spacing=5, padding=[100,5,100,5], opacity=0, disabled=True)  # Bottom nav bar
        btn_specs = [("home","icons/Home.png"),("budget","icons/Budget.png"),("profile","icons/Profile.png")]
        for name, icon_path in btn_specs:
            btn = Button(background_normal=icon_path, background_down=icon_path, border=(0,0,0,0), size_hint_x=None, width=40, height=40, background_color=(0.15,0.4,0.9,1))
            btn.bind(on_press=lambda x, n=name: self.nav_press(n))  # Bind nav button
            self.nav_bar.add_widget(btn)
        self.sm = FintechSM(self.nav_bar)  # Create screen manager
        root.add_widget(self.sm)
        root.add_widget(self.nav_bar)
        return root

    def nav_press(self, name):  # Handle navigation button press
        self.sm.current = name

if __name__ == "__main__":
    FintechApp().run()  # Run the app
# PROGRAM SPECIFICATIONS:
# Good layout (GUI)
# Data persistence: File Handling (Binary file) w/ CRUD functionality
# Exception handling
# Collections
# KEY CONCEPT / PROGRAM BASIS: Expenses Tracker

