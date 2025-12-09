import os
import tkinter as tk
from tkinter import (
    PhotoImage,
    ttk,
    Label,
    Entry,
    Button,
    OptionMenu,
    StringVar,
    DoubleVar,
    filedialog,
    messagebox,
    Frame,
)
from download import download_single_video_threaded, download_playlist_threaded
from utils.utils import select_save_directory, load_last_directory, show_error_message

# Modern color scheme
COLORS = {
    'bg': '#f5f5f5',           # Light gray background
    'fg': '#2c3e50',           # Dark blue-gray text
    'primary': '#3498db',      # Bright blue
    'primary_hover': '#2980b9', # Darker blue
    'success': '#2ecc71',      # Green
    'danger': '#e74c3c',       # Red
    'secondary': '#95a5a6',    # Gray
    'accent': '#9b59b6',       # Purple
    'text_bg': '#ffffff',      # White
    'border': '#bdc3c7',       # Light gray border
}


def setup_gui():
    """
    Sets up the GUI for the YouTube Downloader application with modern styling.
    """
    # Initialize main window
    window = tk.Tk()
    window.title("🎥 YouTube Downloader v2.3")
    window.geometry("900x650")
    window.configure(bg=COLORS['bg'])
    window.resizable(True, True)

    # Set the window icon
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "icon", "logo.ico")
    try:
        window.iconbitmap(icon_path)
    except:
        pass  # Icon not available, continue without it

    # Configure ttk style for modern look
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure notebook style
    style.configure('TNotebook', background=COLORS['bg'], borderwidth=0)
    style.configure('TNotebook.Tab', 
                    background=COLORS['secondary'], 
                    foreground=COLORS['fg'],
                    padding=[20, 10],
                    font=('Segoe UI', 10, 'bold'))
    style.map('TNotebook.Tab', 
              background=[('selected', COLORS['primary'])],
              foreground=[('selected', 'white')])
    
    # Configure frame style
    style.configure('TFrame', background=COLORS['bg'])
    
    # Configure progressbar style
    style.configure('TProgressbar', 
                    thickness=25,
                    troughcolor=COLORS['border'],
                    background=COLORS['success'])

    # Header frame with title
    header_frame = Frame(window, bg=COLORS['primary'], height=80)
    header_frame.pack(fill=tk.X, side=tk.TOP)
    
    title_label = Label(header_frame, 
                       text="YouTube Downloader",
                       font=('Segoe UI', 24, 'bold'),
                       bg=COLORS['primary'],
                       fg='white')
    title_label.pack(pady=20)
    
    subtitle_label = Label(header_frame,
                          text="Download YouTube videos and playlists with ease",
                          font=('Segoe UI', 10),
                          bg=COLORS['primary'],
                          fg='white')
    subtitle_label.pack()

    # Main content frame
    content_frame = Frame(window, bg=COLORS['bg'])
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Progress section
    progress_frame = Frame(content_frame, bg=COLORS['bg'])
    progress_frame.pack(fill=tk.X, pady=(0, 10))
    
    progress_var = DoubleVar()
    progress_label = Label(progress_frame, 
                          text="Ready to download",
                          font=('Segoe UI', 11, 'bold'),
                          bg=COLORS['bg'],
                          fg=COLORS['fg'])
    progress_label.pack(pady=(0, 5))

    progress_bar = ttk.Progressbar(
        progress_frame, 
        length=500, 
        mode="determinate", 
        variable=progress_var,
        style='TProgressbar'
    )
    progress_bar.pack(fill=tk.X, pady=(0, 10))

    # Text area for system messages with modern styling
    text_frame = Frame(content_frame, bg=COLORS['bg'])
    text_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 10))
    
    text_label = Label(text_frame,
                      text="📋 Activity Log",
                      font=('Segoe UI', 10, 'bold'),
                      bg=COLORS['bg'],
                      fg=COLORS['fg'])
    text_label.pack(anchor='w', pady=(0, 5))
    
    text_area = tk.Text(text_frame, 
                       wrap=tk.WORD, 
                       state=tk.DISABLED, 
                       height=8, 
                       width=80,
                       bg=COLORS['text_bg'],
                       fg=COLORS['fg'],
                       font=('Consolas', 9),
                       relief=tk.FLAT,
                       borderwidth=1,
                       highlightthickness=1,
                       highlightbackground=COLORS['border'],
                       padx=10,
                       pady=10)
    text_area.pack(fill=tk.BOTH, expand=True)

    # Create a notebook to separate Single Video and Playlist tabs
    notebook = ttk.Notebook(content_frame, style='TNotebook')
    notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    # --- Single Video Download Tab ---
    single_tab = ttk.Frame(notebook, style='TFrame')
    notebook.add(single_tab, text="📹 Single Video")

    # Configure grid weights for better resizing
    single_tab.columnconfigure(1, weight=1)

    # Single video input fields with better styling
    Label(single_tab, 
          text="YouTube URL:",
          font=('Segoe UI', 10, 'bold'),
          bg=COLORS['bg'],
          fg=COLORS['fg']).grid(
        row=0, column=0, padx=15, pady=15, sticky="w"
    )
    link_entry = Entry(single_tab, 
                      width=50,
                      font=('Segoe UI', 10),
                      relief=tk.FLAT,
                      borderwidth=2,
                      highlightthickness=1,
                      highlightbackground=COLORS['border'])
    link_entry.grid(row=0, column=1, padx=15, pady=15, sticky="ew", columnspan=2)

    Label(single_tab, 
          text="Download Type:",
          font=('Segoe UI', 10, 'bold'),
          bg=COLORS['bg'],
          fg=COLORS['fg']).grid(
        row=1, column=0, padx=15, pady=15, sticky="w"
    )
    download_type_var = StringVar(single_tab)
    download_type_var.set("MP4")
    download_type_menu = OptionMenu(single_tab, download_type_var, "MP4", "MP3")
    download_type_menu.config(font=('Segoe UI', 10),
                             bg='white',
                             fg=COLORS['fg'],
                             relief=tk.FLAT,
                             highlightthickness=1,
                             highlightbackground=COLORS['border'],
                             activebackground=COLORS['primary'],
                             activeforeground='white')
    download_type_menu.grid(row=1, column=1, padx=15, pady=15, sticky="w")

    Label(single_tab, 
          text="Save Directory:",
          font=('Segoe UI', 10, 'bold'),
          bg=COLORS['bg'],
          fg=COLORS['fg']).grid(
        row=2, column=0, padx=15, pady=15, sticky="w"
    )
    save_directory_entry = Entry(single_tab, 
                                 width=50,
                                 font=('Segoe UI', 10),
                                 relief=tk.FLAT,
                                 borderwidth=2,
                                 highlightthickness=1,
                                 highlightbackground=COLORS['border'])
    save_directory_entry.grid(row=2, column=1, padx=15, pady=15, sticky="ew")

    select_directory_button = Button(
        single_tab,
        text="📁 Browse",
        font=('Segoe UI', 10, 'bold'),
        bg=COLORS['secondary'],
        fg='white',
        relief=tk.FLAT,
        padx=20,
        pady=8,
        cursor='hand2',
        command=lambda: select_save_directory(
            save_directory_entry, load_last_directory()
        ),
    )
    select_directory_button.grid(row=2, column=2, padx=15, pady=15, sticky="w")
    
    # Add hover effect
    def on_enter_browse(e):
        e.widget.config(bg=COLORS['fg'])
    def on_leave_browse(e):
        e.widget.config(bg=COLORS['secondary'])
    select_directory_button.bind('<Enter>', on_enter_browse)
    select_directory_button.bind('<Leave>', on_leave_browse)

    # Button frame for better layout
    button_frame = Frame(single_tab, bg=COLORS['bg'])
    button_frame.grid(row=3, column=0, columnspan=3, pady=20)

    download_button = Button(
        button_frame,
        text="⬇️ Download Video",
        font=('Segoe UI', 11, 'bold'),
        bg=COLORS['primary'],
        fg='white',
        relief=tk.FLAT,
        padx=30,
        pady=12,
        cursor='hand2',
        command=lambda: download_single_video_threaded(
            link_entry.get(),
            download_type_var.get(),
            save_directory_entry.get(),
            1,
            text_area,
            progress_var,
            progress_bar,
            progress_label,
            window,
        ),
    )
    download_button.pack(side=tk.LEFT, padx=5)
    
    # Add hover effect for download button
    def on_enter_download(e):
        e.widget.config(bg=COLORS['primary_hover'])
    def on_leave_download(e):
        e.widget.config(bg=COLORS['primary'])
    download_button.bind('<Enter>', on_enter_download)
    download_button.bind('<Leave>', on_leave_download)

    open_directory_button = Button(
        button_frame,
        text="📂 Open Folder",
        font=('Segoe UI', 10, 'bold'),
        bg=COLORS['success'],
        fg='white',
        relief=tk.FLAT,
        padx=20,
        pady=12,
        cursor='hand2',
        command=lambda: open_directory(save_directory_entry),
    )
    open_directory_button.pack(side=tk.LEFT, padx=5)
    
    # Add hover effect
    def on_enter_open(e):
        e.widget.config(bg='#27ae60')
    def on_leave_open(e):
        e.widget.config(bg=COLORS['success'])
    open_directory_button.bind('<Enter>', on_enter_open)
    open_directory_button.bind('<Leave>', on_leave_open)

    # --- Playlist Download Tab ---
    playlist_tab = ttk.Frame(notebook, style='TFrame')
    notebook.add(playlist_tab, text="📑 Playlist")

    # Configure grid weights
    playlist_tab.columnconfigure(1, weight=1)

    # Playlist input fields with better styling
    Label(playlist_tab, 
          text="YouTube Playlist URL:",
          font=('Segoe UI', 10, 'bold'),
          bg=COLORS['bg'],
          fg=COLORS['fg']).grid(
        row=0, column=0, padx=15, pady=15, sticky="w"
    )
    playlist_link_entry = Entry(playlist_tab, 
                                width=50,
                                font=('Segoe UI', 10),
                                relief=tk.FLAT,
                                borderwidth=2,
                                highlightthickness=1,
                                highlightbackground=COLORS['border'])
    playlist_link_entry.grid(row=0, column=1, padx=15, pady=15, sticky="ew", columnspan=2)

    Label(playlist_tab, 
          text="Download Type:",
          font=('Segoe UI', 10, 'bold'),
          bg=COLORS['bg'],
          fg=COLORS['fg']).grid(
        row=1, column=0, padx=15, pady=15, sticky="w"
    )
    download_type_playlist_var = StringVar(playlist_tab)
    download_type_playlist_var.set("MP4")
    download_type_playlist_menu = OptionMenu(
        playlist_tab, download_type_playlist_var, "MP4", "MP3"
    )
    download_type_playlist_menu.config(font=('Segoe UI', 10),
                                      bg='white',
                                      fg=COLORS['fg'],
                                      relief=tk.FLAT,
                                      highlightthickness=1,
                                      highlightbackground=COLORS['border'],
                                      activebackground=COLORS['primary'],
                                      activeforeground='white')
    download_type_playlist_menu.grid(row=1, column=1, padx=15, pady=15, sticky="w")

    Label(playlist_tab, 
          text="Save Directory:",
          font=('Segoe UI', 10, 'bold'),
          bg=COLORS['bg'],
          fg=COLORS['fg']).grid(
        row=2, column=0, padx=15, pady=15, sticky="w"
    )
    playlist_save_directory_entry = Entry(playlist_tab, 
                                          width=50,
                                          font=('Segoe UI', 10),
                                          relief=tk.FLAT,
                                          borderwidth=2,
                                          highlightthickness=1,
                                          highlightbackground=COLORS['border'])
    playlist_save_directory_entry.grid(row=2, column=1, padx=15, pady=15, sticky="ew")

    select_playlist_directory_button = Button(
        playlist_tab,
        text="📁 Browse",
        font=('Segoe UI', 10, 'bold'),
        bg=COLORS['secondary'],
        fg='white',
        relief=tk.FLAT,
        padx=20,
        pady=8,
        cursor='hand2',
        command=lambda: select_save_directory(
            playlist_save_directory_entry, load_last_directory()
        ),
    )
    select_playlist_directory_button.grid(row=2, column=2, padx=15, pady=15, sticky="w")
    
    # Add hover effect
    select_playlist_directory_button.bind('<Enter>', on_enter_browse)
    select_playlist_directory_button.bind('<Leave>', on_leave_browse)

    # Button frame for better layout
    playlist_button_frame = Frame(playlist_tab, bg=COLORS['bg'])
    playlist_button_frame.grid(row=3, column=0, columnspan=3, pady=20)

    download_playlist_button = Button(
        playlist_button_frame,
        text="⬇️ Download Playlist",
        font=('Segoe UI', 11, 'bold'),
        bg=COLORS['accent'],
        fg='white',
        relief=tk.FLAT,
        padx=30,
        pady=12,
        cursor='hand2',
        command=lambda: download_playlist_threaded(
            playlist_link_entry.get(),
            download_type_playlist_var.get(),
            playlist_save_directory_entry.get(),
            text_area,
            progress_var,
            progress_label,
            progress_bar,
            window,
        ),
    )
    download_playlist_button.pack(side=tk.LEFT, padx=5)
    
    # Add hover effect
    def on_enter_playlist(e):
        e.widget.config(bg='#8e44ad')
    def on_leave_playlist(e):
        e.widget.config(bg=COLORS['accent'])
    download_playlist_button.bind('<Enter>', on_enter_playlist)
    download_playlist_button.bind('<Leave>', on_leave_playlist)

    open_playlist_directory_button = Button(
        playlist_button_frame,
        text="📂 Open Folder",
        font=('Segoe UI', 10, 'bold'),
        bg=COLORS['success'],
        fg='white',
        relief=tk.FLAT,
        padx=20,
        pady=12,
        cursor='hand2',
        command=lambda: open_directory(playlist_save_directory_entry),
    )
    open_playlist_directory_button.pack(side=tk.LEFT, padx=5)
    
    open_playlist_directory_button.bind('<Enter>', on_enter_open)
    open_playlist_directory_button.bind('<Leave>', on_leave_open)

    # Load the last directory if available
    last_directory = load_last_directory()
    if last_directory:
        save_directory_entry.insert(0, last_directory)
        playlist_save_directory_entry.insert(0, last_directory)

    # --- Utility Functions ---
    def reset_values():
        """
        Resets all input fields, progress, and messages to default values.
        """
        link_entry.delete(0, tk.END)
        playlist_link_entry.delete(0, tk.END)
        save_directory_entry.delete(0, tk.END)
        playlist_save_directory_entry.delete(0, tk.END)
        progress_var.set(0.0)
        progress_label.config(text="Ready to download")
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        text_area.config(state=tk.DISABLED)

    def open_directory(entry):
        """
        Opens the directory specified in the entry field.
        """
        directory = entry.get()
        if os.path.exists(directory):
            os.startfile(directory)
        else:
            show_error_message(f"Directory not found: {directory}")

    # Bottom control frame
    control_frame = Frame(window, bg=COLORS['bg'], height=60)
    control_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=(0, 20))

    # Reset button with modern styling
    reset_button = Button(control_frame, 
                         text="🔄 Reset All",
                         font=('Segoe UI', 10, 'bold'),
                         bg=COLORS['danger'],
                         fg='white',
                         relief=tk.FLAT,
                         padx=25,
                         pady=10,
                         cursor='hand2',
                         command=reset_values)
    reset_button.pack(side=tk.LEFT)
    
    # Add hover effect
    def on_enter_reset(e):
        e.widget.config(bg='#c0392b')
    def on_leave_reset(e):
        e.widget.config(bg=COLORS['danger'])
    reset_button.bind('<Enter>', on_enter_reset)
    reset_button.bind('<Leave>', on_leave_reset)
    
    # Add info label
    info_label = Label(control_frame,
                      text="💡 Tip: You can download videos individually or entire playlists",
                      font=('Segoe UI', 9),
                      bg=COLORS['bg'],
                      fg=COLORS['secondary'])
    info_label.pack(side=tk.RIGHT, padx=10)

    return window, text_area, progress_var, progress_label, progress_bar


if __name__ == "__main__":
    window, text_area, progress_var, progress_label, progress_bar = setup_gui()
    window.mainloop()
