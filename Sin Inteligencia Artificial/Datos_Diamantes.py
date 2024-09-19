import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

diamantes = sns.load_dataset('diamonds')
print("--------------------- INFORMACIÓN DE DATAFRAME -------------------")
print(diamantes.head())
print('-'*50)
print(diamantes.info())
print('-'*50)
print(diamantes.describe())
print('----------------------------- FIN --------------------------------')

# graficos relacionales

sns.set_style('whitegrid')

# comparativa entre el precio del diamante y su color

sns.catplot(
    data=diamantes,
    x='color',
    y='price',
    kind='bar',
    hue='cut'
)

plt.show()

# comparativa entre el corte de un diamente y sus valores X, Y y Z

sns.displot(
    data=diamantes,
    x='color',
    y='x',
    hue='cut'
)

plt.show()

# comparativa entre relaciones especificas

graf = sns.jointplot(
    data=diamantes,
    x='cut',
    y='carat',
    kind='hist',
)

graf.set_axis_labels('Calidad de Corte',
                     'Peso en quilates')

plt.show()

# comparativa entre todas las variables

graf2 = sns.pairplot(
    data=diamantes,
    corner=True,
)

graf.set_axis_labels('Calidad de Corte',
                     'Peso en quilates')

plt.show()