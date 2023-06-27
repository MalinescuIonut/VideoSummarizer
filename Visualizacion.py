from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os


##STREAM 0 IFRAMES
##STREAM 1 SRT
##STREAM 2 ESCENAS
##STREAM 3 MUESTREO
##STREAM 4  


root = Tk()

root.title('Visualizacion')

## Ajustamos ventana al tamaño de pantalla
w = root.winfo_screenwidth()
h = root.winfo_screenheight()


root.geometry("%dx%d" % (w, h))


my_canvas = Canvas(root,bg="white")
my_canvas.pack(fill=BOTH, expand=True)

##Preguntamos por el directorio de trabajo
img_dir = filedialog.askdirectory(parent=root, initialdir="D:/Temp/", title='Choose folder') 
folder=os.path.basename(os.path.normpath(img_dir))


os.chdir(img_dir)
##Guardamos subcarpetas

folder0=os.path.join(img_dir, folder.replace("summarized","summarized0"))
folder1=os.path.join(img_dir, folder.replace("summarized","summarized1"))
folder2=os.path.join(img_dir, folder.replace("summarized","summarized2"))
folder3=os.path.join(img_dir, folder.replace("summarized","summarized3"))
folder4=os.path.join(img_dir, folder.replace("summarized","summarized4"))

# Guardado de nombres de imagenes en listas, ordenadas

imgs0 = os.listdir(folder0)
imgs0 = sorted(imgs0, key=lambda x: float(x.split("-")[0]))
imgs1 = os.listdir(folder1)
imgs1 = sorted(imgs1, key=lambda x: float(x.split("-")[0]))
imgs2 = os.listdir(folder2)
imgs2 = sorted(imgs2, key=lambda x: float(x.split("-")[0]))
imgs3 = os.listdir(folder3)
imgs3 = sorted(imgs3, key=lambda x: float(x.split("-")[0]))

##Lista de tiempos de imagen
lista0=[]
lista1=[]
lista2=[]
lista3=[]

##Lista de nombres de imágenes en cada stream
pics0 = []
pics1 = []
pics2 = []
pics3 = []
pics4= []

##Lista con objetos PIL de imágenes en cada stream
ima_canvas0= []
ima_canvas1= []
ima_canvas2= []
ima_canvas3= []
ima_canvas4= []
text_canvas=[]


os.chdir(folder0)

##folder0
for image_file in imgs0:
    lista0.append(float(image_file.split("-")[0])) #Se añade los tiempos
    pics0.append(ImageTk.PhotoImage(Image.open(image_file).resize(( int(w/6),int(h/6*0.9))))) ## Se añade imagen reescalada


##folder1

os.chdir(folder1)
for image_file in imgs1:
    lista1.append(float(image_file.split("-")[0]))  #Se añade los tiempos
    pics1.append(ImageTk.PhotoImage(Image.open(image_file).resize(( int(w/6),int(h/6*0.9))))) ## Se añade imagen reescalada

##folder2
os.chdir(folder2)
for image_file in imgs2:
    lista2.append(float(image_file.split("-")[0]))  #Se añade los tiempos
    pics2.append(ImageTk.PhotoImage(Image.open(image_file).resize(( int(w/6),int(h/6*0.9))))) ## Se añade imagen reescalada

##folder3
os.chdir(folder3)
for image_file in imgs3:
    lista3.append(float(image_file.split("-")[0]))  #Se añade los tiempos
    pics3.append(ImageTk.PhotoImage(Image.open(image_file).resize(( int(w/6),int(h/6*0.9))))) ## Se añade imagen reescalada

#Ultima imagen añadida
lastImage=0

#coord x última imagen añadida
currentx=0

#índice de cada carpeta
folder0Idx=0
folder1Idx=0
folder2Idx=0
folder3Idx=0

