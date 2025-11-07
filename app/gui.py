"""
Prosty interfejs graficzny (GUI) dla Presidio Local Anonymizer.
Obsługuje drag & drop i przetwarzanie wsadowe.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from pathlib import Path
import logging
from typing import List
import sys

# Dodaj parent directory do sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.analyzer import build_analyzer
from app.main import _process_file

# Konfiguracja logowania dla GUI
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("app.gui")


class AnonymizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Presidio Local Anonymizer - GUI")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # Zmienne
        self.analyzer = None
        self.config = None
        self.files_to_process = []
        self.is_processing = False

        # Styl
        style = ttk.Style()
        style.theme_use('clam')

        # Inicjalizacja analyzera w tle
        self.init_analyzer()

        # Buduj interfejs
        self.create_widgets()

        # Drag & Drop setup (opcjonalne - wymaga tkinterdnd2)
        try:
            from tkinterdnd2 import DND_FILES, TkinterDnD
            # Note: Wymaga reinstall root jako TkinterDnD.Tk()
            logger.info("Drag & Drop dostępny (wymaga tkinterdnd2)")
        except ImportError:
            logger.info("Drag & Drop niedostępny - zainstaluj: pip install tkinterdnd2")

    def create_widgets(self):
        """Tworzy wszystkie widgety GUI."""

        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame,
            text="🔐 Presidio Local Anonymizer",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)

        # Main content
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Instrukcja
        instruction_label = tk.Label(
            main_frame,
            text="Wybierz pliki do zanonimizowania lub przeciągnij je tutaj",
            font=("Arial", 10)
        )
        instruction_label.pack(pady=(0, 10))

        # Listbox z plikami
        self.files_frame = tk.LabelFrame(main_frame, text="Pliki do przetworzenia", padx=10, pady=10)
        self.files_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Scrollbar dla listboxa
        scrollbar = tk.Scrollbar(self.files_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.files_listbox = tk.Listbox(
            self.files_frame,
            yscrollcommand=scrollbar.set,
            font=("Courier", 9),
            height=8
        )
        self.files_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)

        # Przyciski akcji
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)

        self.select_files_btn = ttk.Button(
            buttons_frame,
            text="📄 Wybierz pliki...",
            command=self.select_files
        )
        self.select_files_btn.pack(side=tk.LEFT, padx=5)

        self.select_folder_btn = ttk.Button(
            buttons_frame,
            text="📁 Wybierz folder...",
            command=self.select_folder
        )
        self.select_folder_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = ttk.Button(
            buttons_frame,
            text="🗑️ Wyczyść listę",
            command=self.clear_files
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Progress bar
        self.progress_frame = tk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=10)

        self.progress_label = tk.Label(
            self.progress_frame,
            text="Gotowy do przetwarzania",
            font=("Arial", 9)
        )
        self.progress_label.pack(anchor=tk.W)

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(fill=tk.X, pady=5)

        # Przycisk anonimizacji
        self.anonymize_btn = ttk.Button(
            main_frame,
            text="🚀 Anonimizuj",
            command=self.start_anonymization,
            state=tk.DISABLED
        )
        self.anonymize_btn.pack(pady=10)

        # Log output
        log_frame = tk.LabelFrame(main_frame, text="Logi", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            font=("Courier", 8),
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Inicjalizacja...",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 8)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def init_analyzer(self):
        """Inicjalizuje Presidio Analyzer w osobnym wątku."""
        def init():
            try:
                self.log("Inicjalizacja Presidio Analyzer...")
                self.analyzer, self.config = build_analyzer()
                self.log("✓ Analyzer gotowy")
                self.status_bar.config(text="Gotowy")
            except Exception as e:
                self.log(f"✗ Błąd inicjalizacji: {e}", level="ERROR")
                self.status_bar.config(text="Błąd inicjalizacji")
                messagebox.showerror("Błąd", f"Nie można zainicjalizować analyzera:\n{e}")

        thread = threading.Thread(target=init, daemon=True)
        thread.start()

    def log(self, message: str, level: str = "INFO"):
        """Dodaje wiadomość do logu."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{level}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

        if level == "ERROR":
            logger.error(message)
        else:
            logger.info(message)

    def select_files(self):
        """Otwiera dialog wyboru plików."""
        filetypes = [
            ("Wszystkie obsługiwane", "*.docx *.odt *.pdf *.png *.jpg *.jpeg *.tiff *.tif"),
            ("Word", "*.docx"),
            ("OpenDocument", "*.odt"),
            ("PDF", "*.pdf"),
            ("Obrazy", "*.png *.jpg *.jpeg *.tiff *.tif"),
            ("Wszystkie pliki", "*.*")
        ]

        files = filedialog.askopenfilenames(
            title="Wybierz pliki do zanonimizowania",
            filetypes=filetypes
        )

        if files:
            for file in files:
                if file not in self.files_to_process:
                    self.files_to_process.append(file)
                    self.files_listbox.insert(tk.END, Path(file).name)

            self.update_ui_state()
            self.log(f"Dodano {len(files)} plików")

    def select_folder(self):
        """Otwiera dialog wyboru folderu."""
        folder = filedialog.askdirectory(title="Wybierz folder z dokumentami")

        if folder:
            folder_path = Path(folder)

            # Znajdź wszystkie obsługiwane pliki
            patterns = ['*.docx', '*.odt', '*.pdf', '*.png', '*.jpg', '*.jpeg', '*.tiff', '*.tif']
            files_found = []

            for pattern in patterns:
                files_found.extend(list(folder_path.rglob(pattern)))

            if files_found:
                for file in files_found:
                    file_str = str(file)
                    if file_str not in self.files_to_process:
                        self.files_to_process.append(file_str)
                        self.files_listbox.insert(tk.END, file.name)

                self.update_ui_state()
                self.log(f"Znaleziono {len(files_found)} plików w folderze")
            else:
                messagebox.showinfo("Informacja", "Nie znaleziono obsługiwanych plików w tym folderze")

    def clear_files(self):
        """Czyści listę plików."""
        self.files_to_process.clear()
        self.files_listbox.delete(0, tk.END)
        self.update_ui_state()
        self.log("Wyczyszczono listę plików")

    def update_ui_state(self):
        """Aktualizuje stan przycisków w zależności od stanu aplikacji."""
        if self.is_processing:
            self.anonymize_btn.config(state=tk.DISABLED)
            self.select_files_btn.config(state=tk.DISABLED)
            self.select_folder_btn.config(state=tk.DISABLED)
            self.clear_btn.config(state=tk.DISABLED)
        else:
            if self.files_to_process and self.analyzer:
                self.anonymize_btn.config(state=tk.NORMAL)
            else:
                self.anonymize_btn.config(state=tk.DISABLED)

            self.select_files_btn.config(state=tk.NORMAL)
            self.select_folder_btn.config(state=tk.NORMAL)
            self.clear_btn.config(state=tk.NORMAL)

    def start_anonymization(self):
        """Rozpoczyna proces anonimizacji w osobnym wątku."""
        if not self.files_to_process:
            messagebox.showwarning("Uwaga", "Brak plików do przetworzenia")
            return

        if not self.analyzer:
            messagebox.showerror("Błąd", "Analyzer nie jest zainicjalizowany")
            return

        self.is_processing = True
        self.update_ui_state()

        # Uruchom w osobnym wątku
        thread = threading.Thread(target=self.anonymize_files, daemon=True)
        thread.start()

    def anonymize_files(self):
        """Przetwarza wszystkie pliki z listy."""
        total = len(self.files_to_process)
        success_count = 0
        error_count = 0

        self.progress_bar['maximum'] = total
        self.progress_bar['value'] = 0

        for i, file_path in enumerate(self.files_to_process):
            try:
                file_name = Path(file_path).name
                self.progress_label.config(text=f"Przetwarzanie {i + 1}/{total}: {file_name}")
                self.log(f"Przetwarzanie: {file_name}")

                # Przetwórz plik
                report = _process_file(Path(file_path), self.analyzer, self.config)

                if report:
                    self.log(f"✓ Gotowe: {file_name}")
                    success_count += 1
                else:
                    self.log(f"⚠ Pominięto: {file_name}", level="WARNING")

            except Exception as e:
                self.log(f"✗ Błąd dla {file_name}: {e}", level="ERROR")
                error_count += 1

            # Aktualizuj progress bar
            self.progress_bar['value'] = i + 1
            self.root.update_idletasks()

        # Podsumowanie
        self.progress_label.config(text=f"Zakończono! Sukces: {success_count}, Błędy: {error_count}")
        self.log("=" * 50)
        self.log(f"PODSUMOWANIE: {success_count} plików przetworzono, {error_count} błędów")

        messagebox.showinfo(
            "Zakończono",
            f"Przetworzono {success_count} plików\n"
            f"Błędy: {error_count}\n\n"
            f"Zanonimizowane pliki znajdują się w tych samych folderach co oryginały."
        )

        self.is_processing = False
        self.update_ui_state()


def main():
    """Główna funkcja uruchamiająca GUI."""
    try:
        # Spróbuj użyć tkinterdnd2 dla drag & drop
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
        logger.info("Uruchomiono z obsługą Drag & Drop")
    except ImportError:
        root = tk.Tk()
        logger.info("Uruchomiono bez Drag & Drop (zainstaluj tkinterdnd2 dla pełnej funkcjonalności)")

    app = AnonymizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
