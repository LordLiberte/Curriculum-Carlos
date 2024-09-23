import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import xgboost as xgb

# DATA READING AND EXPLORATION
ruta = os.getcwd()
archive = pd.read_csv(f'{ruta}\\En desarrollo\\Comercio de Criptomonedas\\dataset.csv')
df = pd.DataFrame(archive)

# Date data transformation
df['date'] = pd.to_datetime(df['date'], format="%d/%m/%Y")

# Separation of dataframe names
btc_df = df[df['name'] == 'Bitcoin']

# Standard Deviations Open-Close, High-Low
btc_df_copy = btc_df.copy()
btc_df_copy['std_high_low'] = btc_df_copy[['open', 'close']].std(axis=1)

# Añadir media móvil
window_size = 7  # Puedes ajustar este valor según tus necesidades
btc_df_copy['moving_average'] = btc_df_copy['close'].rolling(window=window_size).mean()

# Eliminar las filas con valores NaN resultantes de la media móvil
btc_df_copy = btc_df_copy.dropna()

# Escalar las columnas 'std_high_low', 'close' y 'moving_average'
scaler = MinMaxScaler()
btc_df_copy[['std_high_low', 'moving_average']] = scaler.fit_transform(btc_df_copy[['std_high_low', 'moving_average']])

# Transformar el objetivo
btc_df_copy['log_close'] = np.log1p(btc_df_copy['close'])

# Mantener la columna 'date' para visualización
btc_df_copy['month'] = btc_df_copy['date'].dt.month
btc_df_copy['day_of_week'] = btc_df_copy['date'].dt.dayofweek

# Eliminar columnas no necesarias excepto 'date'
btc_df_copy.drop(columns=['open', 'high', 'low', 'volume', 'market', 'slug', 'symbol', 'name', 'ranknow', 'close_ratio', 'spread', 'close'], inplace=True)

# Convertir las series a arrays de NumPy
X = btc_df_copy[['std_high_low', 'moving_average', 'month', 'day_of_week']].to_numpy()
y_log = btc_df_copy['log_close'].to_numpy()
dates = btc_df_copy['date']  # Mantener la columna 'date' original para visualización

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train_log, y_test_log, dates_train, dates_test = train_test_split(X, y_log, dates, test_size=0.3, random_state=42)

# Modelos base
model_gb = GradientBoostingRegressor(random_state=42)
model_rf = RandomForestRegressor(random_state=42)
model_xgb = xgb.XGBRegressor(random_state=42)

# Ajustar hiperparámetros con GridSearchCV
param_grid_gb = {
    'n_estimators': [50, 100],
    'learning_rate': [0.2, 0.5],
    'max_depth': [3, 5]
}
grid_gb = GridSearchCV(model_gb, param_grid_gb, cv=5, scoring='neg_mean_squared_error')
grid_gb.fit(X_train, y_train_log)

param_grid_rf = {
    'n_estimators': [10, 40],
    'min_samples_leaf': [50, 10]
}
grid_rf = GridSearchCV(model_rf, param_grid_rf, cv=5, scoring='neg_mean_squared_error')
grid_rf.fit(X_train, y_train_log)

# Entrenar el modelo XGBoost
model_xgb.fit(X_train, y_train_log)

# Generar predicciones de los modelos base
gb_train_preds = grid_gb.predict(X_train)
rf_train_preds = grid_rf.predict(X_train)
xgb_train_preds = model_xgb.predict(X_train)
gb_test_preds = grid_gb.predict(X_test)
rf_test_preds = grid_rf.predict(X_test)
xgb_test_preds = model_xgb.predict(X_test)

# Crear un DataFrame con las predicciones de los modelos base
X_train_meta = np.vstack([gb_train_preds, rf_train_preds, xgb_train_preds]).T
X_test_meta = np.vstack([gb_test_preds, rf_test_preds, xgb_test_preds]).T

# Entrenar el meta-modelo
meta_model = LinearRegression()
meta_model.fit(X_train_meta, y_train_log)

# Generar predicciones finales
meta_train_preds = meta_model.predict(X_train_meta)
meta_test_preds = meta_model.predict(X_test_meta)

