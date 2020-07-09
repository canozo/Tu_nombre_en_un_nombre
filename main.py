from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import sqlite3
import random
import math
import sys

# directorio
Path("imagenes/").mkdir(exist_ok=True)

# base de datos
conn = sqlite3.connect("creados2.db")
c = conn.cursor()
c.execute("create table if not exists creados (nombre1 text, nombre2 text, unique(nombre1, nombre2))")

# leer los nombres
nombres = []
with open("nombres.txt", encoding="utf-8") as archivo:
    for line in archivo:
        if line.rstrip("\n") != '':
            nombres.append(line.rstrip("\n"))

n = len(nombres)
maximo = int(math.factorial(n) / math.factorial(n - 2))

query = c.execute("select count(*) from creados")
count = query.fetchone()[0]
if count == maximo:
    print("Ya llegó al máximo, agrega más nombres a 'nombres.txt'")
    sys.exit(0)

# size de las fuentes
font_esquina = ImageFont.truetype("Rubik-Regular.ttf", 164)
font_centro = ImageFont.truetype("Rubik-Regular.ttf", 200)

# generar 5 nombres:
generados = 0
while generados < 5 and count < maximo:
    nombre1 = random.choice(nombres)
    nombre2 = random.choice(nombres)
    print(f"Generando '{nombre1}-{nombre2}.png'... ", end="")

    query = c.execute(f"select exists(select * from creados where nombre1='{nombre1}' and nombre2='{nombre2}')")
    exists = query.fetchone()[0]

    if not exists:
        image = Image.new("RGBA", (1080, 1080), (0, 0, 0, 255))
        draw = ImageDraw.Draw(image)

        # nombre en la esquina
        text_size = font_esquina.getsize(nombre1)
        rectangle = (text_size[0] + 32, text_size[1] + 32)
        rect_img = Image.new("RGBA", rectangle, (255, 255, 255, 255))

        rect_draw = ImageDraw.Draw(rect_img)
        rect_draw.text((20, 0), nombre1, font=font_esquina, fill=(0, 0, 0, 255))
        image.paste(rect_img, (50, 50))

        # nombre en el centro
        text_size = font_centro.getsize(nombre2)
        pad = (1080 - text_size[0]) / 2
        draw.text((pad, 450), nombre2, font=font_centro)

        image.save(f"imagenes/{nombre1}-{nombre2}.png")

        # actualizar db
        c.execute(f"insert into creados (nombre1, nombre2) values ('{nombre1}', '{nombre2}')")
        generados += 1
        count += 1

        print("listo!")
    else:
        print("ya existe!")

conn.commit()
c.close()
