import yt_dlp as yt
import humanize

import tkinter as tk
import customtkinter as ctk
import threading
import subprocess
import os



window = ctk.CTk()
window.title("Baixar Vídeo")
window.geometry("620x250")
window.eval('tk::PlaceWindow . center')

main_frame = ctk.CTkFrame(window)
main_frame.grid(column=0, row=0, padx=15, pady=15)
main_frame.place(relx=.5, rely=.5,anchor=ctk.CENTER)

main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)


link = ctk.CTkEntry(main_frame, placeholder_text="Digite o link da página do vídeo", width=500, height=40)
link.grid(column=0, row=0, padx=15, pady=15)


action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
action_frame.grid(column=0, row=2, padx=15, pady=15)

button_download = ctk.CTkButton(action_frame, text="Baixar", height=35)
button_download.grid(column=0, row=0, padx=15, pady=0)


filename_var = ctk.StringVar(value="")
percent_var = ctk.StringVar(value="")
total_bytes_var = ctk.StringVar(value="")
eta_var = ctk.StringVar(value="")
speednet_var = ctk.StringVar(value="")

filename_label = ctk.CTkLabel(main_frame, textvariable=filename_var)
filename_label.grid(column=0, row=1, padx=15, pady=0)

info_frame = ctk.CTkFrame(action_frame, fg_color="transparent")

percent_label = ctk.CTkLabel(info_frame, text="Baixando: ", font=ctk.CTkFont(family="TkDefaultFont", size=12, weight='bold'))
total_bytes_label = ctk.CTkLabel(info_frame, text="Tamanho: ")
eta_label = ctk.CTkLabel(info_frame, text="Tempo restante: ")
speednet_label = ctk.CTkLabel(info_frame, text="Velocidade: ")

percent_info_label = ctk.CTkLabel(info_frame, textvariable=percent_var, font=ctk.CTkFont(family="TkDefaultFont", size=12, weight='bold'))
total_bytes_info_label = ctk.CTkLabel(info_frame, textvariable=total_bytes_var)
eta_info_label = ctk.CTkLabel(info_frame, textvariable=eta_var, width=100)
speednet_info_label = ctk.CTkLabel(info_frame, textvariable=speednet_var)

percent_label.grid(column=0, row=0, padx=0, pady=0, sticky="W")
total_bytes_label.grid(column=0, row=1, padx=0, pady=0, sticky="W")
eta_label.grid(column=0, row=2, padx=0, pady=0, sticky="W")
speednet_label.grid(column=0, row=3, padx=0, pady=0, sticky="W")

percent_info_label.grid(column=1, row=0, padx=0, pady=0, sticky="W")
total_bytes_info_label.grid(column=1, row=1, padx=0, pady=0, sticky="W")
eta_info_label.grid(column=1, row=2, padx=0, pady=0, sticky="W")
speednet_info_label.grid(column=1, row=3, padx=0, pady=0, sticky="W")



def download_video():
    button_download.configure(state=ctk.DISABLED)
    saving_path = ctk.filedialog.askdirectory()
    print(saving_path)

    if (saving_path == "" or link.get() == "" or link.get() == " "):
        button_download.configure(state=ctk.NORMAL)
        return

    def callback_infos(d):
        info_frame.grid(column=1, row=0, padx=15, pady=0)
        filename_var.set(d['filename'].split('\\')[-1])

        try:
            match d['status']:
                case 'error':
                    button_download.grid(column=0, row=0, padx=15, pady=0)
                    button_download.configure(state=ctk.NORMAL)
                    print("Erro ao baixar")

                case 'downloading':
                    percent_var.set(f'{format((d["downloaded_bytes"]/d["total_bytes"])*100, ".2f")}%')
                    total_bytes_var.set(humanize.naturalsize(d["total_bytes"]))
                    eta_var.set(humanize.naturaltime(round(d["eta"])))
                    speednet_var.set(f'{humanize.naturalsize(format(d["speed"]), ".2f")}/s')

                case 'finished':
                    if filename_var.get() == "Buscando dados...":
                        filename_var.set("Este arquivo já existe")
                        info_frame.grid_forget()
                    # else:
                    #     saving_path_dealed = saving_path.replace("/", "\\")
                    #     try: os.system(f'explorer {saving_path_dealed}') # Windows
                    #     except: os.system(f"xdg-open {saving_path_dealed}") # Mac OS or Linux
                    #     else: pass

                    ctk.filedialog.Directory()
                    button_download.grid(column=0, row=0, padx=15, pady=0)
                    button_download.configure(state=ctk.NORMAL)
                    print('finished')
        except:
            pass

    def run_thread():
        button_download.grid_forget()
        info_frame.grid_forget()
        filename_var.set("Buscando dados...")

        yt_opts = {
            'outtmpl': f'{saving_path}/%(title)s.%(ext)s',
            'progress_hooks': [callback_infos]
        }

        with yt.YoutubeDL(yt_opts) as ydl:
            ydl.download([link.get()])

    thread = threading.Thread(target=run_thread)
    thread.daemon = True
    thread.start()



button_download.configure(command=download_video)

window.mainloop()