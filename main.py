import tkinter
from tkinter import ttk
from tkinter import messagebox

import youtube_dl.run as execute
import threading as tr
import version

all_formats = []

def format_info_get_parameters(format_info):
    video_f = []
    audio_f = []

    for format in format_info:
        if format['resolution'] == "audio only":
            audio_f.append(f"{format['ext']} - {format['tbr']}k")
        elif "video only" in format['note']:
            video_f.append(f"{format['ext']} - {format['resolution']} - {format['number']} - {format['fps']}fps")

    return video_f, audio_f

def search_video():
    progressbar.step(100)

    try:
        format_info = execute.run(["-F", link_entry.get()])

        global all_formats
        all_formats = format_info
        video_f, audio_f = format_info_get_parameters(format_info)

        video_format_combobox.config(state="readonly", values=video_f)
        video_format_combobox.current(0)
        audio_format_combobox.config(state="readonly", values=audio_f)
        audio_format_combobox.current(0)
        download_button.config(state="normal")

    except:
        messagebox.showwarning(title="Error", message="That is not a valid URL.")

def download():
    progressbar.config(mode="indeterminate")
    progressbar.start()
    link_button.config(state="disabled")
    download_button.config(state="disabled")

    download_thread = tr.Thread(target=download_video)
    download_thread.start()
    messagebox.showwarning(title="Downloading", message="The process has started. Don't close the program.")

def download_video():
    vf = video_format_combobox.get()
    video_f = 0
    for format in all_formats:
        if format['ext'] in vf and format['number'] in vf and str(format['fps']) in vf:
            video_f = format['id']

    af = audio_format_combobox.get()
    audio_f = 0
    for format in all_formats:
        if format['ext'] in af and str(format['tbr']) in af:
            audio_f = format['id']
            
    execute.run(["-f", f"{video_f}+{audio_f}", link_entry.get()])
    progressbar.config(mode="determinate")
    progressbar.stop()
    link_button.config(state="normal")
    download_button.config(state="normal")

    messagebox.showwarning(title="Finished", message="The process has been successful.")


window = tkinter.Tk()
window.title(f"Video Downloader {version.__version__} - by TheNeoDriver")

frame = tkinter.Frame(window)
frame.pack()

link_frame = tkinter.LabelFrame(frame)
link_frame.grid(row= 0, column=0, padx=10, pady=10)

link_label = tkinter.Label(link_frame, text="Enter the link:")
link_label.grid(row=0, column=0)

link_entry = tkinter.Entry(link_frame, width=50)
link_entry.grid(row=0, column=1)

link_button = tkinter.Button(link_frame, text="Search", width=20, command=search_video)
link_button.grid(row=1, column=1)

for widget in link_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)


format_frame = tkinter.LabelFrame(frame)
format_frame.grid(row= 1, column=0, padx=20, pady=10)

video_format_label = tkinter.Label(format_frame, text="Select video format:")
video_format_label.grid(row=0, column=0)

video_format_combobox = ttk.Combobox(
        format_frame,
        values=[],
        width=41,
        state="disabled"
    )
video_format_combobox.grid(row=0, column=1)

audio_format_label = tkinter.Label(format_frame, text="Select audio format:")
audio_format_label.grid(row=1, column=0)

audio_format_combobox = ttk.Combobox(
        format_frame,
        values=[],
        width=41,
        state="disabled"
    )
audio_format_combobox.grid(row=1, column=1)

for widget in format_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)


download_button = tkinter.Button(frame, text="Download", width=20, state="disabled", command=download)
download_button.grid(row=2, column=0, pady=10)

progressbar = ttk.Progressbar(frame, length=300)
progressbar.grid(row=3, column=0, pady=10)

if __name__ == '__main__':
    window.mainloop()