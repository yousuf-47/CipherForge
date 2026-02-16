"""
CipherForge - Encrypt Panel
"""

import customtkinter as ctk
from tkinter import filedialog
import os

from theme import (
    VOID_900, VOID_600, NEON_CYAN, NEON_GREEN, TEXT_MAIN, TEXT_MUTED, TEXT_DIM,
    FONT_HEADING_SM, FONT_LABEL, FONT_MONO, FONT_MONO_SM, FONT_TINY,
    NeonButton, NeonSegmentedButton, CyberTextBox, AlgorithmSelector,
    FileDropZone, SectionLabel, CyberPanel, SURFACE,
)


class EncryptPanel(ctk.CTkFrame):
    def __init__(self, master, engine, status_bar, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.engine = engine
        self.status_bar = status_bar
        self.input_mode = "text"
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        icon_frame = ctk.CTkFrame(header, fg_color=VOID_900, border_color=NEON_CYAN,
                                   border_width=1, corner_radius=0, width=36, height=36)
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="E", font=FONT_HEADING_SM, text_color=NEON_CYAN).place(
            relx=0.5, rely=0.5, anchor="center")

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        ctk.CTkLabel(title_frame, text="ENCRYPT", font=FONT_HEADING_SM,
                     text_color=TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="SECURE YOUR DATA WITH MILITARY-GRADE ENCRYPTION",
                     font=FONT_TINY, text_color=TEXT_MUTED).pack(anchor="w")

        # Main content - two columns
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        left = ctk.CTkFrame(content, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right = ctk.CTkFrame(content, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # ── Left Column ──
        # Algorithm selection
        SectionLabel(left, text="Algorithm").pack(anchor="w", pady=(0, 6))
        self.algo_selector = AlgorithmSelector(left)
        self.algo_selector.pack(fill="x", pady=(0, 16))

        # Input mode
        SectionLabel(left, text="Input Mode").pack(anchor="w", pady=(0, 6))
        self.mode_selector = NeonSegmentedButton(
            left, values=["Text", "File"],
            command=self._on_mode_change, color=NEON_CYAN,
        )
        self.mode_selector.pack(anchor="w", pady=(0, 16))

        # Encrypt button
        self.encrypt_btn = NeonButton(
            left, text="ENCRYPT DATA", color=NEON_CYAN, height=44,
            command=self._do_encrypt,
        )
        self.encrypt_btn.pack(fill="x", pady=(0, 0))

        # Input area container
        self.input_container = ctk.CTkFrame(left, fg_color="transparent")
        self.input_container.pack(fill="both", expand=True, pady=(0, 16))

        # Text input
        self.text_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        SectionLabel(self.text_frame, text="Plaintext Input").pack(anchor="w", pady=(0, 6))
        self.input_text = CyberTextBox(self.text_frame, height=180)
        self.input_text.pack(fill="both", expand=True)
        self.text_frame.pack(fill="both", expand=True)

        # File input (hidden initially)
        self.file_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        SectionLabel(self.file_frame, text="File Upload").pack(anchor="w", pady=(0, 6))
        self.file_zone = FileDropZone(self.file_frame, command=self._select_file)
        self.file_zone.pack(fill="x")


        # ── Right Column ──
        header_right = ctk.CTkFrame(right, fg_color="transparent")
        header_right.pack(fill="x", pady=(0, 6))
        SectionLabel(header_right, text="Encrypted Output").pack(side="left")

        self.btn_frame = ctk.CTkFrame(header_right, fg_color="transparent")
        self.btn_frame.pack(side="right")

        self.copy_btn = NeonButton(
            self.btn_frame, text="COPY", color=NEON_CYAN, width=70, height=26,
            command=self._copy_output,
        )

        self.save_btn = NeonButton(
            self.btn_frame, text="SAVE", color=NEON_GREEN, width=70, height=26,
            command=self._save_output,
        )

        self.output_text = CyberTextBox(right, height=340, text_color=NEON_GREEN)
        self.output_text.pack(fill="both", expand=True, pady=(0, 10))
        self.output_text.configure(state="disabled")

        # Info box
        info = CyberPanel(right)
        info.pack(fill="x")
        ctk.CTkLabel(
            info,
            text="[INFO] Encryption key is auto-saved. Output includes algorithm, nonce/IV, ciphertext, and RSA signature.",
            font=FONT_TINY, text_color=TEXT_DIM, wraplength=400, anchor="w", justify="left",
        ).pack(padx=10, pady=8, anchor="w")

    def _on_mode_change(self, mode):
        self.input_mode = mode.lower()
        if self.input_mode == "text":
            self.file_frame.pack_forget()
            self.text_frame.pack(fill="both", expand=True)
        else:
            self.text_frame.pack_forget()
            self.file_frame.pack(fill="both", expand=True)

    def _select_file(self):
        path = filedialog.askopenfilename(title="Select file to encrypt")
        if path:
            self.file_zone.set_file(path)

    def _do_encrypt(self):
        algo = self.algo_selector.get()
        try:
            if self.input_mode == "text":
                plaintext = self.input_text.get_text()
                if not plaintext:
                    self.status_bar.set_error("Input text is empty")
                    return
                result = self.engine.encrypt_text(algo, plaintext)
                self.output_text.configure(state="normal")
                self.output_text.set_text(result)
                self.output_text.configure(state="disabled")
                self.copy_btn.pack(side="left", padx=(0, 4))
                self.save_btn.pack(side="left")
                self.status_bar.set_success(f"Encrypted with {algo}")
            else:
                if not self.file_zone.filepath:
                    self.status_bar.set_error("No file selected")
                    return
                out_path = self.engine.encrypt_file(algo, self.file_zone.filepath)
                self.output_text.configure(state="normal")
                self.output_text.set_text(f"File encrypted successfully!\n\nSaved to:\n{out_path}")
                self.output_text.configure(state="disabled")
                self.status_bar.set_success(f"File encrypted with {algo}: {os.path.basename(out_path)}")
        except Exception as e:
            self.status_bar.set_error(str(e))

    def _copy_output(self):
        self.output_text.configure(state="normal")
        text = self.output_text.get_text()
        self.output_text.configure(state="disabled")
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.status_bar.set_info("Copied to clipboard")

    def _save_output(self):
        self.output_text.configure(state="normal")
        text = self.output_text.get_text()
        self.output_text.configure(state="disabled")
        if text:
            path = filedialog.asksaveasfilename(
                defaultextension=".enc",
                filetypes=[("Encrypted files", "*.enc"), ("All files", "*.*")],
            )
            if path:
                with open(path, "w") as f:
                    f.write(text)
                self.status_bar.set_success(f"Saved: {os.path.basename(path)}")

    def clear(self):
        self.input_text.set_text("")
        self.output_text.configure(state="normal")
        self.output_text.set_text("")
        self.output_text.configure(state="disabled")
        self.file_zone.clear()
