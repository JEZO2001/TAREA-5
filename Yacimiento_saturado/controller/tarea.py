import xlwings as xw
import matplotlib.pyplot as plt
import numpy as np

# Importaciones específicas de las funciones desde el Modelo
# Esto requiere que el script se ejecute desde la carpeta raíz del proyecto
from Yacimiento_saturado.model.funciones import Caudal
from Yacimiento_saturado.model.grafica import crear_grafica


def main():
    # Conecta con el libro de trabajo que llama al script
    wb = xw.Book.caller()
    sheet = wb.sheets[0]  # Usamos el índice 0 para la primera hoja (más seguro)

    # --- 1. 📥 Leer Datos Base desde Excel ---

    # Pr (Presión Yacimiento) se lee de B1
    Pr = sheet["C7"].value
    # Qmax (Caudal Máximo) se lee de B2
    Qmax = sheet["C8"].value
    # Pwf (Lista de Presiones) se lee del rango B4:B9
    Pwf_list_raw = sheet["C10:H10"].value

    # Limpieza de la lista leída: elimina valores None y maneja la estructura
    if isinstance(Pwf_list_raw, list):
        # Aplanar la lista y eliminar None (maneja listas de listas o listas simples)
        Pwf_list = [p for sublist in Pwf_list_raw if isinstance(sublist, list) for p in
                    sublist if p is not None]
        # Si la lista no estaba anidada
        if not Pwf_list:
            Pwf_list = [p for p in Pwf_list_raw if p is not None]
    else:
        # Manejar el caso de un solo valor o None
        Pwf_list = [Pwf_list_raw] if Pwf_list_raw is not None else []

    # Verificar si se leyeron los valores clave antes de calcular
    if Pr is None or Qmax is None or not Pwf_list:
        sheet["A12"].value = "ERROR: Faltan datos de entrada (Pr, Qmax o Pwf)."
        return

    # --- 2. 🧮 Calcular Caudal (Qo) ---

    Qo_list = []

    # Iteramos sobre la lista de presiones válidas para calcular el caudal
    for Pwf in Pwf_list:
        Qo = Caudal(Pr, Pwf, Qmax)
        Qo_list.append(Qo)

    # --- 3. ✍️ Escribir Resultados en Excel ---

    sheet["B12"].value = "Pwf (psi)"
    sheet["C12"].value = "Qo (stb/d)"

    # Limpiar columnas de resultados anteriores
    sheet["B13:C100"].clear_contents()

    # Escribir Pwf (debe ser una columna, por eso usamos reshape)
    sheet["B13"].value = np.array(Pwf_list).reshape(-1, 1)

    # Escribir Qo
    sheet["C13"].value = np.array(Qo_list).reshape(-1, 1)

    # --- 4. 🖼️ Generar e Insertar la Gráfica en Excel ---

    # A. Generar el objeto figura
    figura_mpl = crear_grafica(Qo_list, Pwf_list)

    # B. Insertar la figura en Excel (en la celda G3)
    sheet.pictures.add(
        figura_mpl,
        name='GraficaIPR',
        update=True,
        left=sheet.range('E13').left,
        top=sheet.range('E13').top
    )

    # C. Cerrar la figura de Matplotlib para liberar memoria
    plt.close(figura_mpl)

    sheet[
        "A21"].value = f"Cálculo y gráfica insertados correctamente a las: {xw.utils.datetime.now().strftime('%H:%M:%S')}"


@xw.func
def hello(name):
    """Función de ejemplo que puede ser llamada directamente desde Excel."""
    return f"Hello {name}!"


if __name__ == "__main__":
    # Simula la llamada desde Excel para pruebas en PyCharm
    # Asegúrate de que tarea.xlsm existe y está en el directorio correcto
    try:
        xw.Book("tarea.xlsm").set_mock_caller()
        main()
    except Exception as e:
        print(f"Ocurrió un error al ejecutar main: {e}")