class UserInterface:
    def __init__(self, root, connection, login, db_app):
        self.connection = connection
        self.root = root
        self.cursor = self.connection.cursor()
        self.db_app = db_app
        self.user_login = login

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_window()
