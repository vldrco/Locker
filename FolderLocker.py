import os
import hashlib
import tkinter
from tkinter import messagebox
import subprocess

class FolderLocker:
    def __init__(self, master):
        self.master = master
        master.title("Folder Locker")
        '''
        Check if the folder "Locker" exists
        Verificar a existência da pasta "Locker"
        '''   
        folder_path = os.path.join(os.getcwd(), "Locker")
        folder_path2 = os.path.join(os.getcwd(), "Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}")
        if os.path.isdir(folder_path) or os.path.isdir(folder_path2):
            '''
            If the folder exists, go to main window
            Se a pasta existir, ir a janela principal
            '''
            self.main_window()
        else:
            '''
            If not, opens create password window
            Se não existir, vai para janela de criação
            '''
            self.create_password_window()
            
        self.stored_password = '#.hash'
        
    def main_window(self):
        '''
        Check if the folder is locked or not, widgets are here
        Verificar se a pasta está bloqueada ou não
        '''
        path1 = os.path.join(os.getcwd(), "Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}")

        if os.path.isdir(path1):
            self.unlock_entry_password = tkinter.Entry(self.master, show="*")
            self.unlock_entry_password.pack()
            unlock_button = tkinter.Button(self.master, text="Unlock Folder", command=self.unlock_folder)
            unlock_button.pack()

            change_password_button = tkinter.Button(self.master, text="Change Password", command=self.change_password_window)
            change_password_button.pack()   
        else:
            self.lock_entry_password = tkinter.Entry(self.master, show="*")
            self.lock_entry_password.pack()
            lock_button = tkinter.Button(self.master, text="Lock Folder", command=self.lock_folder)
            lock_button.pack()

            change_password_button = tkinter.Button(self.master, text="Change Password", command=self.change_password_window)
            change_password_button.pack()
    
    def change_password_window(self):
        '''
        Child window, widgets are here.
        Janela filha para mudar a pass
        '''
        self.change_window = tkinter.Toplevel()
        self.change_window.title("Change password")
        
        self.change_window.transient(self.master)
        
        current_password = tkinter.Label(self.change_window, text="Enter the current password:")
        current_password.pack()
        
        self.current_password_entry = tkinter.Entry(self.change_window, show="*")
        self.current_password_entry.pack()
        
        change_label = tkinter.Label(self.change_window, text="Enter a new password:")
        change_label.pack()
        
        self.change_entry = tkinter.Entry(self.change_window, show="*")
        self.change_entry.pack()
        
        self.change_button = tkinter.Button(self.change_window, text="Change", command=self.change_password)
        self.change_button.pack()
        
    def create_password_window(self):
        '''
        Child window to define a password and create the "Locker" folder widgets are here.
        Janela filha para definir a password e criar a pasta "Locker".
        '''
        self.password_window = tkinter.Toplevel()
        self.password_window.title("Set Password")

        password_label = tkinter.Label(self.password_window, text="Enter a password to lock the folder:")
        password_label.pack()

        self.password_entry = tkinter.Entry(self.password_window, show="*")
        self.password_entry.pack()

        set_password_button = tkinter.Button(self.password_window, text="Set", command=self.set_password)
        set_password_button.pack()
        
    def set_password(self):
        '''
        function to set the password, create the "Locker" folder and store the password 
        -in a hash file.
        Função para criar a password, a pasta "Locker" e guardar a password encryptada- 
        -num ficheiro hash.
        Receber a password introduzida no widget de inserção "password_entry"
        '''
        password = self.password_entry.get()
        
        if password == "":
            messagebox.showerror("Error", "Password cannot be empty.")
            return
        
        '''
        Encrypt the password using the SHA-256 algorithm
        Encriptar a password usando o algoritmo SHA-256 do hashlib
        '''
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        '''
        Store the encrypted password inside the hash file
        Guardar a password encriptada dentro do ficheiro hash
        (w[write], r[read])
        '''
        with open(self.stored_password, 'w') as fl:
            fl.write(password_hash)
            
        cmd = f"attrib +h +s {self.stored_password}"
        subprocess.run(cmd)
    
        messagebox.showinfo("Success", "Password set successfully.")
        self.password_entry.delete(0, tkinter.END)
        '''
        Create the folder
        Criar a pasta
        '''
        folder_path = os.path.join(os.getcwd(), "Locker")
        os.makedirs(folder_path, exist_ok=True)
        '''
        Destroy the set password window
        Destroir a Janela de criação
        '''
        self.password_window.destroy()
        '''
        Go to main window
        Ir para janela principal
        '''
        self.main_window()
        
    def lock_folder(self):
        '''
        Function to lock the folder.
        Função para bloquear a pasta.
        Recebe a password inserida no widget de inserção "lock_entry_password"
        '''
        password = self.lock_entry_password.get()
        
        '''
        Encrypts the received password then compares it to the stored one in the hash file
        Encripta a password inserida e de seguida compara com a que está no hash file
        '''
        entered_password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        with open(self.stored_password, 'r') as fl:
            p_hash = fl.read().strip()

        if entered_password_hash != p_hash:
            messagebox.showerror("Error", "Invalid password.")
            return

        os.rename("Locker", "Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}")
        cmd = 'attrib +h +s "Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}"'
        subprocess.run(cmd)

        messagebox.showinfo("Success", "Folder locked successfully.")
        self.lock_entry_password.delete(0, tkinter.END)
        self.master.destroy()
        
    def unlock_folder(self):
        '''
        Function to unlock the folder.
        Função para desbloquear a pasta.
        Recebe a password inserida no widget de inserção "unlock_entry_password"
        '''
        password = self.unlock_entry_password.get()
        '''
        Encrypts the received password then compares it to the stored one in the hash file
        Encripta a password inserida e de seguida compara com a que está no hash file
        '''
        entered_password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        with open(self.stored_password, 'r') as fl:
            p_hash = fl.read().strip()

        if entered_password_hash != p_hash:
            messagebox.showerror("Error", "Invalid password.")
            return

        os.rename("Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}", "Locker")
        cmd = 'attrib -h -s "Locker"'
        subprocess.run(cmd)

        messagebox.showinfo("Success", "Folder unlocked successfully.")
        self.unlock_entry_password.delete(0, tkinter.END)
        self.master.destroy()
        
    def change_password(self):
        '''
        Function to change the password inside the hash file
        Função para mudar a password que está no ficheiro .hash
        Recebe a password inserida pelo usuário no "current_password_entry" widget,
        usando o método get()
        '''
        password = self.current_password_entry.get()
        
        '''
        Encrypts the received password then compares it to the stored one in the hash file
        Encripta a password inserida e de seguida compara com a que está no hash file
        Se a password estiver correcta então a troca de password será realizada.
        '''
        entered_password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        with open(self.stored_password, 'r') as fl:
            p_hash = fl.read().strip()

        if entered_password_hash != p_hash:
            messagebox.showerror("Error", "Invalid password.")
            return
        
        new_password = self.change_entry.get()

        if new_password == "":
            messagebox.showerror("Error", "New password cannot be empty.")
            return
        
        new_hash = hashlib.sha256(new_password.encode()).hexdigest()
        
        fpath = "./#.hash"
        os.remove(fpath)
        self.stored_password = '#.hash'
        
        with open(self.stored_password, 'w') as fl:
            fl.write(new_hash)

        messagebox.showinfo("Success", "Password changed successfully.")
        self.change_entry.delete(0, tkinter.END)
        self.change_window.destroy()
        
root = tkinter.Tk()
app = FolderLocker(root)
root.mainloop()