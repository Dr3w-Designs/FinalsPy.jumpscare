import pickle, os  #For data persistence
from datetime import datetime  #For date handling
from kivy.app import App  #Main Kivy app class
from kivy.core.window import Window  #Window configuration
from kivy.uix.screenmanager import ScreenManager, Screen  #Screen management
from kivy.uix.boxlayout import BoxLayout  #Vertical/horizontal layouts
from kivy.uix.gridlayout import GridLayout  #Grid layouts
from kivy.uix.scrollview import ScrollView  #Scrollable views
from kivy.uix.label import Label  #Text display
from kivy.uix.button import Button  #Interactive buttons
from kivy.uix.textinput import TextInput  #Text input fields
from kivy.uix.popup import Popup  #Popup dialogs
from kivy.uix.image import Image  #Image widgets for icons
from kivy.uix.spinner import Spinner  #For dropdown categories
from kivy.uix.widget import Widget  #For custom widgets
from kivy.graphics import Color, RoundedRectangle, Rectangle  #Graphics for styling
from kivy.uix.dropdown import DropDown
from kivy.uix.anchorlayout import AnchorLayout

#------------------ MOBILE SIZE & BACKGROUND ------------------
Window.size = (360, 640)
Window.clearcolor = (0.95, 0.95, 0.95, 1)

USERS_FILE = "users.dat"

# Bottom navigation bar height
NAV_HEIGHT = 70
APP_ICON = "icons/Logo.png"

# Set custom window icon if file exists
if os.path.exists(APP_ICON):
    try:
        Window.set_icon(APP_ICON)
    except Exception:
        pass

#------------------- FILE FUNCTIONS -------------------
#Load user data from file
def load_users():  
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "rb") as f:
            return pickle.load(f)
    return {}

#Save user data to file
def save_users(users):  
    with open(USERS_FILE, "wb") as f:
        pickle.dump(users, f)

#Get expense file path for user
def get_expense_file(email):  
    return f"expenses_{email}.dat"

#Get budget file path for user
def get_budget_file(email):  
    return f"budget_{email}.dat"

#Load expenses for user
def load_expenses(email): 
    file = get_expense_file(email)
    if os.path.exists(file):
        with open(file, "rb") as f:
            return pickle.load(f)
    return []

#Save expenses for user
def save_expenses(email, data):  
    file = get_expense_file(email)
    with open(file, "wb") as f:
        pickle.dump(data, f)

#Load budget for user
def load_budget(email):  
    file = get_budget_file(email)
    if os.path.exists(file):
        with open(file, "rb") as f:
            return pickle.load(f)
    return 0.0

#Save budget for user
def save_budget(email, amount):  
    file = get_budget_file(email)
    with open(file, "wb") as f:
        pickle.dump(amount, f)

