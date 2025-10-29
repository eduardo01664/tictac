# Tic Tac Toe con IA

Juego de Tic Tac Toe (Tres en Raya) con inteligencia artificial basada en reglas lógicas.

## Requisitos

- Python 3.12.1
- tkinter (incluido con Python)
- pygame

## Instalación

1. Instalar pygame:
```bash
pip install pygame
```

## Configuración de Audio

Para agregar música de fondo, crea una carpeta `audio` en el mismo directorio del juego y coloca tus archivos de música:

```
tictac/
├── tictactoe.py
├── audio/
│   ├── menu_music.mp3    # Música para el menú
│   └── game_music.mp3    # Música durante el juego
```

Puedes modificar las rutas en el código (líneas 15-16 de tictactoe.py):
```python
self.menu_music_path = "audio/menu_music.mp3"
self.game_music_path = "audio/game_music.mp3"
```

Si no tienes archivos de audio, el juego funcionará sin música.

## Ejecutar el juego

```bash
python tictactoe.py
```

## Reglas de la IA

La IA implementa las siguientes reglas lógicas:

- **R1**: Si el centro está libre, tomar el centro
- **R2**: Si hay dos símbolos iguales en una fila y una casilla vacía, completar para ganar o bloquear
- **R3**: Si una esquina está libre y no hay jugada clara, tomar una esquina
- **R4**: Si el oponente puede ganar en el siguiente turno, bloquear

## Cómo jugar

1. Haz clic en "Iniciar Juego" en el menú principal
2. Tú juegas con **X** (azul) y la IA con **O** (rojo)
3. Haz clic en una casilla vacía para hacer tu movimiento
4. El primero en conseguir 3 símbolos en línea (horizontal, vertical o diagonal) gana
5. Si se llena el tablero sin ganador, es empate

## Características

- Interfaz gráfica intuitiva
- IA con estrategia basada en reglas lógicas
- Soporte para música de fondo
- Menú principal
- Detección automática de victoria y empate
