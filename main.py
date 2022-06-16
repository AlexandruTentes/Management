import MainMenu


class Management:
    classes = {}
    sections = {}
    users = {}
    logged_user = None
    sectNum = 0
    user_id = 1

    def __init__(self):
        self.sectNum = int(input("Enter section size: "))

    def addClass(self):
        className = input("Enter the name of the class: ")
    
        if className in self.classes:
            print("Class " + className + " already exists...")
            return

        self.classes[className] = {
            "sections": None,
            "letter": 65
            }

        self.classes[className]["sections"] = {
                chr(self.classes[className]["letter"]): []
            }

        print(self.classes)

    def addStudentClass(self):
        email = input("Type email: ")
        # Generate section number based on max section size
        className = input("Type class: ")

        if email not in self.users:
            print("User email " + email + " does not exist")
            return

        if className not in self.classes:
            print("Class " + className + " does not exist")
            return 

        data = self.classes[className]

        for key, sec in data["sections"].items():
            for user in sec:
                if isinstance(user, User) and user.email == email:
                    print("User " + email + " already present in section " + key + " in class " + className)
                    return

        the_list = data["sections"][chr(data["letter"])]
        if len(the_list) != 0 and len(the_list) >= self.sectNum + int(not isinstance(the_list[0], User)):
            data["sections"][chr(data["letter"] + 1)] = []
            data["letter"] = data["letter"] + 1
            
        data["sections"][chr(data["letter"])].append(self.users[email])
        print(data)

    def addStaffSection(self):
        staffName = input("Enter staff name to add to section: ")
        # Generate section number based on max section size
        className = input("Type class: ")
        section = input("Type section: ")

        if className not in self.classes:
            print("Class " + className + " does not exist")
            return 

        data = self.classes[className]

        if section not in data["sections"]:
            print("Section does not exist")
            return

        the_list = data["sections"][section[0]]
        the_list.append(staffName)
        tmp = the_list[0]
        the_list[0] = the_list[len(the_list) - 1]
        the_list[len(the_list) - 1] = tmp
        print(data)

    def populate_attendance(self):
        if self.logged_user == None or self.logged_user.is_admin == False:
            print("Not logged in...")
            return

        email = input("User email to add attendance to: ")

        if email not in self.users:
            print("User with email " + email + " does not exist...")
            return

        year_dict = {}
        month_dict = {}
        week_dict = {}

        years = input("Add years: ")

        years = years.split(' ')
        for year in years:
            months = input("Add months for year " + year + ": ")

            months = months.split(' ')
            for month in months:
                weeks = input("Add weeks for month " + month + ": ")

                weeks = weeks.split(' ')
                for week in weeks:
                    days = input("Add days for week " + week + ": ")

                    week_dict[week] = days

                month_dict[month] = week_dict
                week_dict = {}

            year_dict[year] = month_dict
            month_dict = {}

        self.users[email].attendance = year_dict

    def login(self, menu_obj):
        if self.logged_user != None:
            menu_obj.page_name = "Admin Menu" if \
                self.logged_user.is_admin == True else "User Menu"
            return True
        
        email = input("Type email: ")
        password = input("Type password: ")
        
        if email in self.users:
            print("Login successful")
            self.logged_user = self.users[email]
            menu_obj.page_name = "Admin Menu" if \
                self.logged_user.is_admin == True else "User Menu"
            return True

        print("Data provided is wrong...")
        return False

    def register(self, menu_obj, is_admin):
        if self.logged_user != None:
            menu_obj.page_name = "Admin Menu" if \
                self.logged_user.is_admin == True else "User Menu"
            return True
        
        name = input("Type username: ")
        email = input("Type email: ")
        password = input("Type password: ")
        
        if email not in self.users:
            print("New user created! Logging in...")
            u = None

            if is_admin == True:
                u = Admin(self.user_id, name, email, password)
            else:
                u = User(self.user_id, name, email, password)
            
            self.users[email] = u
            self.logged_user = self.users[email]
            self.user_id = self.user_id + 1
            menu_obj.page_name = "Admin Menu" if \
                self.logged_user.is_admin == True else "User Menu"
            return True

        print("Email already in use...")
        return False

    def logout(self, menu_obj):
        if self.logged_user != None:
            print("Logging out...")
            self.logged_user = None
            menu_obj.page_name = "Main Menu"
            return True

        print("Please log in first...")
        return False

    def show_attendance(self, cat):
        if self.logged_user == None:
            print("Must log in first...")
            return
        
        if cat == "y":
            self.users[self.logged_user.email].showYearly()
        elif cat == "m":
            self.users[self.logged_user.email].showMonthly()
        elif cat == "w":
            self.users[self.logged_user.email].showWeekly()

