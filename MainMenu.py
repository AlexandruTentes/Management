class Menu:
    is_admin = False
    option = 0
    page = 0
    page_name = ""
    back_page = []
    running = True
    page_layout = []
    pages = []
    page_logic = {}
    page_shift = [0]

    def __init__(self):
        pass

    def set_menu(self, page_logic, page_layout):
        pages = []
        
        for key, item in page_logic.items():
            pages.append(key)
        
        self.pages = pages
        self.page_logic = page_logic
        self.page_layout = page_layout

    def menu_update(self, custom_page_logic):
        if self.page_name != "":
            for i, item in enumerate(self.pages):
                if item == self.page_name:
                    self.page = i
                    break
                
        self.page_name = ""

        data = self.page_logic[self.pages[self.page]]
        self.page_menu(self.page, *tuple(data))

        if self.option != 0:
            obj_func = custom_page_logic[self.pages[self.page]]
            if self.option <= len(obj_func):
                data = obj_func[self.option]
                func = data[0]
                args = data[1:]
                func(*tuple(args))           

    def get_option(self, main_menu_op, update_page = True, is_back = True):
        while self.option == 0 or self.option >= len(main_menu_op):
            print(self.pages[self.option] + " options:")

            self.page_shift = [0]

            i = 1
            shift = -1
            for op in main_menu_op:
                if shift == -1:
                    shift = 0
                    continue

                if op == "NONE":
                    shift = shift + 1
                
                self.page_shift.append(shift)
                
                if op == "NONE":
                    continue

                print(str(i) + ") " + op)
                i = i + 1

            try:
                self.option = abs(int(input("Type option: ")))
                self.option = self.option + self.page_shift[self.option]

                while main_menu_op[self.option] == "NONE" and \
                    self.option <= len(main_menu_op):
                    self.option = self.option + 1

                if self.option >= len(main_menu_op):
                    raise Exception("")

                if update_page:
                    self.back_page.append(self.page)
                    self.page = self.option
            except:
                print("please type a valid integer option...")
                self.option = 0

            if self.option == len(main_menu_op) - 1:
                self.running = False
                self.option = 0
                break
            elif self.option == len(main_menu_op) - 2 and is_back:
                self.page = self.back_page[len(self.back_page) - 1]
                self.back_page = self.back_page[:-1]
                self.option = 0
                break

        if update_page:
            self.option = 0

    def page_menu(self, page, update_page, is_back):
        self.option = 0
        main_menu_op = self.page_layout[page]
        
        self.get_option(main_menu_op, update_page, is_back)
