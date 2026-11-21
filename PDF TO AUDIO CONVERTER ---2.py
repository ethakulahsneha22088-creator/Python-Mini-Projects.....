"""
PDF to Audio Converter
A beginner-friendly Python project that extracts text from a PDF
and converts it into an MP3 audio file using gTTS.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

import pdfplumber
from gtts import gTTS


def extract_text(pdf_path):
    """Extract readable text from every page of a PDF."""
    page_texts = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                page_texts.append(text)

    return "\n".join(page_texts).strip()


def split_text(text, max_chars=4000):
    """Split long text into smaller chunks at word boundaries."""
    words = text.split()
    chunks = []
    current = []

    for word in words:
        candidate = " ".join(current + [word])
        if len(candidate) > max_chars and current:
            chunks.append(" ".join(current))
            current = [word]
        else:
            current.append(word)

    if current:
        chunks.append(" ".join(current))

    return chunks


def convert_pdf_to_audio():
    pdf_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )
    if not pdf_path:
        return

    try:
        status_label.config(text="Extracting text...")
        root.update_idletasks()

        extracted_text = extract_text(pdf_path)
        if not extracted_text:
            messagebox.showwarning(
                "No text found",
                "This PDF has no extractable text. It may be a scanned document."
            )
            status_label.config(text="Ready")
            return

        output_path = filedialog.asksaveasfilename(
            title="Save audio file",
            defaultextension=".mp3",
            filetypes=[("MP3 audio", "*.mp3")],
            initialfile=f"{Path(pdf_path).stem}_audio.mp3"
        )
        if not output_path:
            status_label.config(text="Ready")
            return

        status_label.config(text="Converting text to audio... Please wait.")
        root.update_idletasks()

        chunks = split_text(extracted_text)
        temporary_files = []

        # Convert chunks separately to support long PDF documents.
        for index, chunk in enumerate(chunks, start=1):
            part_path = Path(output_path).with_name(
                f"{Path(output_path).stem}_part_{index}.mp3"
            )
            gTTS(text=chunk, lang="en", slow=False).save(str(part_path))
            temporary_files.append(part_path)

        # Join MP3 chunks in order without requiring extra audio packages.
        # MP3 frames can be concatenated for normal playback in common players.
        with open(output_path, "wb") as final_audio:
            for part_path in temporary_files:
                with open(part_path, "rb") as part_audio:
                    final_audio.write(part_audio.read())
                part_path.unlink(missing_ok=True)

        status_label.config(text="Conversion completed!")
        messagebox.showinfo(
            "Success",
            f"Audio file created successfully:\n{output_path}"
        )

    except Exception as error:
        status_label.config(text="Conversion failed")
        messagebox.showerror(
            "Error",
            "Something went wrong.\n\n"
            f"{error}\n\n"
            "Check your internet connection and make sure the PDF is valid."
        )


root = tk.Tk()
root.title("PDF to Audio Converter")
root.geometry("520x300")
root.resizable(False, False)

heading = tk.Label(
    root,
    text="PDF TO AUDIO CONVERTER",
    font=("Arial", 18, "bold")
)
heading.pack(pady=(28, 12))

description = tk.Label(
    root,
    text="Select a PDF document and convert its text into speech.",
    font=("Arial", 10)
)
description.pack(pady=5)

convert_button = tk.Button(
    root,
    text="Choose PDF and Convert to MP3",
    font=("Arial", 12, "bold"),
    command=convert_pdf_to_audio,
    padx=16,
    pady=12
)
convert_button.pack(pady=28)

status_label = tk.Label(root, text="Ready", font=("Arial", 10))
status_label.pack(pady=8)

note = tk.Label(
    root,
    text="Note: An internet connection is required for gTTS.",
    font=("Arial", 9),
    fg="gray"
)
note.pack(pady=8)

root.mainloop()