class User:
    _id = 0
    name = ""
    password = ""
    email = ""
    attendance = {}
    is_admin = False
    
    def __init__(self):
        pass
    
    def __init__(self, _id, name, email, password):
        self._id = _id
        self.name = name
        self.email = email
        self.password = password

    def showWeekly(self):
        year = input("What year: ")
        month = input("What month: ")
        week = input("What week: ")

        if year not in self.attendance:
            print("User " + self.name + " has no attendance for the year " + year)
            return

        if month not in self.attendance[year]:
            print("User " + self.name + " has no attendance for the month " + month)
            return

        if week not in self.attendance[year][month]:
            print("User " + self.name + " has no attendance for the week " + week)
            return
        
        print("Showing Weekly attendance for: " + self.name)
        print(self.attendance[year][month][week])

    def showMonthly(self):
        year = input("What year: ")
        month = input("What month: ")

        if year not in self.attendance:
            print("User " + self.name + " has no attendance for the year " + year)
            return

        if month not in self.attendance[year]:
            print("User " + self.name + " has no attendance for the month " + month)
            return
        
        print("Showing Monthly attendance for: " + self.name)
        print(self.attendance[year][month])

    def showYearly(self):
        year = input("What year: ")

        if year not in self.attendance:
            print("User " + self.name + " has no attendance for the year " + year)
            return
        
        print("Showing Yearly attendance for: " + self.name)
        print(self.attendance[year])

class Admin(User):
    
    def __init__(self):
        self.is_admin = True

    def __init__(self, _id, name, email, password):
        self.is_admin = True
        super(Admin, self).__init__(_id, name, email, password)


menu = MainMenu.Menu()

page_logic = {
            "Main Menu": [True, False],
            "Admin Login": [False, True],
            "Admin Menu": [False, True],
            "User Login": [False, True],
            "User Menu": [False, True],
        }

layout = [
            [#Main menu
                "Main Menu",
                "Admin",
                "NONE",
                "User",
                "NONE",
                "Exit"
            ],
            [#Admin login
                "Admin Login",
                "Login",
                "Register",
                "Back",
                "Exit"
            ],
            [#Admin menu
                "Admin Menu",
                "Add classes",
                "Add student to class",
                "Add staff to section",
                "Add user attendance",
                "Log out",
                "Back",
                "Exit"
            ],
            [#User login
                "User Login",
                "Login",
                "Register",
                "Back",
                "Exit"
            ],
            [#User menu
                "User Menu",
                "Weekly attendance",
                "Monthly attendance",
                "Yearly attendance",
                "Log out",
                "Back",
                "Exit"
            ],              
        ]



def main():
    menu.set_menu(page_logic, layout)
    manage = Management()

    the_menu = {
        "Admin Menu": {
                1: [manage.addClass],
                2: [manage.addStudentClass],
                3: [manage.addStaffSection],
                4: [manage.populate_attendance],
                5: [manage.logout, menu]
            },
        "Admin Login": {
                1: [manage.login, menu],
                2: [manage.register, menu, True]
            },
        "User Menu": {
                1: [manage.show_attendance, "w"],
                2: [manage.show_attendance, "m"],
                3: [manage.show_attendance, "y"],
                4: [manage.logout, menu],
            },
        "User Login": {
                1: [manage.login, menu],
                2: [manage.register, menu, False]
            },
    }

    while menu.running:
        menu.menu_update(the_menu)


if __name__ == "__main__":
    main()

