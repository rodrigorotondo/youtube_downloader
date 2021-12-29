from tkinter import filedialog,messagebox
import pytube
from pytube.exceptions import *
from tkinter import *
import os


save_path = os.getcwd()


def descargar_video(link,nombre_archivo,calidad):
    #descarga el video
    #obtiene el titulo del video
    EXTENSION = ".mp4"
    EXTENSION_SIN_PUNTO = "mp4"
    nombre_archivo_salida = nombre_archivo.get()

    if not archivo_existe(nombre_archivo_salida,EXTENSION):
    
        try:
            #obtiene el link y crea un objeto del video
            yt = pytube.YouTube(link.get())
            #filtra por calidad, extension y por si el audio y el video estan juntos (eso significa progressive)
            video = yt.streams.filter(res=calidad.get(),file_extension=EXTENSION_SIN_PUNTO,progressive=True)
            
            #si el titulo de video existe lo descarga con la ruta, el titulo y la extension definida
            if nombre_archivo_salida:
                video.first().download(output_path=save_path,filename=(nombre_archivo_salida + EXTENSION))
                
            else:
                mensaje_al_usuario("No ha ingresado ningun titulo para el video!")

        except RegexMatchError:
            mensaje_al_usuario("La url es incorrecta!")
        except (VideoUnavailable, VideoPrivate , VideoRegionBlocked):
            mensaje_al_usuario("Video no disponible :(")
        except AttributeError:
            #este error se da cuando el objeto despues de ser filtrado no contiene la calidad elejida
            mensaje_al_usuario("El video no esta disponible en esa calidad.\nPor favor, elija otra.")
        
        #comprueba que el archivo exista
        if archivo_existe(nombre_archivo_salida,EXTENSION):
            mensaje_al_usuario("El archivo se descargo exitosamente!")
        else:
            mensaje_al_usuario("Algo fallo :(")
    else:
        mensaje_al_usuario("Ya existe un archivo con ese nombre.")  


def descargar_audio(link,nombre_archivo):
    #descarga el video
    #obtiene el titulo del video
    EXTENSION = ".mp3"
    nombre_archivo_salida = nombre_archivo.get()

    if not archivo_existe(nombre_archivo_salida,EXTENSION):
    
        try:
            #obtiene el link y crea un objeto del video
            yt = pytube.YouTube(link.get())
            #filtra por calidad, extension y por si el audio y el video estan juntos (eso significa progressive)
            audio = yt.streams.filter(only_audio=True)
            
            #si el titulo de video existe lo descarga con la ruta, el titulo y la extension definida
            if nombre_archivo_salida:
                audio.first().download(output_path=save_path,filename=(nombre_archivo_salida + EXTENSION))
                
            else:
                mensaje_al_usuario("No ha ingresado ningun titulo para el video!")

        except RegexMatchError:
            mensaje_al_usuario("La url es incorrecta!")
        except (VideoUnavailable, VideoPrivate , VideoRegionBlocked):
            mensaje_al_usuario("Video no disponible :(")
        except AttributeError:
            #este error se da cuando el objeto despues de ser filtrado no contiene la calidad elejida
            mensaje_al_usuario("El video no esta disponible en esa calidad.\nPor favor, elija otra.")
        
        #comprueba que el archivo exista
        if archivo_existe(nombre_archivo_salida,EXTENSION):
            mensaje_al_usuario("El archivo se descargo exitosamente!")
        else:
            mensaje_al_usuario("Algo fallo :(")
    else:
        mensaje_al_usuario("Ya existe un archivo con ese nombre.")  
    
    
