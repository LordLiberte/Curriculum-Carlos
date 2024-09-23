import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import axes
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Cargar datos
val_entreno = r"C:\Repositorios GitHub\Curriculum-Carlos\Con Inteligencia Artificial\NW-Taxi-Fare\Archives\train.csv"
df_entreno = pd.read_csv(val_entreno, delimiter=',')

# Transformar fecha a datetime
df_entreno['pickup_datetime'] = pd.to_datetime(df_entreno['pickup_datetime'], format='%Y-%m-%d %H:%M:%S UTC')

# Eliminar la columna 'key'
df_entreno = df_entreno.drop(['key'], axis=1)

# Escalar datos (si es necesario para el modelo, pero no para la visualización)
escalar = MinMaxScaler(feature_range=(0, 1))
df_entreno_escalar = df_entreno.drop(['pickup_datetime'], axis=1)
array_entreno_escalado = escalar.fit_transform(df_entreno_escalar)
df_entreno_escalado = pd.DataFrame(array_entreno_escalado, columns=df_entreno_escalar.columns)

# Filtrar datos para rangos específicos (opcional, basado en rangos típicos de NYC)
lat_min, lat_max = 40.5, 41
lon_min, lon_max = -74.5, -73.5
df_entreno_filtrado = df_entreno[
    (df_entreno['pickup_latitude'] >= lat_min) &
    (df_entreno['pickup_latitude'] <= lat_max) &
    (df_entreno['pickup_longitude'] >= lon_min) &
    (df_entreno['pickup_longitude'] <= lon_max)
].copy()  # .copy() necesario para que pandas no saque error de aviso por trabajar en una copia de un dataframe

# DIVISIÓN DE FECHA POR AÑO, MES, DIA, HORA, MINUTOS Y SEGUNDOS
df_entreno_filtrado['Año'] = df_entreno_filtrado['pickup_datetime'].dt.year
df_entreno_filtrado['Mes'] = df_entreno_filtrado['pickup_datetime'].dt.month
df_entreno_filtrado['Día'] = df_entreno_filtrado['pickup_datetime'].dt.day
df_entreno_filtrado['Hora'] = df_entreno_filtrado['pickup_datetime'].dt.hour
df_entreno_filtrado['Minuto'] = df_entreno_filtrado['pickup_datetime'].dt.minute
df_entreno_filtrado['Segundos'] = df_entreno_filtrado['pickup_datetime'].dt.second
# eliminamos la columna
df_entreno_filtrado = df_entreno_filtrado.drop(['pickup_datetime'], axis=1)

# ENTRENAMIENTO DE MODELO
df_entreno_filtrado = df_entreno_filtrado.drop(['dropoff_longitude', 'dropoff_latitude'], axis=1)
# eliminados por problema de valores no nulos

X = df_entreno_filtrado.drop(['passenger_count'], axis=1)
y = df_entreno_filtrado['passenger_count']

X_entreno, X_test, y_entreno, y_test = train_test_split(X, y, test_size=0.8, random_state=42)
arbol_de_decisiones = RandomForestRegressor(random_state=42, max_depth=10)
# entrenamiento
arbol_de_decisiones.fit(X_entreno, y_entreno)

prediccion = arbol_de_decisiones.predict(X_test)
score = arbol_de_decisiones.score(X_test, y_test)
print(score)
# visualización CERTEZA DEL GRAFICO

# Revisión COSTE por zona de recogida del taxi con datos originales
fig, axs = plt.subplots(ncols=2, nrows=1, figsize=(12, 6))
ax1, ax2 = axs
# primer grafico, REAL
hb1 = ax1.hexbin(X_entreno['pickup_longitude'], X_entreno['pickup_latitude'],
                 C=y_entreno, gridsize=60, bins=100)
ax1.set_xlabel('Coordenada longitud')
ax1.set_ylabel('Coordenada latitud')
ax1.set_title('Coste por zona de recogida del taxi (Real)')
fig.colorbar(hb1, ax=ax1, format='%.2f', label='Numero de pasajeros Real')

# segundo grafico, predicho
hb2 = ax2.hexbin(X_test['pickup_longitude'], X_test['pickup_latitude'],
                 C=prediccion, gridsize=60, bins=100)
ax2.set_xlabel('Coordenada longitud')
ax2.set_ylabel('Coordenada latitud')
ax2.set_title('Coste por zona de recogida del taxi (Predicho)')
fig.colorbar(hb2, ax=ax2, format='%.2f', label='Numero de pasajeros Predicho')

plt.tight_layout()
plt.show()

