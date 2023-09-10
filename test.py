import numpy as np

print(f'A continuación, se grafica los resultados de este modelo con los datos de test. '
      'En la gráfica se muestran el umbral de Jaccard, el mAP y la F-medida máxima.')

x = np.array([1.1, 1.3, 1.5, 1.7, 1.99, 2])
print(x, x.astype(np.uint))