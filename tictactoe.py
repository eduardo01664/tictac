import tkinter as tk
from tkinter import messagebox
import pygame
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.geometry("400x500")
        self.window.resizable(False, False)

        # Inicializar pygame para el audio
        pygame.mixer.init()

        # Rutas de audio (modificar estas rutas según tus archivos)
        self.menu_music_path = "musica\menu.mp3"  # Ruta relativa para música del menú
        self.game_music_path = "musica\juego.mp3"  # Ruta relativa para música del juego

        # Variables del juego
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # El jugador humano es X
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_frame = None

        self.show_menu()

    def play_music(self, music_path):
        """Reproduce música de fondo"""
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # -1 para loop infinito
        except:
            pass  # Si no encuentra el archivo, continúa sin música

    def stop_music(self):
        """Detiene la música"""
        pygame.mixer.music.stop()

    def show_menu(self):
        """Muestra el menú principal"""
        # Limpiar ventana
        for widget in self.window.winfo_children():
            widget.destroy()

        # Reproducir música del menú
        self.play_music(self.menu_music_path)

        # Frame del menú
        menu_frame = tk.Frame(self.window, bg="#2C3E50")
        menu_frame.pack(fill="both", expand=True)

        # Título
        title_label = tk.Label(
            menu_frame,
            text="TIC TAC TOE",
            font=("Arial", 36, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        title_label.pack(pady=80)

        # Botón de iniciar juego
        start_button = tk.Button(
            menu_frame,
            text="Iniciar Juego",
            font=("Arial", 20),
            bg="#27AE60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            width=15,
            height=2,
            command=self.start_game
        )
        start_button.pack(pady=20)

        # Botón de salir
        exit_button = tk.Button(
            menu_frame,
            text="Salir",
            font=("Arial", 16),
            bg="#E74C3C",
            fg="white",
            activebackground="#C0392B",
            activeforeground="white",
            width=15,
            command=self.window.quit
        )
        exit_button.pack(pady=10)

    def start_game(self):
        """Inicia el juego"""
        # Limpiar ventana
        for widget in self.window.winfo_children():
            widget.destroy()

        # Cambiar música a la del juego
        self.play_music(self.game_music_path)

        # Reiniciar el tablero
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

        # Frame del juego
        self.game_frame = tk.Frame(self.window, bg="#34495E")
        self.game_frame.pack(fill="both", expand=True)

        # Título del juego
        title = tk.Label(
            self.game_frame,
            text="Tic Tac Toe",
            font=("Arial", 24, "bold"),
            bg="#34495E",
            fg="white"
        )
        title.pack(pady=10)

        # Frame del tablero
        board_frame = tk.Frame(self.game_frame, bg="#34495E")
        board_frame.pack(pady=20)

        # Crear botones del tablero
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    board_frame,
                    text='',
                    font=("Arial", 32, "bold"),
                    width=4,
                    height=2,
                    bg="white",
                    fg="black",
                    command=lambda row=i, col=j: self.player_move(row, col)
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = button

        # Botón de volver al menú
        menu_button = tk.Button(
            self.game_frame,
            text="Volver al Menú",
            font=("Arial", 14),
            bg="#95A5A6",
            fg="white",
            command=self.show_menu
        )
        menu_button.pack(pady=10)

    def player_move(self, row, col):
        """Maneja el movimiento del jugador"""
        if self.board[row][col] == '' and self.current_player == 'X':
            self.board[row][col] = 'X'
            self.buttons[row][col].config(text='X', fg="#3498DB", state="disabled")

            # Verificar victoria o empate
            if self.check_winner('X'):
                messagebox.showinfo("Juego terminado", "¡Ganaste!")
                self.show_menu()
                return

            if self.is_draw():
                messagebox.showinfo("Juego terminado", "¡Empate!")
                self.show_menu()
                return

            # Turno de la IA
            self.current_player = 'O'
            self.window.after(500, self.ai_move)  # Delay de 500ms para que sea más natural

    def ai_move(self):
        """Implementa la lógica de la IA basada en las reglas del gato"""
        move = self.get_ai_move()

        if move:
            row, col = move
            self.board[row][col] = 'O'
            self.buttons[row][col].config(text='O', fg="#E74C3C", state="disabled")

            # Verificar victoria o empate
            if self.check_winner('O'):
                messagebox.showinfo("Juego terminado", "¡La IA ganó!")
                self.show_menu()
                return

            if self.is_draw():
                messagebox.showinfo("Juego terminado", "¡Empate!")
                self.show_menu()
                return

            self.current_player = 'X'

    def get_ai_move(self):
        """Determina el mejor movimiento de la IA según las reglas"""
        # R1: Si el centro está libre, tomar el centro
        if self.board[1][1] == '':
            return (1, 1)

        # R2: Si hay dos símbolos iguales en una fila (diagonal, vertical u horizontal)
        # y una casilla vacía, entonces colocar en la vacía para ganar o bloquear

        # Primero intentar ganar (completar línea de O)
        win_move = self.find_two_in_line('O')
        if win_move:
            return win_move

        # R4: Bloquear si el oponente puede ganar en el siguiente turno
        block_move = self.find_two_in_line('X')
        if block_move:
            return block_move

        # R3: Si una esquina está libre y no hay jugada clara, tomar una esquina
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        empty_corners = [(r, c) for r, c in corners if self.board[r][c] == '']
        if empty_corners:
            return random.choice(empty_corners)

        # Si no hay esquinas, tomar cualquier casilla libre
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    return (i, j)

        return None

    def find_two_in_line(self, player):
        """
        Encuentra una línea con 2 símbolos del jugador y una casilla vacía
        Retorna la posición de la casilla vacía
        """
        # Verificar filas
        for i in range(3):
            row = [self.board[i][j] for j in range(3)]
            if row.count(player) == 2 and row.count('') == 1:
                j = row.index('')
                return (i, j)

        # Verificar columnas
        for j in range(3):
            col = [self.board[i][j] for i in range(3)]
            if col.count(player) == 2 and col.count('') == 1:
                i = col.index('')
                return (i, j)

        # Verificar diagonal principal
        diag1 = [self.board[i][i] for i in range(3)]
        if diag1.count(player) == 2 and diag1.count('') == 1:
            i = diag1.index('')
            return (i, i)

        # Verificar diagonal secundaria
        diag2 = [self.board[i][2-i] for i in range(3)]
        if diag2.count(player) == 2 and diag2.count('') == 1:
            i = diag2.index('')
            return (i, 2-i)

        return None

    def check_winner(self, player):
        """Verifica si hay un ganador (T4)"""
        # Verificar filas
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True

        # Verificar columnas
        for j in range(3):
            if all(self.board[i][j] == player for i in range(3)):
                return True

        # Verificar diagonal principal
        if all(self.board[i][i] == player for i in range(3)):
            return True

        # Verificar diagonal secundaria
        if all(self.board[i][2-i] == player for i in range(3)):
            return True

        return False

    def is_draw(self):
        """Verifica si hay empate (T5)"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    return False
        return True

    def run(self):
        """Ejecuta la aplicación"""
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