#Recorrido de todas las carpetas a la vez
while (folder0Idx < len(lista0) ) and (folder1Idx < len(lista1) ) and (folder2Idx < len(lista2) ) and (folder3Idx < len(lista3) ): 
    #Si el stream de Iframes es el siguiente
    if (lista0[folder0Idx] < lista1[folder1Idx]) and (lista0[folder0Idx] < lista2[folder2Idx]) and (lista0[folder0Idx] < lista3[folder3Idx]): 
        os.chdir(folder4)
        #Si última en añadirse es Iframe o no se encuentra en el resumen final
        if(lastImage==0 or (os.path.exists(imgs0[folder0Idx]))):
            currentx+= w/6 #Aumentas x la mitad de fotograma
        else:
            currentx+=w/12 #Aumentas x fotograma completo
        os.chdir(folder0)
        #Dibujas Por pantalla imagen en stream de Iframes
        ima_canvas0.append(my_canvas.create_image(currentx,h/6, anchor=NW, image=pics0[folder0Idx])) 
        #Dibujas Por pantalla texto con tiempo de fotograma
        text_canvas.append(my_canvas.create_text(currentx,h/6-20,text=str(round(lista0[folder0Idx],1)), fill="black",font=('Helvetica 15 bold'))) 
        os.chdir(folder4)
        #Si el Iframe se encuentra en resumen final
        if(os.path.exists(imgs0[folder0Idx])):
            #Dibujas Por pantalla imagen en stream de resumen final
            pics4.append(ImageTk.PhotoImage(Image.open(imgs0[folder0Idx]).resize(( int(w/6),int(h/6)))))
            ima_canvas4.append(my_canvas.create_image(currentx,5*h/6, anchor=NW, image=pics4[-1]))
        lastImage= 0
        folder0Idx+=1

    #Si el stream de subtítulos es el siguiente
    elif (lista1[folder1Idx] < lista2[folder2Idx]) and (lista1[folder1Idx] < lista3[folder3Idx]):
        os.chdir(folder4)
        #Si última en añadirse es subtítulo o no se encuentra en el resumen final
        if( lastImage==1 or (os.path.exists(imgs1[folder1Idx]))):
            currentx += w/6 #Aumentas x la mitad de fotograma
        else:
            currentx+=w/12 #Aumentas x fotograma completo
        os.chdir(folder1)
        #Dibujas Por pantalla imagen en stream de subtítulos
        ima_canvas1.append(my_canvas.create_image(currentx,2*h/6, anchor=NW, image=pics1[folder1Idx]))
        #Dibujas Por pantalla texto con tiempo de fotograma
        text_canvas.append(my_canvas.create_text(currentx,h/6-20,text=str(round(lista1[folder1Idx],1)), fill="black",font=('Helvetica 15 bold')))

        os.chdir(folder4)
        #Si el fotograma de subtítulo se encuentra en resumen final
        if(os.path.exists(imgs1[folder1Idx])):
            #Dibujas Por pantalla imagen en stream de resumen final
            pics4.append(ImageTk.PhotoImage(Image.open(imgs1[folder1Idx]).resize(( int(w/6),int(h/6)))))
            ima_canvas4.append(my_canvas.create_image(currentx,5*h/6, anchor=NW, image=pics4[-1]))
        
        lastImage= 1
        folder1Idx+=1


    #Si el stream de escenas es el siguiente
    elif (lista2[folder2Idx] < lista3[folder3Idx]):
        os.chdir(folder4)
        #Si última en añadirse es fotograma de escena o no se encuentra en el resumen final
        if(lastImage==2 or (os.path.exists(imgs2[folder2Idx]))):
            currentx += w/6 #Aumentas x la mitad de fotograma
        else:
            currentx+=w/12 #Aumentas x fotograma completo
        os.chdir(folder2)
        #Dibujas Por pantalla imagen en stream de resumen final
        ima_canvas2.append(my_canvas.create_image(currentx,3*h/6, anchor=NW, image=pics2[folder2Idx]))
        #Dibujas Por pantalla texto con tiempo de fotograma
        text_canvas.append(my_canvas.create_text(currentx,h/6-20,text=str(round(lista2[folder2Idx],1)), fill="black",font=('Helvetica 15 bold')))

        os.chdir(folder4)
        #Si el fotograma de escena se encuentra en resumen final
        if(os.path.exists(imgs2[folder2Idx])):
            #Dibujas Por pantalla imagen en stream de resumen final
            pics4.append(ImageTk.PhotoImage(Image.open(imgs2[folder2Idx]).resize(( int(w/6),int(h/6)))))
            ima_canvas4.append(my_canvas.create_image(currentx,5*h/6, anchor=NW, image=pics4[-1]))
        
        lastImage=2
        folder2Idx+=1
    
    #Si el stream de fotogramas de muestreo es el siguiente
    else:
        os.chdir(folder4)
        #Si última en añadirse es fotograma de muestreo o no se encuentra en el resumen final
        if((lastImage==3) or (os.path.exists(imgs3[folder3Idx]))):
            currentx += w/6 #Aumentas x la mitad de fotograma
        else:
            currentx+=w/12 #Aumentas x fotograma completo
        os.chdir(folder3)
        #Dibujas Por pantalla imagen en stream de resumen final
        ima_canvas3.append(my_canvas.create_image(currentx,4*h/6, anchor=NW, image=pics3[folder3Idx]))
        text_canvas.append(my_canvas.create_text(currentx,h/6-20,text=str(round(lista3[folder3Idx],1)), fill="black",font=('Helvetica 15 bold')))

        os.chdir(folder4)
        #Si el fotograma de muestreo se encuentra en resumen final
        if(os.path.exists(imgs3[folder3Idx])):
            #Dibujas Por pantalla imagen en stream de resumen final
            pics4.append(ImageTk.PhotoImage(Image.open(imgs3[folder3Idx]).resize(( int(w/6),int(h/6)))))
            ima_canvas4.append(my_canvas.create_image(currentx,5*h/6, anchor=NW, image=pics4[-1]))

        lastImage=3
        folder3Idx+=1

