import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.plot(Qo, PWf, marker='s', linestyle='--', color='green', label='PWf vs Qo')


plt.title('Gráfica de PWf vs Qo')
plt.xlabel('Qo (Caudal)')
plt.ylabel('PWf (Presión en el fondo del pozo)')
plt.grid(True)
plt.legend()


plt.show()