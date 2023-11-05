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

def converter(input_notebook_file):
    """This function automates the process of converting Jupyter Notebook files (.ipynb) to plain text files (.txt)
    by extracting only the code portions.

    Args:
        input_notebook_file (str, optional): A str with the name of the Jupyter Notebook file 
        (including the file extension .ipynb) that you want to convert to plain text.
    """
    
    import nbformat as nbf
    import os
    import traceback
    
    if '.ipynb' not in input_notebook_file:
            input_notebook_file = input_notebook_file + '.ipynb'
    
    output_text_file = input_notebook_file.split('.')[0] + '.txt'

    try:
        ntbk = nbf.read(input_notebook_file, nbf.NO_CONVERT)
        new_ntbk = ntbk
        new_ntbk.cells = [cell for cell in ntbk.cells if cell.cell_type != "markdown"]
        nbf.write(new_ntbk, output_text_file, version=nbf.NO_CONVERT)
        lines = [cell['source'] + '\n\n\n' for cell in new_ntbk['cells']]
        with open(os.path.join('.', output_text_file), 'w', encoding='utf-8') as file:
            file.writelines(lines)
    except:
        traceback.print_exc()
    
def converter_2(input_notebook_file):
    """ This function automates the process of converting Jupyter Notebook files (.ipynb) to plain text files (.txt)
        by extracting only the code portions.

        Args:
            input_notebook_file (str, optional): A str with the name of the Jupyter Notebook file 
            (including the file extension .ipynb) that you want to convert to plain text.
    """
    
    import os
    import json
    
    if '.ipynb' not in input_notebook_file:
            input_notebook_file = input_notebook_file + '.ipynb'
    
    output_text_file = input_notebook_file.split('.')[0] + '.txt'
    
    temp_text_file = output_text_file.split('.')[0] + ".json"
    src = os.path.join('.',input_notebook_file)
    dst = os.path.join('.',temp_text_file)
        
    if os.name == 'nt':  # Windows
        cmd = f'copy "{src}" "{dst}"'
    else:  # Unix/Linux
        cmd = f'cp "{src}" "{dst}"'
    try:    
        os.system(cmd)
            
        with open(dst, "r", encoding="utf-8") as file:
            file_load = json.load(file)
            file_cells = file_load['cells']
            txt_file = []
            for cell in file_cells:
                if cell['cell_type'] != 'markdown':
                    for index, source in enumerate(cell['source']):
                        txt_file.append(source)
                        if index == len(cell['source'])-1:
                            txt_file.append('\n\n\n\n')
                
                
        with open(output_text_file, "w", encoding="utf-8") as file:
            file.writelines(txt_file)
        
        if os.name == 'nt':  # Windows
            cmd = f'del "{dst}"'
        else:  # Unix/Linux
            cmd = f'rm "{dst}"'
        
        os.system(cmd)
    except:
        print('Los argumentos no son validos.')