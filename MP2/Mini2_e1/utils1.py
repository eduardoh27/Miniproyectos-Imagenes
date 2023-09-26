import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage.morphology as morf
from skimage.color import rgb2gray,rgba2rgb,gray2rgb
from skimage.morphology import ball
from skimage.segmentation import watershed
import cv2

def imposed_minima(imagen):
    plt.rcParams["figure.figsize"] = [7.50, 7.50]
    plt.rcParams["figure.autolayout"] = True

    # Se crea la figura
    plt.ion()
    fig, ax = plt.subplots()

    # Se inicializa la imagen para la visualización
    img3 = gray2rgb(imagen)

    # Se inicializan las matrices para guardar las semillas
    higado = np.zeros(imagen.shape,dtype=bool)
    background = np.zeros(imagen.shape,dtype=bool)

    # Se crean las funciones para poder interactuar
    objeto = 'higado'

    def click_liver(event):
        nonlocal higado
        y,x = int(np.round(event.xdata,0)),int(np.round(event.ydata,0))
        copy = np.zeros(imagen.shape)
        copy[x, y] = True
        copy = morf.binary_dilation(copy,ball(5)[5])
        higado =  np.bitwise_or(copy,higado)

    def click_background(event):
        nonlocal background
        y,x = int(np.round(event.xdata,0)),int(np.round(event.ydata,0))
        copy = np.zeros(imagen.shape)
        copy[x, y] = True
        copy = morf.binary_dilation(copy,ball(5)[5])
        background = np.bitwise_or(copy,background)


    continuar = True
    def close1(event):
        nonlocal objeto,fig
        objeto = 'fondo'
        fig.canvas.mpl_connect('button_press_event', click_background)
        fig.canvas.mpl_connect('key_press_event', close2)

    def close2(event):
        nonlocal continuar,fig
        continuar = False
        plt.close(fig)
        
    # Se asignan las funciones para la interacción
    fig.canvas.mpl_connect('button_press_event', click_liver)
    fig.canvas.mpl_connect('key_press_event', close1)
    plt.show()
    # Se inicia el programa de forma interactiva
    while continuar:
        plt.clf()
        plt.title(f'seleccione las semillas para el {objeto}')
        img3[:, :, 0][higado] = 1
        img3[:, :, 1][background] = 1
        plt.imshow(img3)
        plt.axis('off')
        plt.draw()
        plt.pause(0.001)
    plt.ioff()
    copia = np.zeros(imagen.shape)
    copia[higado] = 2
    copia[background] = 1
    return copia