# Revertir la transformación logarítmica
y_train_pred = np.expm1(meta_train_preds)
y_test_pred = np.expm1(meta_test_preds)
y_test_real = np.expm1(y_test_log)

# Crear DataFrame de predicciones
predictions_df = pd.DataFrame({
    'date': dates_test,
    'real': y_test_real,
    'predicción': y_test_pred
})

predictions_df.sort_values('date', inplace=True)

# Visualizar resultados
plt.figure(figsize=(12, 6))
sns.lineplot(data=predictions_df, x='date', y='real', label='Real')
sns.lineplot(data=predictions_df, x='date', y='predicción', label='Predicción')
plt.title('Predicción vs Real')
plt.xlabel('Fecha')
plt.ylabel('Precio de Bitcoin')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Evaluar el rendimiento
mse = mean_squared_error(y_test_real, y_test_pred)
mae = mean_absolute_error(y_test_real, y_test_pred)

print(f"MSE: {mse}")
print(f"MAE: {mae}")

# Obtener datos históricos reales desde Investing.com
# Asegúrate de que este archivo esté actualizado y con el formato correcto
historical_data_path = f'{ruta}\\En desarrollo\\Comercio de Criptomonedas\\Bitcoin Historical Data.csv'
historical_data = pd.read_csv(historical_data_path)

# Mostrar las primeras filas y las columnas para verificar nombres
print("Primeras filas del archivo CSV:")
print(historical_data.head())

print("\nNombres de las columnas:")
print(historical_data.columns)

# Ajusta 'Date' por el nombre correcto si es diferente
historical_data['Date'] = pd.to_datetime(historical_data['Date'])
historical_data.set_index('Date', inplace=True)
historical_data.rename(columns={'Open': 'close'}, inplace=True)  # Renombrar columna Open a close

# Calcular estadísticas recientes
recent_data = btc_df_copy.tail(window_size)  # Obtener los últimos datos disponibles
current_std_high_low = recent_data['std_high_low'].mean()  # Promedio de std_high_low
current_moving_average = recent_data['moving_average'].mean()  # Promedio de moving_average

# Generar el rango de fechas
start_date = '2019-01-01'
end_date = '2024-12-31'
date_range = pd.date_range(start=start_date, end=end_date)

# Crear un DataFrame con las fechas
future_dates_df = pd.DataFrame({'date': date_range})

# Extraer características para el rango de fechas
future_dates_df['month'] = future_dates_df['date'].dt.month
future_dates_df['day_of_week'] = future_dates_df['date'].dt.dayofweek

# Calcular características adicionales: std_high_low y moving_average
future_dates_df['std_high_low'] = current_std_high_low  # Usar desviación estándar actual
future_dates_df['moving_average'] = current_moving_average  # Usar media móvil actual

# Escalar las características de acuerdo con el escalador entrenado
# Asegúrate de que el escalador se ha ajustado a las características de entrenamiento previamente
scaler = MinMaxScaler()
scaler.fit(btc_df_copy[['std_high_low', 'moving_average']])  # Ajustar a las características de entrenamiento
future_features = future_dates_df[['std_high_low', 'moving_average']].to_numpy()
future_features_scaled = scaler.transform(future_features)  # Transformar características

# Concatenar características escaladas con 'month' y 'day_of_week'
future_features_full = np.hstack([future_features_scaled, 
                                   future_dates_df[['week']].to_numpy()])

# Generar predicciones usando el meta-modelo
future_predictions_log = meta_model.predict(future_features_full)

# Revertir la transformación logarítmica
future_predictions = np.expm1(future_predictions_log)

# Crear DataFrame con las predicciones
predictions_df = pd.DataFrame({
    'date': future_dates_df['date'],
    'predicted_price': future_predictions
})

# Graficar las predicciones
plt.figure(figsize=(14, 7))
sns.lineplot(data=predictions_df, x='date', y='predicted_price', color='blue')
plt.title('Predicción de Precio de Bitcoin (2019-2024)')
plt.xlabel('Fecha')
plt.ylabel('Precio de Bitcoin (Predicción)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()


