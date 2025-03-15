import pygame
import os
import tkinter as tk
from pynput import keyboard

pygame.mixer.init()


MUSIC_FOLDER = "eminem"


if not os.path.exists(MUSIC_FOLDER):
    print(f"Ошибка: Папка '{MUSIC_FOLDER}' не найдена!")
    exit()

playlist = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]
if not playlist:
    print(f"Ошибка: В папке '{MUSIC_FOLDER}' нет файлов .mp3")
    exit()

current_track = 0
playing = False

def play_music():
    """Воспроизведение текущего трека"""
    global playing
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, playlist[current_track]))
    pygame.mixer.music.play()
    playing = True
    update_label()

def stop_music():
    """Остановка музыки"""
    global playing
    pygame.mixer.music.stop()
    playing = False
    update_label()

def next_track():
    """Переключение на следующий трек"""
    global current_track
    current_track = (current_track + 1) % len(playlist)
    play_music()

def previous_track():
    """Переключение на предыдущий трек"""
    global current_track
    current_track = (current_track - 1) % len(playlist)
    play_music()

def toggle_play():
    """Пауза / Возобновление"""
    global playing
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        playing = False
    else:
        pygame.mixer.music.unpause()
        playing = True
    update_label()


def update_label():
    song_label.config(text=f" Now Playing: {playlist[current_track]}" if playing else "⏸ Paused")

root = tk.Tk()
root.title("Музыкальный Плеер")
root.geometry("400x300")
root.resizable(False, False)


song_label = tk.Label(root, text=" Now Playing: ", font=("Arial", 12))
song_label.pack(pady=10)

btn_play = tk.Button(root, text="▶ Play/Pause", command=toggle_play, width=15, height=2)
btn_stop = tk.Button(root, text="⏹ Stop", command=stop_music, width=15, height=2)
btn_prev = tk.Button(root, text="⏮ Previous", command=previous_track, width=15, height=2)
btn_next = tk.Button(root, text="⏭ Next", command=next_track, width=15, height=2)


btn_play.pack(pady=5)
btn_stop.pack(pady=5)
btn_prev.pack(pady=5)
btn_next.pack(pady=5)


play_music()


def on_press(key):
    try:
        if key == keyboard.Key.space:
            toggle_play()
        elif key == keyboard.Key.right:
            next_track()
        elif key == keyboard.Key.left:
            previous_track()
        elif key.char == "s":
            stop_music()
    except AttributeError:
        pass


print(" Управление плеером:")
print("[Space] - Play/Pause | [S] - Stop | [→] - Next | [←] - Previous")

with keyboard.Listener(on_press=on_press) as listener:
    root.mainloop()  
    listener.join()
