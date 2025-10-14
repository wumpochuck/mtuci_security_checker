import tkinter as tk
import tkinter.messagebox as messagebox
import subprocess
import os

# ---- Основное окно и переменные --------------- #

root = tk.Tk()
root.config(bg = "white")
root.geometry("610x550+600+300")
root.title("Программа проверки средств информационной безопасности")

result_check_network_connected = tk.StringVar(value="")
result_check_firewall_installed = tk.StringVar(value="")
result_check_firewall_working = tk.StringVar(value="")

result_check_antivirus_installed = tk.StringVar(value="")
result_check_antivirus_working = tk.StringVar(value="")
result_antivirus_testing = tk.StringVar(value="")

result_full = tk.StringVar(value="")

# ---- Проверка межсетевого экрана -------------- #

def check_network_connection():
    try:
        if(subprocess.run("ping -n 1 8.8.8.8").returncode == 0):
            result_check_network_connected.set("Данный компьютер подключен к интернету")
        else:
           result_check_network_connected.set("Данный компьютер не подключен к интернету")
    except subprocess.CalledProcessError:
        result_check_network_connected.set("Данный компьютер не подключен к интернету")
    except Exception as e:
        messagebox.showerror("Error", e)

def is_firewall_installed():
    try:
        if(subprocess.run("powershell -Command Get-Service -Name MpsSvc").returncode == 0):
            result_check_firewall_installed.set("Фаервол установлен!")
        else:
            result_check_firewall_installed.set("Фаервол не установлен!")
    except subprocess.CalledProcessError:
            result_check_firewall_installed.set("Фаервол не установлен!")
    except Exception as e:
        messagebox.showerror("Error", e)

def is_firewall_working():
    try:
        count = str(subprocess.check_output('powershell netsh advfirewall show allprofiles | findstr State')).lower().count("on")
        if count == 3:
            result_check_firewall_working.set("Фаервол работает!")
        elif 1 <= count <= 2 :
            result_check_firewall_working.set("Фаервол работает не полностью!")
        else:
            result_check_firewall_working.set("Фаервол не работает!")
    except subprocess.CalledProcessError:
        result_check_firewall_working.set("Фаервол не работает!")
    except Exception as e:
        messagebox.showerror("Error", e)

def interface1(root):
    frame1 = tk.LabelFrame(root, text="Проверка межсетевого экрана", bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="#f0f0f0")
    frame1.pack(fill='x', pady=5, padx=5)

    btn_check_network = tk.Button(frame1, text="Проверка подключения к интернету", command = check_network_connection)
    btn_check_network.grid(row=0, column=0, sticky='ew', pady=2)

    lbl_check_network = tk.Label(frame1, textvariable=result_check_network_connected, bd=1, relief=tk.SUNKEN, width=50, background='white')
    lbl_check_network.grid(row=0, column=1, padx=10, pady=2, sticky='ew')

    btn_check_firewall_installed = tk.Button(frame1, text="Проверка наличия установленного\nмежсетевого экрана", command = is_firewall_installed)
    btn_check_firewall_installed.grid(row=1, column=0, sticky='ew', pady=2)

    lbl_chek_firewall_installed = tk.Label(frame1, textvariable=result_check_firewall_installed, bd=1, relief=tk.SUNKEN, width=50, background='white')
    lbl_chek_firewall_installed.grid(row=1, column=1, padx=10, pady=2, sticky='ew')

    btn_check_firewall_working = tk.Button(frame1, text="Проверка работоспособности\nмежсетевого экрана", command = is_firewall_working)
    btn_check_firewall_working.grid(row=2, column=0, sticky='ew', pady=2)

    lbl_chek_firewall_working = tk.Label(frame1, textvariable=result_check_firewall_working, bd=1, relief=tk.SUNKEN, width=50, background='white')
    lbl_chek_firewall_working.grid(row=2, column=1, padx=10, pady=2, sticky='ew')

interface1(root)

# ---- Проверка антивирусного ПО ---------------- #

def check_antivirus_installed():
    try:
        if(os.path.exists(r"C:\Program Files\Windows Defender\MpCmdRun.exe")):
            result_check_antivirus_installed.set("Антивирус установлен!")
        else:
            result_check_antivirus_installed.set("Антивирус не установлен!")
    except Exception as e:
        messagebox.showerror("Error", e)
        
def check_antivirus_working():
    try:
        code = str(subprocess.check_output("powershell -Command Get-MpComputerStatus | Select-Object AMServiceEnabled, AntispywareEnabled, AntivirusEnabled, RealTimeProtectionEnabled")
                ).lower().count("true")
        if code == 4:
            result_check_antivirus_working.set("Антивирус работает полностью!")
        elif 1 <= code <= 3:
            result_check_antivirus_working.set("Антивирус работает не полностью!")
        else:
            result_check_antivirus_working.set("Антивирус не работает!")
    except subprocess.CalledProcessError:
        result_check_antivirus_installed.set("Антивирус не работает!")
    except Exception as e:
        messagebox.showerror("Error", e)

