from tkinter import Tk
from tkinter import *
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from xml.sax import SAXNotSupportedException
import pygame
from turtle import back, bgcolor
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import random
from random import choice


##################
# Welcome to BubbleGum Music PLAYER
# I have updated this version to make the app play the next song when the current has reached its lenght. Line 86
# Please run cd
# cd /Users/ceciliagebhard/Documents/Mp3playerapp
# cd mp3
# source virt/bin/activate
# RUN writing: python3.9 player.py
# ENJOY!

###################
# MODULO

#Initialize Pygame
pygame.mixer.init()



# funcion askcolor
def funcionaskcolor():
    resultado = askcolor(color="#6666E6", title="El título")
    print(resultado)
    colorseleccion.append(resultado[1])
    for opcion in colorseleccion:
        root.config(bg=opcion)

# funcion reset color
def funcionresetcolor():
    obtain = root.config(bg="#FFB5C5")
    
def funcionbgsorpresa():
            hex_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
            color_code = '#'
            color_code = color_code + choice(hex_chars)
            color_code = color_code + choice(hex_chars)
            color_code = color_code + choice(hex_chars)
            color_code = color_code + choice(hex_chars)
            color_code = color_code + choice(hex_chars)
            color_code = color_code + choice(hex_chars)
            print('El color hexagecimal generado es:', color_code)
            root.config(bg=color_code)
    
# Create a Function to Deal with Time
def play_time():
    # Check to see if song is Stopped
    if stopped:
        return
    else:
        # Grab current song time
        current_time = pygame.mixer.music.get_pos() / 1000
        # Convert Song Time to Time Format
        converted__current_time = time.strftime('%M:%S', time.gmtime(current_time))
    
        # reconstruct song with directory structure stuff
        song = playlist_box.get(ACTIVE)
        song = f'/Users/ceciliagebhard/Documents/Mp3playerapp/mp3/audio/{song}.mp3'
        # Find current song lenght
        song_mut = MP3(song)
        global song_length
        song_length = song_mut.info.length
        # Convert to time format
        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    
        # set slider to song length (UPDATE:NOT ANYMORE)
        # song_slider.config(to=song_length)
        # my_label.config(text=song_slider.get())
    
    # Check to see if song is over
    if int(song_slider.get()) == int(song_length):
        #stop()
        # Exception that automatically plays the next song in the playlist when the current one is over
        try:
            next_song()
        # this exception catches the Tuple Index Error that is generated when there isn't a next song
        except IndexError as e:
            print("---: ", e)      
            stop()      
    elif paused:
        # Check to see if paused, if so - pass
        pass
    else:
        # Move Slider Along 1 Second at a Time
        next_time = int(song_slider.get()) + 1
        # Output new time value to slider and to lenght of song
        song_slider.config(to=song_length, value=next_time)
        # Convert Slider position to time format
        converted__current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))
        # Output slider
        status_bar.config(text=f'Time Elapsed: {converted__current_time} of {converted_song_length}', bd=1, background="#771d71")
    
    # Add Current Time of Song Length to Status Bar
    if current_time > 0.2:
        status_bar.config(text=f'Time Elapsed: {converted__current_time} of {converted_song_length}', bd=1,background="#771d71")
    # Create Loop to Check the Time Every Second
    status_bar.after(1000, play_time)



# funcion add song
def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3" ), ))
    # Strip out directory structure and .mp3 from song title
    song = song.replace("/Users/ceciliagebhard/Documents/Mp3playerapp/mp3/audio/", "")
    song = song.replace(".mp3", "")
    # Add To End Of Playlist
    my_label.config(text=song + "" + "--> Added To Playlist", fg="#CD2990", bg="#54FF9F")
    playlist_box.insert(END, song)

#funcion add many songs
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3" ), ))
    # Loop thru songlist and replace directory structure and .mp3 from song name
    for song in songs:
        # Strip out directory structure and .mp3 from song title
        song = song.replace("/Users/ceciliagebhard/Documents/Mp3playerapp/mp3/audio/", "")
        song = song.replace(".mp3", "")
        # Add To End Of Playlist
        my_label.config(text="All Selected Songs Had Been Added To Playlist", fg="#CD2990", bg="#54FF9F")
        playlist_box.insert(END, song)

