import pandas as pd

def evaluar_elcsa(archivo_entrada, archivo_salida):
    print(f"Cargando datos de: {archivo_entrada}...")
    
    # 1. Cargar el CSV
    df = pd.read_csv(archivo_entrada, encoding='utf-8-sig')
    
    # 2. Limpiar espacios en blanco de las respuestas para evitar errores de lectura
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    
    # 3. Definir las columnas que corresponden a la prueba ELCSA
    elcsa_cols = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 
                  'E9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15']
    
    # Validar que las columnas existan en el CSV
    columnas_faltantes = [col for col in elcsa_cols if col not in df.columns]
    if columnas_faltantes:
        print(f"Error: Faltan las siguientes columnas en el CSV: {columnas_faltantes}")
        return

    # 4. Calcular el puntaje: 'SI' suma 1 punto, cualquier otra cosa (NO, NaN) suma 0
    print("Calculando puntajes ELCSA...")
    df_puntajes = df[elcsa_cols].map(lambda x: 1 if str(x).upper() == 'SI' else 0)
    df['Puntaje_ELCSA'] = df_puntajes.sum(axis=1)
    
    # 5. Algoritmo de clasificación ELCSA
    def clasificar(row):
        puntaje = row['Puntaje_ELCSA']
        
        # Verificar si hay menores de edad en el hogar (DSE10 == 'SI')
        # Si tu columna se llama distinto, cambia 'DSE10' por el nombre correcto.
        hay_menores = True if str(row.get('DSE10', 'NO')).upper() == 'SI' else False
        
        if hay_menores: # Escala para hogares CON menores (15 preguntas)
            if puntaje == 0: return 'Seguridad Alimentaria'
            elif 1 <= puntaje <= 5: return 'Inseguridad Alimentaria Leve'
            elif 6 <= puntaje <= 10: return 'Inseguridad Alimentaria Moderada'
            else: return 'Inseguridad Alimentaria Severa'
        else: # Escala para hogares SIN menores (8 preguntas)
            if puntaje == 0: return 'Seguridad Alimentaria'
            elif 1 <= puntaje <= 3: return 'Inseguridad Alimentaria Leve'
            elif 4 <= puntaje <= 6: return 'Inseguridad Alimentaria Moderada'
            else: return 'Inseguridad Alimentaria Severa'

    df['Clasificacion_ELCSA'] = df.apply(clasificar, axis=1)
    
    # 6. Guardar el nuevo CSV con las dos nuevas columnas
    df.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
    print(f"✅ ¡Éxito! Archivo calificado guardado como: {archivo_salida}")

if __name__ == '__main__':
    # Configura aquí el nombre de tu archivo de entrada y cómo quieres que se llame el de salida
    ARCHIVO_ENTRADA = 'DB.csv' 
    ARCHIVO_SALIDA = 'DB_ELCSA_Calificado.csv'
    
    evaluar_elcsa(ARCHIVO_ENTRADA, ARCHIVO_SALIDA)
