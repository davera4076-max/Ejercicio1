def limpiar_registro_sensor(registro_raw: dict[str, str]) -> dict:
    """
    Procesa y normaliza un diccionario con datos crudos de un sensor térmico
    utilizando exclusivamente métodos de cadenas de texto.
    
    Parámetros:
        registro_raw (dict): Diccionario con claves 'sensor_id', 'temperatura', 'ubicacion'.
        
    Retorna:
        dict: Diccionario estandarizado con ID limpio, temperatura tipo float y ubicación segura.
    """
    # 1. Limpiamos el identificador del sensor eliminando espacios sobrantes
    sensor_id = registro_raw.get("sensor_id", "DESCONOCIDO").strip()
    
    # 2. Limpiamos y convertimos la temperatura a tipo float usando replace
    temp_raw = str(registro_raw.get("temperatura", "0"))
    try:
        temperatura = float(
            temp_raw.replace("°C", "")
                    .replace("C", "")
                    .strip()
        )
    except ValueError:
        temperatura = 0.0
        
    # 3. Limpiamos la ubicación y asignamos un valor por defecto seguro si está vacía
    ubicacion_raw = registro_raw.get("ubicacion", "")
    if not ubicacion_raw or not str(ubicacion_raw).strip():
        ubicacion = "\033[1;91m[Ubicación desconocida]\033[0m"
    else:
        ubicacion = str(ubicacion_raw).strip()
        
    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion
    }


def generar_resumen_sensores(lista_sensores_limpios: list[dict], umbral_temperatura: float) -> tuple[list[str], float]:
    """
    Analiza la colección de sensores limpios para identificar anomalías y calcular promedios.
    
    Parámetros:
        lista_sensores_limpios (list): Lista de diccionarios con datos normalizados.
        umbral_temperatura (float): Límite térmico para considerar alerta.
        
    Retorna:
        tuple: (lista de IDs en alerta, promedio térmico global)
    """
    lista_sensores_alerta = []
    suma_temperaturas = 0.0
    total_sensores = len(lista_sensores_limpios)
    
    for sensor in lista_sensores_limpios:
        temperatura = sensor["temperatura"]
        sensor_id = sensor["sensor_id"]

        if temperatura > umbral_temperatura:
            if sensor_id not in lista_sensores_alerta:
                lista_sensores_alerta.append(sensor_id)

        suma_temperaturas += temperatura
        
    promedio_temperatura = (suma_temperaturas / total_sensores) if total_sensores > 0 else 0.0

    return lista_sensores_alerta, promedio_temperatura


# ==========================================
# BLOQUE DE EJECUCIÓN Y PRUEBAS (ECOTECH)
# ==========================================
if __name__ == "__main__":
    sensores_raw = [
        {
                        "sensor_id": " TEMP-001 ",
                        "temperatura": "26.5C",
                        "ubicacion": "    Planta Tupungato"
                    },
                    {
                        "sensor_id": "TEMP-002",
                        "temperatura": "13.2 °C",
                        "ubicacion": "   "
                    },
                    {
                        "sensor_id": " TEMP-003 ", 
                        "temperatura": "28.0 C",
                        "ubicacion": "Planta San Rafael"
                    },
                    {
                        "sensor_id": "TEMP-004",
                        "temperatura": "35.8C",
                        "ubicacion": "Planta Malargüe"
                    },
                    {
                        "sensor_id": " TEMP-005 ",
                        "temperatura": "35.8C",
                        "ubicacion": "Planta San Rafael"
                    },
                    {
                        "sensor_id": "TEMP-005",
                        "temperatura": " 24.1 °C",
                        "ubicacion": "Planta Luján"
                    },
                    {
                        "sensor_id": " TEMP-006 ",
                        "temperatura": "18.7°C",
                        "ubicacion": "Planta General Alvear"
                    },
                    {
                        "sensor_id": "TEMP-007",
                        "temperatura": "29.4 C ",
                        "ubicacion": "   "
                    },
                    {
                        "sensor_id": "TEMP-008",
                        "temperatura": "32.0°C",
                        "ubicacion": "Planta Maipú"
                    },
                    {
                        "sensor_id": " TEMP-009",
                        "temperatura": "15.6 C",
                        "ubicacion": "Planta Godoy Cruz"
                    },
                    {
                        "sensor_id": " TEMP-010 ",
                        "temperatura": "21.3 °C",
                        "ubicacion": "Planta Lavalle"
                    },
                    {
                        "sensor_id": "TEMP-011 ",
                        "temperatura": " 27.8°C ",
                        "ubicacion": "Planta Tunuyán"
                    },
                    {
                        "sensor_id": "TEMP-012",
                        "temperatura": "11.5C",
                        "ubicacion": "   "
                    },
                    {
                        "sensor_id": " TEMP-013 ",
                        "temperatura": "30.2 °C",
                        "ubicacion": "Planta Guaymallén"
                    },
    ]

    # Paso 1: Normalización de registros crudos
    sensores_limpios = [limpiar_registro_sensor(registro) for registro in sensores_raw]

    # Paso 2: Análisis estadístico con un umbral de 30.0 °C
    umbral = 30.0
    sensores_alerta, promedio_global = generar_resumen_sensores(sensores_limpios, umbral)

    # Paso 3: Impresión formateada del reporte ejecutivo en columnas perfectamente alineadas
    ancho_total = 70
    print("\033[1;36m" + "=" * ancho_total + "\033[0m")
    print("\033[1;32m      REPORTE CONSOLIDADO DE SENSORES - ECOTECH SOLUTIONS\033[0m")
    print("\033[1;36m" + "=" * ancho_total + "\033[0m")
    
    # Cabeceras de la tabla con anchos fijos explícitos
    print(f"\033[1m{'ID SENSOR':<12} | {'TEMPERATURA':<14} | {'ESTADO':<10} | {'UBICACIÓN'}\033[0m")
    print("-" * ancho_total)

    for sensor in sensores_limpios:
        s_id = f"{sensor['sensor_id']:<12}"
        temp_text = f"{sensor['temperatura']:5.1f} °C"
        temp_padded = f"{temp_text:<14}"
        
        if sensor['temperatura'] > umbral:
            temp_col = f"\033[1;91m{temp_padded}\033[0m"
            estado_padded = f"{'ALERTA':<10}"
            estado_col = f"\033[1;91m{estado_padded}\033[0m"
        else:
            temp_col = f"\033[92m{temp_padded}\033[0m"
            estado_padded = f"{'Normal':<10}"
            estado_col = f"\033[92m{estado_padded}\033[0m"
            
        print(f"{s_id} | {temp_col} | {estado_col} | {sensor['ubicacion']}")

    print("\033[1;36m" + "=" * ancho_total + "\033[0m")
    print(f"\033[1mUmbral de Temperatura Establecido:\033[0m {umbral} °C")
    print(f"\033[1mDispositivos en Alerta (IDs):\033[0m \033[1;91m{sensores_alerta}\033[0m")
    print(f"\033[1mTemperatura Promedio Global:\033[0m \033[1;93m{promedio_global:.2f} °C\033[0m")
    print("\033[1;36m" + "=" * ancho_total + "\033[0m")