#funcion delete song
def delete_song():
    #deletes higlighted song from playlist
    playlist_box.delete(ANCHOR)

#funcion delete all songs
def delete_all_songs():
    #deletes all songs
    playlist_box.delete(0, END)

#funcion PLAY
def play():
    # Set stopped to False since a song is now playing
    global stopped
    stopped = False 
    # reconstruct song with directory structure stuff
    song = playlist_box.get(ACTIVE)
    song = f'/Users/ceciliagebhard/Documents/Mp3playerapp/mp3/audio/{song}.mp3'
    
    #Load song with pygame mixer
    pygame.mixer.music.load(song)
    #Play song with pygame mixer
    pygame.mixer.music.play(loops=0)
    my_label.config(text=song + "" + "--> Playing", fg="#CD2990", bg="#54FF9F")
    playlist_box.insert(END, song)
    
    # Get Song Time
    play_time()

# Create Stop Variable
global stopped 
stopped = False

#funcion STOP
def stop():
    # Stop the song
    pygame.mixer.music.stop()
    # Clear Playlist Bar
    playlist_box.selection_clear(ACTIVE)
    
    status_bar.config(text='', background="#771d71")
    # Set slider to Zero
    song_slider.config(value=0)
    # Set Stop Variable to True
    global stopped 
    stopped = True


# Create paused variable
global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused
    if paused: 
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True

# Function for next song / forward button
def next_song():
    # Reset slider position and status bar
    status_bar.config(text='')
    song_slider.config(value=0)
    # Get current song number
    next_one = playlist_box.curselection()
    # add one to the current song tuple/list
    next_one = next_one[0] + 1
    # grab the song title from the playlist
    song = playlist_box.get(next_one)
    # Add directory structure stuff to the song title
    song = f'/Users/ceciliagebhard/Documents/Mp3playerapp/mp3/audio/{song}.mp3'
    #Load song with pygame mixer
    pygame.mixer.music.load(song)
    #Play song with pygame mixer
    pygame.mixer.music.play(loops=0)
    my_label.config(text=song + "" + "--> Playing", fg="#CD2990", bg="#54FF9F")
    playlist_box.insert(END, song)
    #Clear Active Bar in Playlist
    playlist_box.selection_clear(0, END)
    # Move Active Bard to Next Song
    playlist_box.activate(next_one)
    # Set Active Bar to Next Song
    playlist_box.selection_set(next_one, last=None)
    

# Create Function to previous song
def previous_song():
    # Reset slider position and status bar
    status_bar.config(text='')
    song_slider.config(value=0)
    # Get current song number
    previous_one = playlist_box.curselection()
    # add one to the current song tuple/list
    previous_one = previous_one[0] - 1
    # grab the song title from the playlist
    song = playlist_box.get(previous_one)
    # Add directory structure stuff to the song title
    song = f'/Users/ceciliagebhard/Documents/Mp3playerapp/mp3/audio/{song}.mp3'
    #Load song with pygame mixer
    pygame.mixer.music.load(song)
    #Play song with pygame mixer
    pygame.mixer.music.play(loops=0)
    my_label.config(text=song + "" + "--> Playing", fg="#CD2990", bg="#54FF9F")
    playlist_box.insert(END, song)
    #Clear Active Bar in Playlist
    playlist_box.selection_clear(0, END)
    # Move Active Bard to Next Song
    playlist_box.activate(previous_one)
    # Set Active Bar to Next Song
    playlist_box.selection_set(previous_one, last=None)

# Create a volume slider
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())    
    
# Create a song slider
def slide(x):
    # reconstruct song with directory structure stuff
    song = playlist_box.get(ACTIVE)
    song = f'/Users/ceciliagebhard/Documents/Mp3playerapp/mp3/audio/{song}.mp3'
    
    #Load song with pygame mixer
    pygame.mixer.music.load(song)
    #Play song with pygame mixer
    pygame.mixer.music.play(loops=0, start=song_slider.get())

###################
# VISTA

# Ventana Principal
root = Tk()

