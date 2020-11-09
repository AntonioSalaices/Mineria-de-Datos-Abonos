import pymysql
import statistics as stats
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import tree
from sklearn.datasets import load_breast_cancer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import confusion_matrix as cm
import csv
import tkinter as tk 
import threading
import time
from tkinter import ttk
from tkinter import messagebox

importes = []
tipos = []
indices = []
fechas = []
cambios = []
monedas = []
confirmados = []

clasificar = []


gnb = GaussianNB()


root = tk.Tk()
root.configure(bg = 'beige')

root.title('Aplicación de Minería de Datos')
root.geometry("500x600")

course=["N","S","OBR","VIA","CAJ", "F","CAM","COM","REP","C"]
tk.Label(root,text="Tipo de Importe:").grid(row=1)
cb=ttk.Combobox(root,values=course,width=10)
cb.grid(column=8, row=1)
cb.current(0)


course2=["1","2"]
tk.Label(root,text="Moneda:").grid(row=2)
cb2=ttk.Combobox(root,values=course2,width=10)
cb2.grid(column=8, row=2)
cb2.current(0)


tk.Label(root, text="Tipo de Cambio:").grid(row=3)
textBox3= tk.Text(root, height=1, width=10)
textBox3.grid(row=3, column=8)

tk.Label(root, text="Tipo de cambio el dia jueves:").grid(row=4)
textBox4= tk.Text(root, height=1, width=10)
textBox4.grid(row=4, column=8)


course3=["N","S"]
tk.Label(root,text="Abono confirmado:").grid(row=5)
cb3=ttk.Combobox(root,values=course3,width=10)
cb3.grid(column=8, row=5)
cb3.current(0)



tk.Button(root, text='Clasificar', command= lambda: Hilos() ).grid(row=7, column=8)
def Limpiar():
    del clasificar[:]
tk.Button(root, text='Limpiar', command=Limpiar).grid(row=10, column=8)

# tk.Button(root, text='Grafica Importes-Fecha', command=lambda: ).grid(row=11, column=8)

 
def retrieve_input(textBox):
    time.sleep(10)
    dato1 = cb.get()
    clasificar.append(dato1)
    dato2 = cb2.get()
    clasificar.append(dato2)
    dato3 = textBox3.get("1.0",'end-1c')
    clasificar.append(dato3)
    dato4 = textBox4.get("1.0",'end-1c')
    clasificar.append(dato4)
    dato5 = cb3.get()
    clasificar.append(dato5)
    Buscar(clasificar)



def Hilos():
    Res = threading.Thread(target=retrieve_input, args=(cb,))
    Res.start()


def Buscar(Enter):
    #DATA DE ENTRADA
    print("clasificar")
    print(clasificar)
    dftest = pd.DataFrame(clasificar)
    dftest[0].replace(["N","S","OBR","VIA","CAJ", "F","CAM","COM","REP","C"],[0,1,2,3,4,5,6,7,8,9], inplace=True)
    print("frame")
    dftest[0] = dftest[0].astype(float)
    print(dftest)
    print(dftest.dtypes)
    # dftest[3].replace(["N","S"],[0,1], inplace=True)
    #FIN DATA DE ENTRADA
    datos = pd.read_csv("abonos.csv", header=None)
    df = pd.DataFrame(datos)
    df[6].replace(["N","S","OBR","VIA","CAJ", "F","CAM","COM","REP","C"],[0,1,2,3,4,5,6,7,8,9], inplace=True)
    df[14].replace(["N","S"],[0,1], inplace=True)
    bins= [0,20000,40000,60000,80000]
    names= ["abono bajo", "abono medio", "abono medio alto","abono alto"]
    df[4] = pd.cut(df[4], bins, labels=names)
    #Eliminacion de columnas con valores nulos
    df.drop([11,12,15], axis=1, inplace=True)
    #Eliminacion de campos sin influencia
    df = df.drop([0,1,3,2,5,9,10], axis=1)
    #Eliminación de Datos por fila
    df.dropna(axis=0, how="any",inplace=True)
    #Algoritmos de Mineria
    X= np.array(df.drop([4],1))
    y= np.array(df[4])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    #Clasificiacion Gaussiana
    gnb.fit(X_train,y_train)
    prediccion=gnb.predict(X_test)
    score=gnb.score(X_test,y_test)
    print("Clasificación Gaussiana")
    print(score)
    prediccion=gnb.predict(dftest)
    print("RESULTADO")
    messagebox.showinfo(message=prediccion[0], title="Clasificado como:")

    


def grafica1(dfgraf):
    time.sleep(5)
    # Graficación
    matplotlib.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots()
    ax.plot(dfgraf[4], dfgraf[6], 'o')
    ax.set_title('Relación entre los abonos y su tipo.')
    plt.show()


def grafica2(dfgraf):
    time.sleep(5)
    matplotlib.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots()
    ax.plot(dfgraf[4], dfgraf[6], 'o')
    ax.set_title('Relación entre los abonos y su tipo.')
    plt.show()

    
#     # Clasificar()

# def Clasificar(url):
#     #Aqui se clasifica la data 

root.mainloop()



