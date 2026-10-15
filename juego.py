import atexit
import math
import os
import random
import struct
import tempfile
import tkinter as tk
import wave

try:
    import winsound
except ImportError:
    winsound = None

ANCHO = 1000
ALTO = 600
ANCHO_LUCHADOR = 80
VELOCIDAD = 24

vida_jugador = 100
vida_enemigo = 100
player_x = 150
enemy_x = 750
fin_del_juego = False
ataque_disponible = True
temporizador_enemigo = None

root = tk.Tk()
root.title("Duelo Arcade: Nova vs. Brasa")
root.resizable(False, False)

canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="#11131c", highlightthickness=0)
canvas.pack()

# Arena y barras de vida
canvas.create_rectangle(0, 0, ANCHO, 450, fill="#222244", outline="")
canvas.create_rectangle(0, 450, ANCHO, ALTO, fill="#555555", outline="")
canvas.create_oval(440, 85, 560, 205, fill="#343451", outline="#555577", width=3)
canvas.create_line(0, 450, ANCHO, 450, fill="#d0d0d0", width=3)
canvas.create_line(0, 525, ANCHO, 525, fill="#777777", width=2)
canvas.create_line(100, 450, 160, 525, fill="#777777", width=2)
canvas.create_line(840, 450, 900, 525, fill="#777777", width=2)
canvas.create_rectangle(20, 40, 220, 60, fill="#392f36", outline="")
canvas.create_rectangle(780, 40, 980, 60, fill="#392f36", outline="")
barra_jugador = canvas.create_rectangle(20, 40, 220, 60, fill="#35d07f", outline="")
barra_enemigo = canvas.create_rectangle(780, 40, 980, 60, fill="#f05252", outline="")
texto_jugador = canvas.create_text(20, 25, anchor="w", text="NOVA", fill="white", font=("Arial", 12, "bold"))
texto_enemigo = canvas.create_text(980, 25, anchor="e", text="BRASA", fill="white", font=("Arial", 12, "bold"))
mensaje = canvas.create_text(ANCHO // 2, 110, text="", fill="white", font=("Arial", 26, "bold"))
mensaje_accion = canvas.create_text(ANCHO // 2, 230, text="", fill="#ffe27a", font=("Arial", 20, "bold"))
canvas.create_text(ANCHO // 2, 555, text="A / D o flechas: mover     J: golpe     K: patada     ESPACIO: saltar     R: reiniciar", fill="white", font=("Arial", 13, "bold"))

def crear_luchador(x, color, etiqueta, direccion, estilo):
    pierna_delantera = x + 52 if direccion > 0 else x + 28
    pierna_trasera = x + 28 if direccion > 0 else x + 52
    canvas.create_line(pierna_trasera, 405, pierna_trasera - 8, 466, pierna_trasera - 13, 480, fill="#252633", width=16, capstyle=tk.ROUND, tags=etiqueta)
    pierna = canvas.create_line(pierna_delantera, 405, pierna_delantera + 8, 466, pierna_delantera + 13, 480, fill="#303241", width=16, capstyle=tk.ROUND, tags=etiqueta)
    canvas.create_oval(pierna_trasera - 21, 472, pierna_trasera + 2, 486, fill="#171820", outline="white", width=1, tags=etiqueta)
    bota = canvas.create_oval(pierna_delantera + 2, 472, pierna_delantera + 25, 486, fill="#171820", outline="white", width=1, tags=etiqueta)
    canvas.create_line(x + 20, 345, x + 5, 382, x + 12, 397, fill=color, width=13, capstyle=tk.ROUND, tags=etiqueta)
    canvas.create_oval(x + 3, 389, x + 20, 406, fill="#252633", outline="white", tags=etiqueta)
    brazo_delantero = x + 56 if direccion > 0 else x + 24
    guante_delantero = x + 72 if direccion > 0 else x + 8
    brazo = canvas.create_line(brazo_delantero, 345, guante_delantero, 374, guante_delantero, 389, fill=color, width=14, capstyle=tk.ROUND, tags=etiqueta)
    guante = canvas.create_oval(guante_delantero - 10, 382, guante_delantero + 10, 402, fill="#252633", outline="white", width=2, tags=etiqueta)
    canvas.create_rectangle(x + 33, 317, x + 47, 338, fill="#d6a887", outline="", tags=etiqueta)
    cuerpo = canvas.create_polygon(x + 30, 330, x + 50, 330, x + 62, 350, x + 55, 405, x + 25, 405, x + 18, 350, fill=color, outline="white", width=2, tags=etiqueta)
    canvas.create_line(x + 25, 354, x + 55, 354, fill="#ffffff", width=2, tags=etiqueta)
    color_cinturon = "#e8fbff" if estilo == "nova" else "#ffbd4a"
    canvas.create_rectangle(x + 24, 385, x + 56, 394, fill=color_cinturon, outline="#362a1b", tags=etiqueta)
    canvas.create_oval(x + 25, 292, x + 55, 322, fill="#d6a887", outline="#171717", width=2, tags=etiqueta)
    if estilo == "nova":
        canvas.create_arc(x + 23, 287, x + 57, 313, start=0, extent=180, fill="#24212b", outline="#24212b", tags=etiqueta)
        canvas.create_line(x + 24, 301, x + 56, 301, fill="#e8fbff", width=4, tags=etiqueta)
        canvas.create_line(x + 25, 301, x + 15, 294, x + 14, 303, fill="#e8fbff", width=3, tags=etiqueta)
        canvas.create_oval(x + 35, 363, x + 45, 373, fill="#e8fbff", outline="", tags=etiqueta)
    else:
        canvas.create_polygon(x + 24, 303, x + 25, 288, x + 34, 298, x + 42, 283, x + 46, 297, x + 57, 289, x + 54, 307, fill="#ffbd4a", outline="#54291f", tags=etiqueta)
        canvas.create_polygon(x + 17, 345, x + 30, 337, x + 39, 349, x + 30, 359, fill="#ffbd4a", outline="#54291f", tags=etiqueta)
        canvas.create_polygon(x + 34, 365, x + 43, 360, x + 47, 369, x + 39, 376, fill="#54291f", outline="", tags=etiqueta)
    ojo_x = x + 43 if direccion > 0 else x + 35
    canvas.create_oval(ojo_x, 304, ojo_x + 3, 307, fill="#171717", outline="", tags=etiqueta)
    return {"torso": cuerpo, "brazo": brazo, "guante": guante, "pierna": pierna, "bota": bota}


jugador = crear_luchador(player_x, "#20b9d2", "jugador", 1, "nova")
enemigo = crear_luchador(enemy_x, "#e55336", "enemigo", -1, "brasa")
estados_salto = {
    "jugador": {"activo": False, "desplazamiento": 0.0, "velocidad": 0.0, "version": 0},
    "enemigo": {"activo": False, "desplazamiento": 0.0, "velocidad": 0.0, "version": 0},
}
animacion_ataque = {"activa": False, "version": 0, "poses": {}}


def crear_sonido_vocal(nombre, tono_base, duracion):
    frecuencia_muestreo = 22050
    cantidad_muestras = int(frecuencia_muestreo * duracion)
    generador = random.Random(nombre)
    muestras = bytearray()

    for indice in range(cantidad_muestras):
        tiempo = indice / frecuencia_muestreo
        progreso = tiempo / duracion
        tono = tono_base * (1 - 0.24 * progreso) + 8 * math.sin(2 * math.pi * 5 * tiempo)
        fase = 2 * math.pi * tono / frecuencia_muestreo if indice == 0 else fase + 2 * math.pi * tono / frecuencia_muestreo
        voz = 0.0
        for armonico in range(1, 13):
            frecuencia = tono * armonico
            formante_1 = math.exp(-((frecuencia - 550) / 360) ** 2)
            formante_2 = 0.55 * math.exp(-((frecuencia - 1450) / 650) ** 2)
            voz += (formante_1 + formante_2) * math.sin(fase * armonico) / armonico

        envolvente = min(1, progreso * 14) * (1 - progreso) ** 1.8
        voz = (voz + generador.uniform(-0.025, 0.025)) * envolvente * 1.8
        muestra = max(-1, min(1, voz))
        muestras.extend(struct.pack("<h", int(muestra * 32767)))

    ruta = os.path.join(carpeta_sonidos.name, f"{nombre}.wav")
    with wave.open(ruta, "wb") as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(frecuencia_muestreo)
        archivo.writeframes(muestras)
    return ruta


def crear_sonido_impacto(nombre, frecuencia_base, duracion):
    frecuencia_muestreo = 22050
    generador = random.Random(nombre)
    muestras = bytearray()
    for indice in range(int(frecuencia_muestreo * duracion)):
        tiempo = indice / frecuencia_muestreo
        decaimiento = math.exp(-tiempo * 34)
        ruido = generador.uniform(-1, 1) * math.exp(-tiempo * 75)
        tono = math.sin(2 * math.pi * (frecuencia_base - 35 * tiempo) * tiempo) * decaimiento
        muestra = max(-1, min(1, (ruido * 0.7 + tono * 0.8) * (1 - tiempo / duracion)))
        muestras.extend(struct.pack("<h", int(muestra * 32767)))

    ruta = os.path.join(carpeta_sonidos.name, f"{nombre}.wav")
    with wave.open(ruta, "wb") as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(frecuencia_muestreo)
        archivo.writeframes(muestras)
    return ruta


sonidos = {}
carpeta_sonidos = None
if winsound is not None:
    carpeta_sonidos = tempfile.TemporaryDirectory(prefix="mk_sonidos_")
    atexit.register(carpeta_sonidos.cleanup)
    sonidos = {
        "golpe": crear_sonido_vocal("golpe", 145, 0.20),
        "patada": crear_sonido_vocal("patada", 115, 0.24),
        "daño": crear_sonido_vocal("daño", 95, 0.28),
        "salto": crear_sonido_vocal("salto", 185, 0.16),
        "victoria": crear_sonido_vocal("victoria", 175, 0.34),
        "derrota": crear_sonido_vocal("derrota", 85, 0.38),
        "impacto_puno": crear_sonido_impacto("impacto_puno", 165, 0.12),
        "impacto_patada": crear_sonido_impacto("impacto_patada", 85, 0.20),
    }


def reproducir_sonido(nombre):
    if winsound is not None and nombre in sonidos:
        try:
            winsound.PlaySound(sonidos[nombre], winsound.SND_FILENAME | winsound.SND_ASYNC)
            return
        except (OSError, RuntimeError):
            pass
    root.bell()


def actualizar_barras():
    canvas.coords(barra_jugador, 20, 40, 20 + vida_jugador * 2, 60)
    canvas.coords(barra_enemigo, 980 - vida_enemigo * 2, 40, 980, 60)


def mostrar_accion(texto, color):
    canvas.itemconfig(mensaje_accion, text=texto, fill=color)
    root.after(500, lambda: canvas.itemconfig(mensaje_accion, text=""))


def saltar(etiqueta):
    estado = estados_salto[etiqueta]
    if fin_del_juego or estado["activo"] or (etiqueta == "jugador" and animacion_ataque["activa"]):
        return

    estado["activo"] = True
    estado["version"] += 1
    estado["velocidad"] = -11.5
    version = estado["version"]
    reproducir_sonido("salto")

    def animar():
        if estado["version"] != version:
            return
        estado["velocidad"] += 0.75
        nueva_altura = estado["desplazamiento"] + estado["velocidad"]
        if nueva_altura >= 0:
            canvas.move(etiqueta, 0, -estado["desplazamiento"])
            estado["desplazamiento"] = 0
            estado["velocidad"] = 0
            estado["activo"] = False
            return
        canvas.move(etiqueta, 0, nueva_altura - estado["desplazamiento"])
        estado["desplazamiento"] = nueva_altura
        root.after(20, animar)

    animar()


def comprobar_fin():
    global fin_del_juego, temporizador_enemigo
    if vida_jugador <= 0 or vida_enemigo <= 0:
        fin_del_juego = True
        if temporizador_enemigo is not None:
            root.after_cancel(temporizador_enemigo)
            temporizador_enemigo = None
        resultado = "¡NOVA GANA!" if vida_enemigo <= 0 else "¡BRASA GANA!"
        canvas.itemconfig(mensaje, text=f"{resultado}  Pulsa R para reiniciar")
        reproducir_sonido("victoria" if vida_enemigo <= 0 else "derrota")
        return True
    return False


def mover_jugador(cantidad):
    global player_x
    if fin_del_juego or animacion_ataque["activa"]:
        return
    limite_derecho = ANCHO - ANCHO_LUCHADOR
    if cantidad > 0:
        limite_derecho = min(limite_derecho, enemy_x - ANCHO_LUCHADOR)
    nueva_x = max(0, min(limite_derecho, player_x + cantidad))
    canvas.move("jugador", nueva_x - player_x, 0)
    player_x = nueva_x


def izquierda(evento=None):
    mover_jugador(-VELOCIDAD)


def derecha(evento=None):
    mover_jugador(VELOCIDAD)


def animar_ataque(tipo):
    partes = jugador
    ids = (partes["brazo"], partes["guante"]) if tipo == "golpe" else (partes["pierna"], partes["bota"])
    animacion_ataque["version"] += 1
    version = animacion_ataque["version"]
    animacion_ataque["activa"] = True
    animacion_ataque["poses"] = {item: canvas.coords(item) for item in ids}

    if tipo == "golpe":
        brazo = canvas.coords(partes["brazo"])
        brazo[2] += 24
        brazo[4] += 24
        canvas.coords(partes["brazo"], *brazo)
        canvas.move(partes["guante"], 24, 0)
    else:
        pierna = canvas.coords(partes["pierna"])
        pierna[2] += 10
        pierna[3] -= 18
        pierna[4] += 25
        pierna[5] -= 28
        canvas.coords(partes["pierna"], *pierna)
        canvas.move(partes["bota"], 25, -28)

    def recuperar_pose():
        if animacion_ataque["version"] != version:
            return
        for item, pose in animacion_ataque["poses"].items():
            canvas.coords(item, *pose)
        animacion_ataque["poses"] = {}
        animacion_ataque["activa"] = False

    root.after(125, recuperar_pose)


def atacar(danio, alcance):
    global vida_enemigo, ataque_disponible
    if fin_del_juego or not ataque_disponible:
        return
    if estados_salto["jugador"]["desplazamiento"] < -8:
        mostrar_accion("¡NO PUEDES ATACAR EN EL AIRE!", "#ffffff")
        return

    tipo = "golpe" if danio <= 10 else "patada"
    animar_ataque(tipo)
    distancia = enemy_x - (player_x + ANCHO_LUCHADOR)
    if estados_salto["enemigo"]["desplazamiento"] < -8:
        mostrar_accion("¡EL RIVAL ESTÁ EN EL AIRE!", "#ffffff")
    elif 0 <= distancia <= alcance:
        vida_enemigo = max(0, vida_enemigo - danio)
        canvas.itemconfig(enemigo["torso"], fill="#ffffff")
        root.after(120, lambda: canvas.itemconfig(enemigo["torso"], fill="#e55336"))
        impacto = canvas.create_oval(enemy_x - 5, 350, enemy_x + 35, 390, fill="#ffe27a", outline="white", width=2)
        root.after(130, lambda: canvas.delete(impacto))
        mostrar_accion("¡IMPACTO!", "#ffe27a")
        actualizar_barras()
        termino = comprobar_fin()
        if not termino:
            root.after(40, lambda: reproducir_sonido("impacto_puno" if tipo == "golpe" else "impacto_patada"))
    else:
        mostrar_accion("¡FUERA DE ALCANCE!", "#ffffff")

    reproducir_sonido(tipo)
    ataque_disponible = False
    root.after(350, habilitar_ataque)


def habilitar_ataque():
    global ataque_disponible
    ataque_disponible = True


def golpe():
    atacar(10, 70)


def patada():
    atacar(15, 75)


def turno_enemigo():
    global enemy_x, vida_jugador, temporizador_enemigo
    temporizador_enemigo = None
    if fin_del_juego:
        return

    distancia = enemy_x - (player_x + ANCHO_LUCHADOR)
    if distancia > 65:
        avance = min(random.choice((12, 18, 24)), distancia - 55)
        enemy_x -= avance
        canvas.move("enemigo", -avance, 0)
    elif estados_salto["enemigo"]["desplazamiento"] < -8:
        pass
    elif estados_salto["jugador"]["desplazamiento"] < -8:
        mostrar_accion("¡ESQUIVASTE!", "#8ee9ff")
    elif random.random() < 0.12:
        saltar("enemigo")
    elif random.random() < 0.65:
        vida_jugador = max(0, vida_jugador - random.choice((8, 10, 12)))
        reproducir_sonido("impacto_patada")
        root.after(45, lambda: reproducir_sonido("daño"))
        canvas.itemconfig(jugador["torso"], fill="#ffffff")
        root.after(120, lambda: canvas.itemconfig(jugador["torso"], fill="#20b9d2"))
        actualizar_barras()
        comprobar_fin()

    if not fin_del_juego:
        temporizador_enemigo = root.after(random.randint(500, 900), turno_enemigo)


def reiniciar():
    global vida_jugador, vida_enemigo, player_x, enemy_x, fin_del_juego, ataque_disponible, temporizador_enemigo
    if temporizador_enemigo is not None:
        root.after_cancel(temporizador_enemigo)
    animacion_ataque["version"] += 1
    for item, pose in animacion_ataque["poses"].items():
        canvas.coords(item, *pose)
    animacion_ataque["poses"] = {}
    animacion_ataque["activa"] = False
    vida_jugador = 100
    vida_enemigo = 100
    player_x = 150
    enemy_x = 750
    fin_del_juego = False
    ataque_disponible = True
    for etiqueta, estado in estados_salto.items():
        estado["version"] += 1
        if estado["desplazamiento"]:
            canvas.move(etiqueta, 0, -estado["desplazamiento"])
        estado["desplazamiento"] = 0
        estado["activo"] = False
    canvas.move("jugador", player_x - canvas.coords(jugador["torso"])[0] + 30, 0)
    canvas.move("enemigo", enemy_x - canvas.coords(enemigo["torso"])[0] + 30, 0)
    canvas.itemconfig(jugador["torso"], fill="#20b9d2")
    canvas.itemconfig(enemigo["torso"], fill="#e55336")
    canvas.itemconfig(mensaje, text="")
    canvas.itemconfig(mensaje_accion, text="")
    actualizar_barras()
    temporizador_enemigo = root.after(700, turno_enemigo)


def manejar_tecla(evento):
    tecla = evento.keysym.lower()
    acciones = {
        "a": izquierda,
        "left": izquierda,
        "d": derecha,
        "right": derecha,
        "j": golpe,
        "k": patada,
        "space": lambda: saltar("jugador"),
        "up": lambda: saltar("jugador"),
        "r": reiniciar,
    }
    accion = acciones.get(tecla)
    if accion is not None:
        accion()
        return "break"


root.bind_all("<KeyPress>", manejar_tecla)
canvas.focus_set()

actualizar_barras()
temporizador_enemigo = root.after(700, turno_enemigo)
root.mainloop()
