import csv
import qrcode
import random
import tkinter as tk
from PIL import Image, ImageTk

# lista para almacenar los datos de los códigos QR generados
qr_data_list = []

# function para generar un código QR con un número aleatorio
def generate_random_qr_code():
    number = random.randint(1000, 9999)
    data = str(number)
    qr_code_size = random.randint(50, 200)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=qr_code_size // 10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_code_img = qr.make_image(fill_color="black", back_color="white")

    # setea una inclinación aleatoria al código QR dentro de los angulos indicados
    angle = random.randint(-20, 20)
    qr_code_img = qr_code_img.rotate(angle, resample=Image.BILINEAR, center=(qr_code_img.width / 2, qr_code_img.height / 2))

    # almacena los datos del código QR generado en una lista
    qr_data_list.append([number, qr_code_size, angle, qr_code_speed])

    return qr_code_img, number

# funcion encargada de la animación
def update_animation():
    global x, y, qr_code_label, current_number

    # mueve al código QR a la derecha
    x += qr_code_speed
    if x > screen_width:
        x = -qr_code_size
        qr_code_img, current_number = generate_random_qr_code()
        qr_code_photo = ImageTk.PhotoImage(qr_code_img)
        qr_code_label.configure(image=qr_code_photo)
        qr_code_label.qr_code_photo = qr_code_photo

        # Generar una nueva posición Y aleatoria cercana al centro de la pantalla
        y = random.randint((screen_height - qr_code_size) // 3, (2 * screen_height - qr_code_size) // 3)

    # actuliza la posición del código QR
    qr_code_label.place(x=x, y=y)

    # setea la próxima actualización
    root.after(50, update_animation)

# función para guardar los datos en un archivo CSV
def save_to_csv():
    with open('qr_data.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Número', 'Tamaño', 'Inclinación', 'Velocidad'])
        writer.writerows(qr_data_list)

# resolucion de la pantalla
screen_width = 1280
screen_height = 768

# parametros de la animación
qr_code_size = 100
qr_code_speed = 60

# inicia la ventana de tkinter
root = tk.Tk()
root.title("QRgenerator - Scanner tester")

# Botón para guardar los datos en un archivo CSV
save_button = tk.Button(root, text="Guardar en CSV", command=save_to_csv)
save_button.pack()

# inicia la posición del código QR
x = 0

# genera el primer código QR y la posición vertical aleatoria inicial
qr_code_img, current_number = generate_random_qr_code()
qr_code_photo = ImageTk.PhotoImage(qr_code_img)
y = random.randint((screen_height - qr_code_size) // 3, (2 * screen_height - qr_code_size) // 3)

# crea la etiqueta inicial para la animación del código QR
qr_code_label = tk.Label(root, image=qr_code_photo)
qr_code_label.qr_code_photo = qr_code_photo
qr_code_label.pack()

# programa la primera actualización de la animación
root.after(50, update_animation)

# inicia la ventana
root.geometry(f"{screen_width}x{screen_height}")
root.mainloop()