root.title("BubbleGum Player ʕ•ᴥ•ʔ")
root.config(bg="#FFB5C5")
# color v1 #8B4789
# color bg v1 #FFE1FF
root.geometry("1500x800")

# Main frame
main_frame = Frame(root, bg="#771d71")
main_frame.pack(pady=20)

# Creates Playlist Box
playlist_box = Listbox(main_frame, bg="#54FF9F", fg="#CD2990", width=90, selectbackground="#771d71", selectforeground="#54FF9F")
# bg v1 #98FB98
playlist_box.grid(row=0, column=0)

# Create Volume Slider Frame
volume_frame = LabelFrame(main_frame, text="VOLUME", bg="#FFB5C5")
volume_frame.grid(row=0, column=1, pady=5)

# Create Volume Slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, length=140, value=1, command=volume)
volume_slider.pack(pady=5,padx=25)

# Create Song Slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=820, value=0, command=slide)
song_slider.grid(row=2, column=0, pady=20)

# Define Button Images for Control
back_btn_img = PhotoImage(file='images/backward_black_small.png')
forward_btn_img = PhotoImage(file='images/forward_black_small.png')
play_btn_img = PhotoImage(file='images/play_black_small.png')
pause_btn_img = PhotoImage(file='images/pause_black_small.png')
stop_btn_img = PhotoImage(file='images/stop_black_small.png')

# Create Button Frame
control_frame = Frame(main_frame, bg="#771d71")
control_frame.grid(row=1, column=0, pady=50, padx=10)

# Create Play/Stop etc Buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=2, command=previous_song)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=2, command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=2, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=2, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=2, command= stop)
boton_c = Button(control_frame, text="Elige tu propio color de fondo a gusto... ύ.ὺ", foreground="black", background="pink", command=funcionaskcolor)
boton_r = Button(control_frame, text="Restaurar Background original", foreground="black", background="pink", command=funcionresetcolor)
boton_s = Button(control_frame, text="Background Sorpresa", foreground="black", background="pink", command=funcionbgsorpresa)


back_button.grid(row=1, column=0, padx=1, pady=10)
play_button.grid(row=1, column=1, padx=50, pady=10)
pause_button.grid(row=1, column=2, padx=0, pady=10)
stop_button.grid(row=1, column=3, padx=50, pady=10)
forward_button.grid(row=1, column=4, padx=1, pady=10)
boton_c.grid(row=2, column=2, pady=20)
boton_r.grid(row=3, column=2, pady=20)
boton_s.grid(row=4, column=2, pady=20)


# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create Add Song Menu Dropdowns
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs...", menu=add_song_menu)
# Add One Song To Playlist
add_song_menu.add_command(label="Add One Song To Playlist...", command=add_song)
# Add Many Songs To Playlist
add_song_menu.add_command(label="Add Many Songs To Playlist...", command=add_many_songs)

# Create Delete Song Menu Drodowns
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu) 
remove_song_menu.add_command(label="Remove Selected Song From Playlist...", command=delete_song) 
remove_song_menu.add_command(label="Remove All Songs From Playlist...", command=delete_all_songs) 

# Create Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E, background="#771d71")
status_bar.place(relx=0.3, rely=0.3, anchor=S)
#status_bar.pack(fill=X, side=BOTTOM, ipady=2)


    
poemselection = [
    "Nunca rompas el silencio si no es para mejorarlo", 
    "Mi canto es una cadena sin comienzo ni final y en cada eslabón se encuentra el canto de los demás",
    "Mi audacia está en la armonía, en los ritmos, en los contratiempos, en el contrapunto de dos o tres instrumentos, que es hermoso y buscar que no siempre sea tonal, buscar la atonalidad",
    "La mente humana es fantástica e infinita. La perseverancia es fundamental. El que innova nunca debe dejar de hacerlo"
    ]

poema = random.choice(poemselection)

# Temporary Label
#"Welcome to the bubblegum player..."
my_label = Label(root, text=poema, font=("Helvetica, 14"), fg="#CD2990", bd=1, bg="#54FF9F")
my_label.pack(pady=20) 
    
colorseleccion = [] 

root.mainloop()
