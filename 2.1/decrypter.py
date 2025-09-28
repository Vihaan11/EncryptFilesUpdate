import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from cryptography.fernet import Fernet

# dir_list = path_to_file.split('/')
# filename = dir_list.pop(-1).split('.')
# ext = filename[-1]
# self.new_ext = f".{ext}_encrypted"
# self.new_filename = f"{filename[0]}{self.new_ext}"

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

if os.getenv('FERNET_KEY') is None:
    mykey = Fernet.generate_key()
    os.system(f'setx FERNET_KEY "{mykey.decode()}"')
else:
    mykey=os.getenv('FERNET_KEY')

myfernet = Fernet(mykey)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.quitter)
        self.success_var = tk.StringVar()
        self.success_var.set("During saving, you need to set the file extention yourself")
        self.encrypted_data = None
        self.new_filename = None
        self.new_ext = None
        self.path=tk.StringVar()
        self.geometry('600x300+640+350')
        self.title("Decrypter")
        self.resizable(False,False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.mainf = Mainframe(self, padding=15)
        self.mainf.grid(sticky='nsew')
        self.Label = ttk.Label()
    def askfilepath(self, var_name:tk.StringVar):
        path = filedialog.askopenfile(mode='r',
                                      parent=self,
                                      title='File to encrypt',
                                      # initialdir=fr'C:\Users\{self.username}',
                                      filetypes=[('All Files', '*.*')]
                                      )
        if path:
            var_name.set(path.name)
    def decrypter(self, path_to_file: str, engine: Fernet):
        try:
            with open(path_to_file, 'r+b') as f:
                token = f.read()
                self.encrypted_data = engine.decrypt(token)
                enc_file=filedialog.asksaveasfile(mode='wb',parent=self,title='Save As',filetypes=[('All Files', '.*')], initialfile=self.new_filename)
                if enc_file:
                    enc_file.write(self.encrypted_data)
                    enc_file.close()
                    self.success_var.set("Success! Your decrypted file has been saved")
                else:
                    # self.success_var.set("Save cancelled")
                    pass
        except:
            self.success_var.set("Sorry! Your file could not be decrypted")
    def quitter(self):
        confirmation = messagebox.askyesno(title='Quit?', message='Are you sure you want to quit?')
        if confirmation:
            self.destroy()

class Mainframe(ttk.Frame):
    def __init__(self, container: MainWindow, **kwargs):
        super().__init__(container, **kwargs)
        self.columnconfigure(0, weight=1)
        self.welcome_label = ttk.Label(self, text='Welcome to EncryptFiles', font=('Consolas',20), anchor='center', padding=(0,20,0,0))
        self.description_label = ttk.Label(self, text='This update gives GUI support and encryption for all file types', anchor='center', font=('Consolas', 10))
        self.welcome_label.grid(row=0, column=0)
        self.description_label.grid(row=1, column=0)
        self.file_path_frame = ttk.Frame(self, padding=(0,30,0,0))
        self.file_path_frame.grid(row=2, column=0)
        self.path_label = ttk.Label(self.file_path_frame, text='Path:  ', anchor='center')
        self.path_label.grid(row=0, column=0)
        self.path_entry = ttk.Entry(self.file_path_frame, width=45, textvariable=container.path)
        self.path_entry.grid(row=0, column=1)
        self.path_chooser = ttk.Button(self.file_path_frame, text='Browse Files', command=lambda: container.askfilepath(container.path))
        self.path_chooser.grid(row=0, column=2, padx=15)

        self.lower_buttons = ttk.Frame(self)
        self.lower_buttons.grid(row=3, column=0, padx=50, pady=5, sticky='ew')
        self.lower_buttons.columnconfigure(0, weight=3)
        self.lower_buttons.columnconfigure(1, weight=1)
        self.encrypt_button = ttk.Button(self.lower_buttons, text = 'Decrypt File', command=lambda : container.decrypter(container.path.get(), myfernet))
        self.encrypt_button.grid(row=0, column=0, sticky='ew')

        self.quit_button = ttk.Button(self.lower_buttons, text = 'Quit', command=container.quitter)
        self.quit_button.grid(row=0, column=1, sticky='ew')

        self.success_label = self.description_label = ttk.Label(self, textvariable=container.success_var, anchor='center', font=('Consolas', 10))
        self.success_label.grid(row=4, column=0, sticky='ew', padx=20, pady=15)

root = MainWindow()

if __name__ == '__main__':
    root.mainloop()