def antivirus_testing():

    def check_file():
        if not os.path.exists(target_file):
            result_antivirus_testing.set("Антивирус работает корректно!")
        else:
            result_antivirus_testing.set("Антивирус работает некорректно!")

        if (result_full.get() != ""):
            result_full.set(result_full.get() + result_antivirus_testing.get())
            result_antivirus_testing.set("")

    try:
        target_file = './target_file.txt'

        if os.path.exists(target_file):
            os.remove(target_file)

        file = open(target_file, "w+")
        file.write(r'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*')
        file.close()
        result_antivirus_testing.set("Ожидайте...")

        try:
            file = open(target_file,"r")
            file.close()
        except:
            pass

        root.after(20000, check_file)

    except Exception as e:
        messagebox.showerror("Error", e)

def interface2(root):
    frame2 = tk.LabelFrame(root, text="Проверка антивирусного программного обеспечения", bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="#f0f0f0")
    frame2.pack(fill='x', pady=5, padx=5)

    btn_check_antivirus_installed = tk.Button(frame2, text="Проверка наличия установленного\nантивируса", command = check_antivirus_installed)
    btn_check_antivirus_installed.grid(row=0, column=0, sticky='ew', pady=2)

    lbl_check_antivirus_installed = tk.Label(frame2, textvariable=result_check_antivirus_installed, bd=1, relief=tk.SUNKEN, width=50, background='white')
    lbl_check_antivirus_installed.grid(row=0, column=1, padx=10, pady=2, sticky='ew')

    btn_check_antivirus_working = tk.Button(frame2, text="Проверка работоспособности\nантивирусного ПО", command = check_antivirus_working)
    btn_check_antivirus_working.grid(row=1, column=0, sticky='ew', pady=2)

    lbl_check_antivirus_working = tk.Label(frame2, textvariable=result_check_antivirus_working, bd=1, relief=tk.SUNKEN, width=50, background='white')
    lbl_check_antivirus_working.grid(row=1, column=1, padx=10, pady=2, sticky='ew')

    btn_antivirus_testing = tk.Button(frame2, text="Тестирование антивирусного ПО", command = antivirus_testing)
    btn_antivirus_testing.grid(row=2, column=0, sticky='ew', pady=2)

    lbl_antivirus_testing = tk.Label(frame2, textvariable=result_antivirus_testing, bd=1, relief=tk.SUNKEN, width=50, background='white')
    lbl_antivirus_testing.grid(row=2, column=1, padx=10, pady=2, sticky='ew')

interface2(root)

# ---- Результаты проверок и рекомендации ------- #

def do_report():
    check_network_connection()
    is_firewall_installed()
    is_firewall_working()

    check_antivirus_installed()
    check_antivirus_working()
    antivirus_testing()

    result_full.set(result_check_network_connected.get() + "\n" +
                    result_check_firewall_installed.get()+ "\n" +
                    result_check_firewall_working.get() + "\n" +
                    result_check_antivirus_installed.get()+ "\n" +
                    result_check_antivirus_working.get()+ "\n")
    
    result_check_network_connected.set("")
    result_check_firewall_installed.set("")
    result_check_firewall_working.set("")
    result_check_antivirus_installed.set("")
    result_check_antivirus_working.set("")

def save_report():
    try:
        report_file_path = "./report.txt"
        if(result_full.get() != ""):
            print(result_full.get())
            file = open(report_file_path, "w+", encoding='utf-8')
            file.write(result_full.get())
            file.close()
        else:
            messagebox.showwarning("Ошибка", "Отчёт не создан!")

    except Exception as e:
        messagebox.showerror("Error", e)

def exit_app():
    root.destroy()

def interface3(root):
    frame3 = tk.LabelFrame(root, text="Результаты проверок и рекомендации", bd=2, relief=tk.GROOVE, padx=10, pady=10)
    frame3.pack(fill='x', pady=5, padx=5)

    frame3.grid_columnconfigure(0, weight=1)
    frame3.grid_rowconfigure(0, weight=1)
    frame3.grid_rowconfigure(1, weight=1)
    frame3.grid_rowconfigure(2, weight=1)

    lbl_results = tk.Label(frame3, textvariable=result_full, height=10, width=60, bd=1, relief=tk.SUNKEN, anchor='nw', justify='left', background='white')
    lbl_results.grid(row=0, column=0, rowspan=3, padx=5, pady=5, sticky='nsew')

    btn_do_report = tk.Button(frame3, text="Вывести\nрезультаты", width=15, command = do_report)
    btn_do_report.grid(row=0, column=1, padx=5, pady=2, sticky='ew')

    btn_save_report = tk.Button(frame3, text="Сохранить\nрезультаты\nв файл", width=15, command=save_report)
    btn_save_report.grid(row=1, column=1, padx=5, pady=2, sticky='ew')

    btn_exit = tk.Button(frame3, text='Выход', command=exit_app)
    btn_exit.grid(row=2, column=1, padx=5, pady=2, sticky='ew')

interface3(root)

# ---- Запуск ----------------------------------- #

root.mainloop()
