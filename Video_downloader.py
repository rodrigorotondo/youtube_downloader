from tkinter import filedialog,messagebox
from tkinter import *
import customtkinter
import os
import pytube
from pytube.exceptions import *
import time


save_path = os.getcwd()


def descargar_video(link,nombre_archivo,calidad,extension):
    #descarga el video
    #obtiene el titulo del video

    error = False

    EXTENSION_SIN_PUNTO = "mp4"
    nombre_archivo_salida = nombre_archivo.get()

    if not archivo_existe(nombre_archivo_salida,extension):
    
        try:
            #obtiene el link y crea un objeto del video
            yt = pytube.YouTube(link.get())

            if extension == ".mp4":
                #filtra por calidad, extension y por si el audio y el video estan juntos (eso significa progressive)
                video = yt.streams.filter(res=calidad.get(),file_extension=EXTENSION_SIN_PUNTO,progressive=True)
            else:
                audio = yt.streams.filter(only_audio=True)

            
            #si el titulo de video existe lo descarga con la ruta, el titulo y la extension definida
            if nombre_archivo_salida:
                #comprueba si la extension es mp4 u mp3
                if extension == ".mp4":
                    video.first().download(output_path=save_path,filename=(nombre_archivo_salida + extension))
                else:
                    audio.first().download(output_path=save_path,filename=(nombre_archivo_salida + extension))

                
            else:
                mensaje_al_usuario("No ha ingresado ningun titulo para el video!")

        except RegexMatchError:
            mensaje_al_usuario("La url es incorrecta!")
            error = True
        except (VideoUnavailable, VideoPrivate , VideoRegionBlocked):
            mensaje_al_usuario("Video no disponible :(")
            error = True
        except AttributeError:
            #este error se da cuando el objeto despues de ser filtrado no contiene la calidad elejida
            mensaje_al_usuario("El video no esta disponible en esa calidad.\nPor favor, elija otra.")
            error = True
            
        if(not error):
            mensaje_al_usuario("El archivo se descargo exitosamente!")
        
    else:
        mensaje_al_usuario("Ya existe un archivo con ese nombre.")  


def interfaz():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    raiz = customtkinter.CTk()
    raiz.title("Youtube Downloader")
    raiz.geometry("560x350")
    #raiz.config(bg="#282828")
    raiz.resizable(False,False)

    mi_frame = customtkinter.CTkFrame(master = raiz)
    mi_frame.pack()

    #label de la url
    label_url = customtkinter.CTkLabel(master = mi_frame, text="URL")
    label_url.configure(font=("Baskerville Old Face", 14))
    label_url.grid(padx=10, pady=10, row=1, column=0)

    #entry de la url
    entry_url = customtkinter.CTkEntry(master = mi_frame) 
    entry_url.grid(padx=10, pady=10, row=1, column=1, ipady=8)

    #label del nombre del archivo
    label_nombre_del_archivo = customtkinter.CTkLabel(master=mi_frame, text="Nombre del archivo")
    label_nombre_del_archivo.configure(font=("Baskerville Old Face", 14))
    label_nombre_del_archivo.grid(padx=10, pady=10, row=2, column=0)

    #entry del nombre del archivo
    entry_nombre_del_archivo = customtkinter.CTkEntry(master=mi_frame)
    entry_nombre_del_archivo.grid(padx=10, pady=10, row=2, column=1, ipady=8)

    #menu que muestra las calidades disponibles
    variable_calidad = customtkinter.StringVar(value="Elija la calidad, por favor")
    menu_opciones_calidad_lista = ["1080p" , "720p" , "480p" , "360p" , "240p" , "144p"]
    menu_opciones_calidad = customtkinter.CTkOptionMenu(raiz,values = menu_opciones_calidad_lista,variable=variable_calidad)
    menu_opciones_calidad.pack(pady=10,padx=10)
    menu_opciones_calidad.set("Elija la calidad, por favor")

    #boton para elegir la tura en la que se guarda el video
    boton_elegir_ruta = customtkinter.CTkButton(master = raiz,text="Elegir directorio de descarga" , command= lambda:elegir_directorio_de_descarga(raiz))
    boton_elegir_ruta.configure(width=34, font=("Baskerville Old Face",14))
    boton_elegir_ruta.pack(pady=10,padx=10)

    #boton que llama a la funcion que descarga el video
    boton_descargar_video = customtkinter.CTkButton(raiz, text="¡Descargar Video!", command= lambda:descargar_video(entry_url,entry_nombre_del_archivo,variable_calidad,".mp4"))
    boton_descargar_video.configure(width=22, font=("Baskerville Old Face", 14))
    boton_descargar_video.pack(padx=10,pady=10)

    #boton que llama a la funcion que descarga el audio
    boton_descargar_audio = customtkinter.CTkButton(raiz, text="¡Descargar Audio!", command= lambda:descargar_video(entry_url,entry_nombre_del_archivo,variable_calidad, ".mp3"))
    boton_descargar_audio.configure(width=22, font=("Baskerville Old Face", 14))
    boton_descargar_audio.pack(padx=10,pady=10)

    raiz.mainloop()

def elegir_directorio_de_descarga(raiz):
    #esta funcion muestra una interfaz que permite ver el lugar donde se guarda el video para seleccionarla
    global save_path
    directorio_actual = os.getcwd()
    directorio_elegido = customtkinter.filedialog.askdirectory(initialdir = directorio_actual, parent= raiz,title="Por favor, elija un directorio para su descarga")

    if directorio_elegido:
        save_path = directorio_elegido
    
def mensaje_al_usuario(mensaje):
    #envia un mensaje al usuario en el que comunica algo pasado por parametro
    messagebox.showwarning('Atencion!', mensaje)

def archivo_existe(nombre,extension):
    #comprueba la existencia de un video con el mismo nombre
    if os.path.isfile(save_path + "\\" + nombre + extension):
        return True
    else:
        return False


interfaz()
    

