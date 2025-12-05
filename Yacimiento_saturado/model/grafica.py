import matplotlib.pyplot as plt


def crear_grafica(Qo, PWf):  # Renombramos a 'crear_grafica' para mayor claridad
    """
    Genera la figura de Matplotlib para la IPR y la devuelve.
    """
    fig = plt.figure(figsize=(8, 5))  # Asignamos la figura a una variable

    # 1. Creamos los ejes
    ax = fig.add_subplot(111)

    # 2. Ploteamos los datos
    ax.plot(Qo, PWf, marker='s', linestyle='--', color='green', label='PWf vs Qo')

    # 3. Configuramos la gráfica
    ax.set_title('Gráfica de IPR (Inflow Performance Relationship)')
    ax.set_xlabel('Qo (Caudal, stb/d)')
    ax.set_ylabel('PWf (Presión en el fondo del pozo, psi)')
    ax.grid(True)
    ax.legend()

    # NOTA IMPORTANTE: Quitamos plt.show()

    return fig  # Devolvemos el objeto de la figura