def interfaz():
    
    raiz = Tk()
    #dimensiones y colores
    raiz.title("Youtube Downloader")
    raiz.iconbitmap("youtube.ico")
    raiz.geometry("560x350")
    raiz.config(bg="#282828")
    raiz.resizable(False,False)

    #dimensiones y colores del frame
    mi_frame= Frame(raiz, width="560", height="300")
    mi_frame.config(bg="#282828")
    mi_frame.pack()

    #label del titulo
    label_inicial = Label(mi_frame, text="Youtube Downloader")
    label_inicial.config(font=("Baskerville Old Face", 18), bg="#282828",fg="grey")
    label_inicial.grid(padx=10, pady=10, row=0, column=0, columnspan=2)

    #label de la url
    label_url = Label(mi_frame, text="URL",fg ="grey")
    label_url.config(font=("Baskerville Old Face", 14), bg="#282828")
    label_url.grid(padx=10, pady=10, row=1, column=0)

    #entry de la url
    entry_url = Entry(mi_frame) 
    entry_url.config(bg="black", width=35, insertbackground="whitesmoke",fg="grey",font=10)
    entry_url.grid(padx=10, pady=10, row=1, column=1, ipady=8)

    #label del nombre del archivo
    label_nombre_del_archivo = Label(mi_frame, text="Nombre del archivo",fg="grey")
    label_nombre_del_archivo.config(font=("Baskerville Old Face", 14), bg="#282828")
    label_nombre_del_archivo.grid(padx=10, pady=10, row=2, column=0)

    #entry del nombre del archivo
    entry_nombre_del_archivo = Entry(mi_frame)
    entry_nombre_del_archivo.config(bg="black", width=35, insertbackground="whitesmoke", fg="grey",font=10)
    entry_nombre_del_archivo.grid(padx=10, pady=10, row=2, column=1, ipady=8)

    #menu que muestra las calidades disponibles
    variable_calidad = StringVar(raiz)
    variable_calidad.set("Elija la calidad, por favor")
    menu_opciones_calidad_lista = ["1080p" , "720p" , "480p" , "360p" , "240p" , "144p"]
    menu_opciones_calidad = OptionMenu(raiz,variable_calidad,*menu_opciones_calidad_lista)
    menu_opciones_calidad.config(bg="#282828",fg="gray")
    menu_opciones_calidad.pack()

    #boton para elegir la tura en la que se guarda el video
    boton_elegir_ruta = Button(raiz,text="Elegir directorio de descarga" , command= lambda:elegir_directorio_de_descarga(raiz))
    boton_elegir_ruta.config(width=34, font=("Baskerville Old Face",14) , bg="#282828",fg="grey")
    boton_elegir_ruta.pack()

    #boton que llama a la funcion que descarga el video
    boton_descargar_video = Button(raiz, text="¡Descargar Video!", command= lambda:descargar_video(entry_url,entry_nombre_del_archivo,variable_calidad))
    boton_descargar_video.config(width=22, font=("Baskerville Old Face", 14), bg="#282828",fg="grey")
    boton_descargar_video.pack()

    boton_descargar_audio = Button(raiz, text="¡Descargar Audio!", command= lambda:descargar_audio(entry_url,entry_nombre_del_archivo))
    boton_descargar_audio.config(width=22, font=("Baskerville Old Face", 14), bg="#282828",fg="grey")
    boton_descargar_audio.pack()

    raiz.mainloop()

def elegir_directorio_de_descarga(raiz):
    #esta funcion muestra una interfaz que permite ver el lugar donde se guarda el video para seleccionarla
    global save_path
    directorio_actual = os.getcwd()
    directorio_elegido = filedialog.askdirectory(initialdir = directorio_actual, parent= raiz,title="Por favor, elija un directorio para su descarga")

    if directorio_elegido:
        save_path = directorio_elegido
    
def mensaje_al_usuario(mensaje):
    #envia un mensaje al usuario en el que comunica algo pasado por parametro
    
    messagebox.showinfo('Atencion!', mensaje)

def archivo_existe(nombre,extension):
    #comprueba la existencia de un video con el mismo nombre
    if os.path.isfile(save_path + "\\" + nombre + extension):
        return True
    else:
        return False



interfaz()