#------------------- LOGIN SCREEN -------------------
class LoginScreen(Screen):
    def __init__(self, sm, nav_bar, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm  
        self.nav_bar = nav_bar
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(Image(source="icons/TBudge.png", size_hint_y=None, height=230, fit_mode='contain'))
        layout.add_widget(Label(text="Budge a goal today in Budgeting with TBudge", size_hint_y=None, height=40, color=(0,0,0,1)))
        layout.add_widget(Label(text="Login Now!", size_hint_y=None, height=40, color=(0.15,0.4,0.9,1), bold=True))

        self.email_input = TextInput(hint_text="Email", size_hint_y=None, height=40, foreground_color=(0,0,0,1))
        self.pwd_input = TextInput(hint_text="Password", password=True, size_hint_y=None, height=40, foreground_color=(0,0,0,1))

        login_btn = Button(text="Login", size_hint_y=None, height=45, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        login_btn.bind(on_press=self.login)

        register_btn = Button(text="Register", size_hint_y=None, height=45, background_color=(1,0,0,1), color=(1,1,1,1))
        register_btn.bind(on_press=self.register)

        layout.add_widget(self.email_input)
        layout.add_widget(self.pwd_input)
        layout.add_widget(login_btn)
        layout.add_widget(register_btn)
        self.add_widget(layout)

    #Hide nav bar on auth screen
    def on_pre_enter(self):
        self.nav_bar.height = 0
        self.nav_bar.opacity = 0
        self.nav_bar.disabled = True
        
    #Handle login attempt
    def login(self, instance):  
        email = self.email_input.text.strip()
        pwd = self.pwd_input.text.strip()
        users = load_users()
        if email in users and users[email] == pwd:
            self.sm.current_user = email
            self.sm.transition.direction = "left"
            self.sm.current = "home"
            self.email_input.text = ""
            self.pwd_input.text = ""
            #Show nav bar
            self.nav_bar.height = NAV_HEIGHT
            self.nav_bar.opacity = 1
            self.nav_bar.disabled = False
        else:
            Popup(title="Error", content=Label(text="Invalid credentials", color=(0,0,0,1)), size_hint=(0.6,0.3)).open()
    
    #Switch to register screen
    def register(self, instance):  
        self.sm.transition.direction = "left"
        self.sm.current = "register"

#------------------- REGISTER SCREEN -------------------
class RegisterScreen(Screen):
    def __init__(self, sm, nav_bar, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        self.nav_bar = nav_bar
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(Image(source="icons/TBudge.png", size_hint_y=None, height=230, fit_mode='contain'))
        layout.add_widget(Label(text="Budge a goal today in Budgeting with TBudge", size_hint_y=None, height=40, color=(0,0,0,1)))
        layout.add_widget(Label(text="Register Now", size_hint_y=None, height=40, color=(0.15,0.4,0.9,1), bold=True))

        self.email_input = TextInput(hint_text="Email", size_hint_y=None, height=40, foreground_color=(0,0,0,1))
        self.pwd_input = TextInput(hint_text="Password", password=True, size_hint_y=None, height=40, foreground_color=(0,0,0,1))

        register_btn = Button(text="Register", size_hint_y=None, height=45, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        register_btn.bind(on_press=self.register)

        back_btn = Button(text="Back to Login", size_hint_y=None, height=45, background_color=(1,0,0,1), color=(1,1,1,1))
        back_btn.bind(on_press=lambda x: self.sm.switch_to_login())

        layout.add_widget(self.email_input)
        layout.add_widget(self.pwd_input)
        layout.add_widget(register_btn)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    #Hide nav bar on auth screen
    def on_pre_enter(self):
        self.nav_bar.height = 0
        self.nav_bar.opacity = 0
        self.nav_bar.disabled = True

    #Handle registration
    def register(self, instance):
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

#------------------- HOME SCREEN -------------------
class HomeScreen(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm 
        self.expenses = []
        self.budget = 0.0 

        main = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=[10, 10, 10, NAV_HEIGHT]
        )
        #Wallet Card - displays budget info with Logo
        self.wallet_card = BoxLayout(orientation='horizontal', size_hint_y=None, height=120, padding=10, spacing=10)
        with self.wallet_card.canvas.before:
            Color(0.15,0.4,0.9,1)
            self.rect = RoundedRectangle(pos=self.wallet_card.pos, size=self.wallet_card.size, radius=[12])
        self.wallet_card.bind(pos=self.update_rect, size=self.update_rect)

        self.wallet_logo = Image(
            source='icons/Logo.png',
            size_hint=(None, None),
            size=(90, 90),
            fit_mode='contain'
        )
        self.wallet_logo_wrap = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.35)
        self.wallet_logo_wrap.add_widget(self.wallet_logo)
        self.wallet_text = Label(text='', markup=True, color=(1,1,1,1), valign='middle', halign='left')
        self.wallet_text.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        self.wallet_card.add_widget(self.wallet_logo_wrap)
        self.wallet_card.add_widget(self.wallet_text)
        main.add_widget(self.wallet_card)

        #Add Expense Button
        add_btn = Button(text="      Add Expense", size_hint_y=None, height=45, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        add_icon = Image(
            source='icons/Add.png',
            size_hint=(None, None),
            size=(22, 22),
            fit_mode='contain'
        )
        add_btn.bind(
            pos=lambda i, v, ic=add_icon: setattr(ic, 'center', (i.x + 28, i.center_y)),
            size=lambda i, v, ic=add_icon: setattr(ic, 'center', (i.x + 28, i.center_y))
        )
        add_btn.add_widget(add_icon)
        add_btn.bind(on_press=self.add_expense_popup)
        main.add_widget(add_btn)

        #Quick action to clear all expenses
        clear_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=30)
        clear_row.add_widget(Widget())
        clear_btn = Button(
            text="Clear Expenses",
            size_hint=(None, 1),
            width=130,
            background_color=(1,0,0,1),
            color=(1,1,1,1)
        )
        clear_btn.bind(on_press=self.clear_all_expenses)
        clear_row.add_widget(clear_btn)
        main.add_widget(clear_row)

        #Scrollable Expenses List
        scroll = ScrollView()
        self.list_layout = GridLayout(cols=1, size_hint_y=None, spacing=5, padding=5)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        scroll.add_widget(self.list_layout)
        main.add_widget(scroll)

        self.add_widget(main)

    #Update rounded rectangle position/size
    def update_rect(self, instance, value):  
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    #Called when screen is entered
    def on_enter(self):  
        self.load_user_data()

    #Load user's expenses and budget
    def load_user_data(self):  
        email = self.sm.current_user
        self.expenses = load_expenses(email)
        self.budget = load_budget(email)
        self.update_home()

    #Refresh home screen display
    def update_home(self):  
        total = sum([e["amount"] for e in self.expenses])
        remaining = self.budget - total
        remaining_color = "[color=00FF00]" if remaining >=0 else "[color=FF0000]"
        self.wallet_text.text = f"[b]Wallet[/b]\nTotal Spent: ₱{total:.2f}\nBudget: ₱{self.budget:.2f}\nRemaining: {remaining_color}₱{remaining:.2f}[/color]"

        #Expenses list with Edit/Delete buttons
        self.list_layout.clear_widgets()
        for idx, e in enumerate(self.expenses):
            box = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
            box.add_widget(Label(text=f"{e['category']}", size_hint_x=0.3, color=(0,0,0,1)))
            box.add_widget(Label(text=f"₱{e['amount']}", size_hint_x=0.3, color=(0,0,0,1)))
            box.add_widget(Label(text=e['date'], size_hint_x=0.2, color=(0,0,0,1)))
            
            #--- EDIT BUTTON---
            edit_btn = Button(
                size_hint=(None, None),
                size=(32, 32),
                background_color=(0, 0, 0, 0), 
                border=(0, 0, 0, 0),
                background_normal='',
                background_down=''
            )

            with edit_btn.canvas.before:
                Color(0.15, 0.4, 0.9, 1)
                edit_bg = RoundedRectangle(
                    pos=edit_btn.pos,
                    size=edit_btn.size,
                    radius=[16]
                )

            edit_btn.bind(
                pos=lambda i, v, bg=edit_bg: setattr(bg, 'pos', i.pos),
                size=lambda i, v, bg=edit_bg: setattr(bg, 'size', i.size)
            )

            edit_icon = Image(
                source='icons/Edit.png',
                size_hint=(None, None),
                size=(18, 18),
                fit_mode='contain'
            )
            edit_btn.bind(
                pos=lambda i, v, icon=edit_icon: setattr(icon, 'center', i.center),
                size=lambda i, v, icon=edit_icon: setattr(icon, 'center', i.center)
            )
            edit_btn.add_widget(edit_icon)

            edit_btn.bind(on_press=lambda x, i=idx: self.edit_expense_popup(i))


            #--- DELETE BUTTON---
            delete_btn = Button(
                size_hint=(None, None),
                size=(32, 32),
                background_color=(0, 0, 0, 0),
                border=(0, 0, 0, 0),
                background_normal='',
                background_down=''
            )

            with delete_btn.canvas.before:
                Color(1, 0, 0, 1)
                delete_bg = RoundedRectangle(
                    pos=delete_btn.pos,
                    size=delete_btn.size,
                    radius=[16]
                )

            delete_btn.bind(
                pos=lambda i, v, bg=delete_bg: setattr(bg, 'pos', i.pos),
                size=lambda i, v, bg=delete_bg: setattr(bg, 'size', i.size)
            )

            delete_icon = Image(
                source='icons/Trash.png',
                size_hint=(None, None),
                size=(18, 18),
                fit_mode='contain'
            )
            delete_btn.bind(
                pos=lambda i, v, icon=delete_icon: setattr(icon, 'center', i.center),
                size=lambda i, v, icon=delete_icon: setattr(icon, 'center', i.center)
            )
            delete_btn.add_widget(delete_icon)

            delete_btn.bind(on_press=lambda x, i=idx: self.delete_expense(i))

            
            box.add_widget(edit_btn)
            box.add_widget(delete_btn)
            self.list_layout.add_widget(box)


    #Show popup to add new expense
    def add_expense_popup(self, instance):  
        layout = BoxLayout(orientation="vertical", spacing=10, padding=[10, 8, 10, 10])

        header_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=34, spacing=8)
        title_label = Label(text="Add Expense", color=(1,1,1,1), halign='left', valign='middle')
        title_label.bind(size=lambda i, v: setattr(i, 'text_size', (i.width, None)))
        header_row.add_widget(title_label)
        close_btn = Button(text="X", size_hint=(None, 1), width=42, background_color=(1,1,1,1), color=(0,0,0,1))
        header_row.add_widget(close_btn)
        layout.add_widget(header_row)

        header_sep = Widget(size_hint_y=None, height=2)
        with header_sep.canvas.before:
            Color(0.2, 0.75, 1, 1)
            sep_rect = Rectangle(pos=header_sep.pos, size=header_sep.size)
        header_sep.bind(
            pos=lambda ins, val, rect=sep_rect: setattr(rect, "pos", ins.pos),
            size=lambda ins, val, rect=sep_rect: setattr(rect, "size", ins.size)
        )
        layout.add_widget(header_sep)
        
        #Dropdown Category
        cat_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
        self.cat_input = TextInput(hint_text="Category", size_hint_x=0.8, foreground_color=(0,0,0,1))
        dropdown_btn = Button(text="", size_hint_x=0.2, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        more_icon = Image(
            source='icons/More.png',
            size_hint=(None, None),
            size=(18, 18),
            fit_mode='contain'
        )
        dropdown_btn.bind(
            pos=lambda i, v, ic=more_icon: setattr(ic, 'center', i.center),
            size=lambda i, v, ic=more_icon: setattr(ic, 'center', i.center)
        )
        dropdown_btn.add_widget(more_icon)
        dropdown_btn.bind(on_press=self.show_category_dropdown)
        cat_layout.add_widget(self.cat_input)
        cat_layout.add_widget(dropdown_btn)
        layout.add_widget(cat_layout)
        amt_input = TextInput(hint_text="Amount", size_hint_y=None, height=40, foreground_color=(0,0,0,1))
        add_btn = Button(text="Add", size_hint_y=None, height=40, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        btn_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
        btn_layout.add_widget(add_btn)
        layout.add_widget(amt_input)
        layout.add_widget(btn_layout)
        popup = Popup(title="", separator_height=0, content=layout, size_hint=(0.9, None), height=250)
        add_btn.bind(on_press=lambda x: self.save_expense(self.cat_input.text, amt_input.text, popup))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    #Open category selector for add form
    def show_category_dropdown(self, instance):
        self.open_category_overlay(self.cat_input)

    #Show category list in popup overlay
    def open_category_overlay(self, target_input):
        categories = sorted(set(e['category'] for e in self.expenses if e.get('category')))
        if not categories:
            Popup(title="Info", content=Label(text="No saved categories yet.", color=(0,0,0,1)), size_hint=(0.7,0.3)).open()
            return

        content = BoxLayout(orientation="vertical", spacing=8, padding=10)
        scroll = ScrollView()
        list_layout = GridLayout(cols=1, spacing=6, size_hint_y=None)
        list_layout.bind(minimum_height=list_layout.setter('height'))
        scroll.add_widget(list_layout)

        close_btn = Button(text="Close", size_hint_y=None, height=40, background_color=(0.7,0.7,0.7,1), color=(0,0,0,1))
        content.add_widget(scroll)
        content.add_widget(close_btn)

        picker_popup = Popup(title="Select Category", content=content, size_hint=(0.9, 0.55))

        for cat in categories:
            cat_btn = Button(
                text=cat,
                size_hint_y=None,
                height=42,
                background_color=(0.15,0.4,0.9,1),
                color=(1,0.85,0,1),
                halign='left',
                valign='middle'
            )
            cat_btn.bind(size=lambda b, v: setattr(b, 'text_size', (b.width - 20, None)))
            cat_btn.bind(on_press=lambda btn, c=cat: self.select_category(target_input, c, picker_popup))
            list_layout.add_widget(cat_btn)

        close_btn.bind(on_press=picker_popup.dismiss)
        picker_popup.open()

    #Apply selected category to input
    def select_category(self, target_input, category, popup):
        target_input.text = category
        popup.dismiss()

    #Save new expense
    def save_expense(self, category, amount, popup):  
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
            Popup(title="Error", content=Label(text="Invalid input", color=(1,1,1,1)), size_hint=(0.6,0.3)).open()

    #Delete all expenses and update storage
    def clear_all_expenses(self, instance):
        self.expenses = []
        save_expenses(self.sm.current_user, self.expenses)
        self.update_home()

    #Show popup to edit expense
    def edit_expense_popup(self, idx):  
        e = self.expenses[idx]
        layout = BoxLayout(orientation="vertical", spacing=10, padding=[10, 8, 10, 10])

        header_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=34, spacing=8)
        title_label = Label(text="Edit Expense", color=(1,1,1,1), halign='left', valign='middle')
        title_label.bind(size=lambda i, v: setattr(i, 'text_size', (i.width, None)))
        header_row.add_widget(title_label)
        close_btn = Button(text="X", size_hint=(None, 1), width=42, background_color=(1,1,1,1), color=(0,0,0,1))
        header_row.add_widget(close_btn)
        layout.add_widget(header_row)

        header_sep = Widget(size_hint_y=None, height=2)
        with header_sep.canvas.before:
            Color(0.2, 0.75, 1, 1)
            sep_rect = Rectangle(pos=header_sep.pos, size=header_sep.size)
        header_sep.bind(
            pos=lambda ins, val, rect=sep_rect: setattr(rect, "pos", ins.pos),
            size=lambda ins, val, rect=sep_rect: setattr(rect, "size", ins.size)
        )
        layout.add_widget(header_sep)
        
        #Dropdown Category
        cat_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
        self.edit_cat_input = TextInput(text=e['category'], size_hint_x=0.8, foreground_color=(0,0,0,1))
        dropdown_btn = Button(text="", size_hint_x=0.2, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        more_icon = Image(
            source='icons/More.png',
            size_hint=(None, None),
            size=(18, 18),
            fit_mode='contain'
        )
        dropdown_btn.bind(
            pos=lambda i, v, ic=more_icon: setattr(ic, 'center', i.center),
            size=lambda i, v, ic=more_icon: setattr(ic, 'center', i.center)
        )
        dropdown_btn.add_widget(more_icon)
        dropdown_btn.bind(on_press=self.show_edit_category_dropdown)
        cat_layout.add_widget(self.edit_cat_input)
        cat_layout.add_widget(dropdown_btn)
        layout.add_widget(cat_layout)
        amt_input = TextInput(text=str(e['amount']), size_hint_y=None, height=40, foreground_color=(0,0,0,1))
        save_btn = Button(text="Save", size_hint_y=None, height=40, background_color=(0.15,0.4,0.9,1), color=(1,0.85,0,1))
        btn_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
        btn_layout.add_widget(save_btn)
        layout.add_widget(amt_input)
        layout.add_widget(btn_layout)
        popup = Popup(title="", separator_height=0, content=layout, size_hint=(0.9, None), height=250)
        save_btn.bind(on_press=lambda x: self.save_edit(idx, self.edit_cat_input.text, amt_input.text, popup))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    #Open category selector for edit form
    def show_edit_category_dropdown(self, instance):
        self.open_category_overlay(self.edit_cat_input)

    #Save edited expense
    def save_edit(self, idx, category, amount, popup):  
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
            Popup(title="Error", content=Label(text="Invalid input", color=(1,1,1,1)), size_hint=(0.6,0.3)).open()

    #Delete expense
    def delete_expense(self, idx):  
        self.expenses.pop(idx)
        save_expenses(self.sm.current_user, self.expenses)
        self.update_home()

#------------------- BUDGET SCREEN -------------------
class BudgetScreen(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm
        
        layout = BoxLayout(
            orientation="vertical",
            padding=[20, 20, 20, NAV_HEIGHT],
            spacing=10
        )

        layout.add_widget(Image(source="icons/SetBudget.png", size_hint_y=None, height=120, fit_mode='contain'))
        layout.add_widget(Label(text="Set Today's Budget", size_hint_y=None, height=50, color=(0.15,0.4,0.9,1)))

        self.budget_input = TextInput(
            hint_text="Enter Budget(₱0.0)",
            size_hint_y=None,
            height=40,
            foreground_color=(0,0,0,1)
        )
        layout.add_widget(self.budget_input)

        save_btn = Button(
            text="Save Budget",
            size_hint_y=None,
            height=45,
            background_color=(0.15,0.4,0.9,1),
            color=(1,0.85,0,1)
        )
        save_btn.bind(on_press=self.save_budget)
        layout.add_widget(save_btn)

        reset_btn = Button(
            text="Reset Monthly Budget",
            size_hint_y=None,
            height=45,
            background_color=(1,0,0,1),
            color=(1,1,1,1)
        )
        reset_btn.bind(on_press=self.reset_budget)
        layout.add_widget(reset_btn)

        self.add_widget(layout)

    #Reset input every time screen opens
    def on_enter(self): 
        self.budget_input.text = ""
        self.budget_input.hint_text = "Enter Budget(₱0.0)"

    #Save budget to user file
    def save_budget(self, instance):  
        try:
            amount = float(self.budget_input.text)
            save_budget(self.sm.current_user, amount)
            self.budget_input.text = ""
            Popup(title="Success", content=Label(text="Budget saved", color=(0,0,0,1)), size_hint=(0.6,0.3)).open()
        except:
            Popup(title="Error", content=Label(text="Invalid input", color=(1,1,1,1)), size_hint=(0.6,0.3)).open()

    #Set budget back to zero
    def reset_budget(self, instance):
        save_budget(self.sm.current_user, 0.0)
        self.budget_input.text = ""
        Popup(title="Success", content=Label(text="Budget reset to ₱0.0", color=(0,0,0,1)), size_hint=(0.6,0.3)).open()

#------------------- PROFILE SCREEN -------------------
class ProfileScreen(Screen):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.sm = sm  

        #FIX: added bottom padding (70)
        layout = BoxLayout(
            orientation="vertical",
            padding=[20, 20, 20, NAV_HEIGHT],
            spacing=10
        )

        layout.add_widget(Image(source="icons/UserProfile.png", size_hint_y=None, height=120, fit_mode='contain'))
        layout.add_widget(Label(text="Profile", size_hint_y=None, height=50, color=(0.15,0.4,0.9,1)))

        self.info_label = Label(text="", size_hint_y=None, height=60, color=(0,0,0,1))
        layout.add_widget(self.info_label)

        logout_btn = Button(
            text="Logout",
            size_hint_y=None,
            height=45,
            background_color=(0.15,0.4,0.9,1),
            color=(1,0.85,0,1)
        )
        logout_btn.bind(on_press=self.logout) 
        layout.add_widget(logout_btn)

        delete_btn = Button(
            text="Delete Account",
            size_hint_y=None,
            height=45,
            background_color=(1,0,0,1),
            color=(1,1,1,1)
        )
        delete_btn.bind(on_press=self.confirm_delete_account)
        layout.add_widget(delete_btn)

        self.add_widget(layout)

    #Show current user info
    def on_enter(self):  
        self.info_label.text = f"User: {self.sm.current_user}"

    #Logout and return to login
    def logout(self, instance):  
        self.sm.current_user = None
        self.sm.current = "login"
        self.sm.nav_bar.height = 0
        self.sm.nav_bar.opacity = 0
        self.sm.nav_bar.disabled = True

    #Ask confirmation before deleting account
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

    #Delete account and user files
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

#------------------- SCREEN MANAGER -------------------
class TBudgeSM(ScreenManager):
    def __init__(self, nav_bar, **kwargs):
        super().__init__(**kwargs)
        #Store shared app state
        self.current_user = None 
        self.nav_bar = nav_bar 
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

    #Switch to login screen and hide nav bar
    def switch_to_login(self):  
        self.transition.direction = "right"
        self.current = "login"
        self.nav_bar.height = 0
        self.nav_bar.opacity = 0
        self.nav_bar.disabled = True

#------------------- APP -------------------
class TBudgeApp(App):
    icon = APP_ICON

    #Build root UI and navigation
    def build(self):
        root = BoxLayout(orientation="vertical")

        # ---------------- BOTTOM NAV BAR ----------------
        self.nav_bar = BoxLayout(
            size_hint_y=None,
            height=0,
            spacing=0,
            padding=[10, 8, 10, 8],
            opacity=0,
            disabled=True
        )

        #Rounded background
        with self.nav_bar.canvas.before:
            Color(0.15, 0.4, 0.9, 1)
            self.nav_bg = RoundedRectangle(
                pos=self.nav_bar.pos,
                size=self.nav_bar.size,
                radius=[20, 20, 0, 0]
            )

        self.nav_bar.bind(
            pos=lambda i, v: setattr(self.nav_bg, "pos", i.pos),
            size=lambda i, v: setattr(self.nav_bg, "size", i.size)
        )

        # ---------------- NAV CONTAINER ----------------
        nav_container = BoxLayout(
            orientation="horizontal",
            size_hint=(1, 1),
            spacing=0,
            padding=[0, 0, 0, 0]
        )

        btn_specs = [
            ("home", "icons/Home.png"),
            ("budget", "icons/Budget.png"),
            ("profile", "icons/Profile.png")
        ]

        for name, icon_path in btn_specs:
            wrapper = AnchorLayout(anchor_x="center", anchor_y="center", size_hint=(1, 1))

            btn = Button(
                size_hint=(None, None),
                size=(50, 50),
                background_color=(0, 0, 0, 0),
                border=(0, 0, 0, 0),
                background_normal="",
                background_down=""
            )

            # Circle background
            with btn.canvas.before:
                Color(0.15, 0.4, 0.9, 1)
                bg_circle = RoundedRectangle(
                    pos=btn.pos,
                    size=btn.size,
                    radius=[25]
                )

            btn.bind(
                pos=lambda i, v, bg=bg_circle: setattr(bg, "pos", i.pos),
                size=lambda i, v, bg=bg_circle: setattr(bg, "size", i.size)
            )

            # Icon
            icon = Image(
                source=icon_path,
                size_hint=(None, None),
                size=(26, 26),
                center=btn.center
            )

            btn.bind(
                pos=lambda i, v, ic=icon: setattr(ic, "center", i.center),
                size=lambda i, v, ic=icon: setattr(ic, "center", i.center)
            )

            btn.add_widget(icon)

            btn.bind(on_press=lambda x, n=name: self.nav_press(n))

            wrapper.add_widget(btn)
            nav_container.add_widget(wrapper)

        self.nav_bar.add_widget(nav_container)

        # ---------------- SCREEN MANAGER ----------------
        self.sm = TBudgeSM(self.nav_bar)

        root.add_widget(self.sm)
        root.add_widget(self.nav_bar)

        return root

    #Handle bottom-nav page switching
    def nav_press(self, name):
        nav_order = ["home", "budget", "profile"]
        current = self.sm.current

        if name == current:
            return

        if current in nav_order and name in nav_order:
            current_idx = nav_order.index(current)
            target_idx = nav_order.index(name)
            self.sm.transition.direction = "left" if target_idx > current_idx else "right"

        self.sm.current = name

if __name__ == "__main__":
    #Run the app
    TBudgeApp().run()  