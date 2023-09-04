import io
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import tempfile
import os
import uuid
import time
from elevenlabs import generate, play, set_api_key

# Setting the API key
set_api_key("ENTERAPI")

def generate_audio():
    input_text = text_box.get(1.0, tk.END)
    paragraphs = input_text.split('\n\n')
    output_audio = AudioSegment.empty()

    for index, paragraph in enumerate(paragraphs):
        if len(paragraph.strip()) > 0:
            print(f"Generating audio for paragraph {index + 1} of {len(paragraphs)}...")
            countdown.set(f"Paragraphs remaining: {len(paragraphs) - index - 1}")
            audio_bytes = generate(text=paragraph, voice="Bella", model="eleven_monolingual_v1")
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format='mp3')
            output_audio += audio_segment

    save_path = filedialog.asksaveasfilename(defaultextension='.mp3')
    output_audio.export(save_path, format='mp3')

def update_char_count(*args):
    char_count.set(f"Character count: {len(text_box.get(1.0, tk.END)) - 1}")

def exit_app():
    root.destroy()

# Retro style configuration
retro_bg = "#0c0c0c"
retro_fg = "#33ff33"
retro_font = "Courier 14"
retro_button_color = "#1d1d1d"
retro_button_fg = "#33ff33"

root = tk.Tk()
root.title("ElevenLabs TTS")
root.geometry("600x400")
root.resizable(True, True)
root.minsize(1000, 800)
root.configure(bg=retro_bg)

frame1 = tk.Frame(root, bg=retro_bg)
frame1.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

text_box = tk.Text(frame1, wrap=tk.WORD, bg=retro_bg, fg=retro_fg, font=retro_font, insertbackground=retro_fg, selectbackground="#505050", selectforeground=retro_fg)
text_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
text_box.bind("<KeyRelease>", update_char_count)

scrollbar = tk.Scrollbar(frame1, command=text_box.yview, bg=retro_bg)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_box.config(yscrollcommand=scrollbar.set)

char_count = tk.StringVar()
char_count_label = tk.Label(root, textvariable=char_count, bg=retro_bg, fg=retro_fg, font=retro_font)
char_count_label.pack(pady=5)
update_char_count()

countdown = tk.StringVar()
countdown_label = tk.Label(root, textvariable=countdown, bg=retro_bg, fg=retro_fg, font=retro_font)
countdown_label.pack(pady=5)

generate_button = tk.Button(root, text="Generate Audio", command=generate_audio, bg=retro_button_color, fg=retro_button_fg, font=retro_font, relief=tk.FLAT, activebackground="#2a2a2a", activeforeground=retro_button_fg)
generate_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_app, bg=retro_button_color, fg=retro_button_fg, font=retro_font, relief=tk.FLAT, activebackground="#2a2a2a", activeforeground=retro_button_fg)
exit_button.pack(pady=10)

root.mainloop()
