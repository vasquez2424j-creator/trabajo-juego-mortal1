# Ring Nine — Duelo Arcade

Proyecto de videojuego de combate entre **Nova** y **Brasa**. Incluye dos versiones independientes:

- **`juego_3d.html`**: versión 3D para navegador, desarrollada con Three.js.
- **`juego.py`**: versión 2D para escritorio, desarrollada con Python y Tkinter.

## Requisitos

### Versión 3D (navegador)
- Un navegador moderno con soporte para WebGL.
- Conexión a internet para cargar Three.js desde CDN y las fuentes externas.
- No necesita instalar Python.

### Versión 2D (Python)
- Python 3 instalado.
- Tkinter, que normalmente viene incluido en la instalación de Python para Windows.
- No requiere instalar paquetes con `pip`.

## Cómo ejecutar

### Abrir el juego 3D
1. Descarga `juego_3d.html`.
2. Ábrelo con Chrome, Edge o Firefox.
3. Si no carga la arena, revisa la conexión a internet y que WebGL esté habilitado.

También puedes publicarlo con **GitHub Pages**: en el repositorio, entra en **Settings → Pages**, selecciona la rama principal y la carpeta raíz. Luego guarda los cambios y abre la URL publicada que GitHub te indique.

### Ejecutar el juego 2D en Windows
1. Instala Python 3 si todavía no lo tienes.
2. Abre PowerShell o la terminal en la carpeta del proyecto.
3. Ejecuta:

   ```powershell
   python juego.py
   ```

   Si el comando `python` no funciona, prueba:

   ```powershell
   py juego.py
   ```

## Controles

### Juego 3D
- **W / A / S / D** o flechas: moverse.
- **J**: puño.
- **K**: patada.
- **Espacio**: saltar.
- **L**: ataque especial cuando la barra de energía esté llena.
- Botones en pantalla: reiniciar y activar/desactivar sonido.

### Juego 2D
- **A / D** o flechas izquierda/derecha: moverse.
- **J**: puño.
- **K**: patada.
- **Espacio** o flecha arriba: saltar.
- **R**: reiniciar combate.

## Estructura

```text
ring-nine-github/
├── juego_3d.html
├── juego.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Publicar en GitHub

1. Entra en https://github.com/ e inicia sesión.
2. Pulsa **New repository** y crea un repositorio, por ejemplo `ring-nine-duelo-arcade`.
3. En la página del repositorio, selecciona **Add file → Upload files**.
4. Sube los archivos de esta carpeta y pulsa **Commit changes**.

## Notas

- Los dos archivos son versiones distintas del juego; ejecútalos por separado.
- El archivo HTML usa Three.js desde un CDN, por lo que necesita conexión a internet para descargar esa biblioteca.
- Este proyecto es un prototipo arcade educativo y no pretende reproducir exactamente un juego comercial.