##Si pulsas teclas de dirección te mueves por el programa
xMAx=currentx-w/6
currentx=0
def left(event):
    global currentx
    print (currentx)
    if currentx >= w/3:
        currentx -= w/3
        x = w/3
        y = 0
        for img in ima_canvas0:
            my_canvas.move(img, x, y)

        for img in ima_canvas1:
            my_canvas.move(img, x, y)

        for img in ima_canvas2:
            my_canvas.move(img, x, y)

        for img in ima_canvas3:
            my_canvas.move(img, x, y)

        for img in ima_canvas4:
            my_canvas.move(img, x, y)

        for texttime in text_canvas:
            my_canvas.move(texttime, x, y)
	

def right(event):
    global currentx
    global xMAx
    print (currentx)

    if currentx <= xMAx:
        currentx += w/3
        x = -w/3
        y = 0
        for img in ima_canvas0:
            my_canvas.move(img, x, y)
        
        for img in ima_canvas1:
            my_canvas.move(img, x, y)

        for img in ima_canvas2:
            my_canvas.move(img, x, y)

        for img in ima_canvas3:
            my_canvas.move(img, x, y)

        for img in ima_canvas4:
            my_canvas.move(img, x, y)

        for texttime in text_canvas:
            my_canvas.move(texttime, x, y)


def up(event):
    x = 0
    y = -10
    for img in ima_canvas0:
        my_canvas.move(img, x, y)
	
    for img in ima_canvas1:
        my_canvas.move(img, x, y)

    for img in ima_canvas2:
        my_canvas.move(img, x, y)
        
    for img in ima_canvas3:
        my_canvas.move(img, x, y)

    for img in ima_canvas4:
        my_canvas.move(img, x, y)
    
    for texttime in text_canvas:
        my_canvas.move(texttime, x, y)


def down(event):
    x = 0
    y = 10
    for img in ima_canvas0:
        my_canvas.move(img, x, y)
	
    for img in ima_canvas1:
        my_canvas.move(img, x, y)

    for img in ima_canvas2:
        my_canvas.move(img, x, y)
        
    for img in ima_canvas3:
        my_canvas.move(img, x, y)

    for img in ima_canvas4:
        my_canvas.move(img, x, y)
    
    for texttime in text_canvas:
        my_canvas.move(texttime, x, y)



root.bind("<Left>", left)
root.bind("<Right>", right)
root.bind("<Up>", up)
root.bind("<Down>", down)




root.mainloop()
