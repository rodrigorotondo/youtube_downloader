from tkinter import filedialog,messagebox
import pytube
from pytube.exceptions import *
from tkinter import *
import os


save_path = ""


def descargar_video(link,nombre_archivo):
    
    try:
        yt = pytube.YouTube(link.get())
        video = yt.streams.get_highest_resolution()
        titulo_video = nombre_archivo.get()
        if titulo_video:
            video.download(output_path=save_path,filename=(titulo_video + ".mp4"))
            
        else:
            mensaje_al_usuario("No ha ingresado ningun titulo para el video!")

    except NameError:
        mensaje_al_usuario("El directorio de descarga no ha sido definido!")
    except RegexMatchError:
        mensaje_al_usuario("La url es incorrecta!")
    except (VideoUnavailable, VideoPrivate , VideoRegionBlocked):
        mensaje_al_usuario("Video no disponible :(")
    
    try:
        if os.path.isfile(save_path + "\\" + titulo_video + ".mp4"):
            mensaje_al_usuario("El archivo se descargo exitosamente!")
        else:
            mensaje_al_usuario("Algo fallo :(")
    except:
        mensaje_al_usuario("Algo fallo :(")
    
    
    
def interfaz():
    
    raiz = Tk()
    raiz.title("Youtube Downloader")
    raiz.geometry("560x250")
    raiz.config(bg="white")
    raiz.resizable(False,False)


    mi_frame= Frame(raiz, width="560", height="500")
    mi_frame.config(bg="white")
    mi_frame.pack()

    
    label_inicial = Label(mi_frame, text="Youtube Downloader")
    label_inicial.config(font=("Courier", 18), bg="white")
    label_inicial.grid(padx=10, pady=10, row=0, column=0, columnspan=2)

    label_url = Label(mi_frame, text="URL")
    label_url.config(font=("Courier", 14), bg="white")
    label_url.grid(padx=10, pady=10, row=1, column=0)

    entry_url = Entry(mi_frame) 
    entry_url.config(bg="black", width=35, insertbackground="blue",fg="white",font=10)
    entry_url.grid(padx=10, pady=10, row=1, column=1, ipady=8)

    label_nombre_del_archivo = Label(mi_frame, text="Nombre del archivo")
    label_nombre_del_archivo.config(font=("Courier", 14), bg="white")
    label_nombre_del_archivo.grid(padx=10, pady=10, row=2, column=0)

    entry_nombre_del_archivo = Entry(mi_frame)
    entry_nombre_del_archivo.config(bg="black", width=35, insertbackground="blue", fg="white",font=10)
    entry_nombre_del_archivo.grid(padx=10, pady=10, row=2, column=1, ipady=8)

    boton_elegir_ruta = Button(raiz,text="Elegir directorio de descarga" , command= lambda:elegir_directorio_de_descarga(raiz))
    boton_elegir_ruta.config(width=34, font=("Courier",14) , bg="whitesmoke")
    boton_elegir_ruta.pack()

    boton_descargar = Button(raiz, text="¡Descargar!", command= lambda:descargar_video(entry_url,entry_nombre_del_archivo))
    boton_descargar.config(width=22, font=("Courier", 14), bg="whitesmoke")
    boton_descargar.pack()

    raiz.mainloop()

def elegir_directorio_de_descarga(raiz):
    global save_path
    directorio_actual = os.getcwd()
    directorio_elegido = filedialog.askdirectory(initialdir = directorio_actual, parent= raiz,title="Por favor, elija un directorio para su descarga")

    if directorio_elegido:
        save_path = directorio_elegido
    else:
        save_path = directorio_actual

def mensaje_al_usuario(mensaje):
    
    messagebox.showinfo('Atencion!', mensaje) 


interfaz()
