import xlwings as xw
import matplotlib.pyplot as plt
import numpy as np

from Yacimiento_saturado.model.funciones import Caudal
from Yacimiento_saturado.model.grafica import crear_grafica

def main():
    wb = xw.Book.caller()
    sheet = wb.sheets[0]

    # Datos Base desde Excel

    # Pr (Presión Yacimiento)
    Pr = sheet["C7"].value
    # Qmax (Caudal Máximo)
    Qmax = sheet["C8"].value
    # Pwf (Lista de Presiones)
    Pwf_list = sheet["C10:H10"].value

    # Calcular Caudal (Qo)
    Qo_list = []

    # Iteramos sobre la lista de presiones válidas para calcular el caudal
    for Pwf in Pwf_list:
        Qo = Caudal(Pr, Pwf, Qmax)
        Qo_list.append(Qo)

    # Limpiar columnas de resultados anteriores
    sheet["B13:C100"].clear_contents()
    # Resultados

    sheet["B12"].value = "Pwf (psi)"
    sheet["C12"].value = "Qo (stb/d)"

    # Escribir Pwf
    sheet["B13"].value = np.array(Pwf_list).reshape(-1, 1)
    # Escribir Qo
    sheet["C13"].value = np.array(Qo_list).reshape(-1, 1)

    # Insertar la Gráfica en Excel

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


@xw.func
def hello(name):
    """Función de ejemplo que puede ser llamada directamente desde Excel."""
    return f"Hello {name}!"


if __name__ == "__main__":
    try:
        xw.Book("tarea.xlsm").set_mock_caller()
        main()
    except Exception as e:
        print(f"Ocurrió un error al ejecutar main: {e}")