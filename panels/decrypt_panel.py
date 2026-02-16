"""
CipherForge - Decrypt Panel
"""

import customtkinter as ctk
from tkinter import filedialog
import os

from theme import (
    VOID_900, NEON_GREEN, NEON_CYAN, TEXT_MAIN, TEXT_MUTED, TEXT_DIM,
    FONT_HEADING_SM, FONT_TINY,
    NeonButton, NeonSegmentedButton, CyberTextBox, FileDropZone,
    SectionLabel, CyberPanel, SURFACE,
)


class DecryptPanel(ctk.CTkFrame):
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

        icon_frame = ctk.CTkFrame(header, fg_color=VOID_900, border_color=NEON_GREEN,
                                   border_width=1, corner_radius=0, width=36, height=36)
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="D", font=FONT_HEADING_SM, text_color=NEON_GREEN).place(
            relx=0.5, rely=0.5, anchor="center")

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        ctk.CTkLabel(title_frame, text="DECRYPT", font=FONT_HEADING_SM,
                     text_color=TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="RESTORE ENCRYPTED DATA TO ITS ORIGINAL FORM",
                     font=FONT_TINY, text_color=TEXT_MUTED).pack(anchor="w")

        # Two columns
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        left = ctk.CTkFrame(content, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right = ctk.CTkFrame(content, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # ── Left ──
        SectionLabel(left, text="Input Mode").pack(anchor="w", pady=(0, 6))
        self.mode_selector = NeonSegmentedButton(
            left, values=["Text", "File"],
            command=self._on_mode_change, color=NEON_GREEN,
        )
        self.mode_selector.pack(anchor="w", pady=(0, 16))

        self.input_container = ctk.CTkFrame(left, fg_color="transparent")
        self.input_container.pack(fill="both", expand=True, pady=(0, 16))

        self.text_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        SectionLabel(self.text_frame, text="Encrypted Input").pack(anchor="w", pady=(0, 6))
        self.input_text = CyberTextBox(self.text_frame, height=240)
        self.input_text.pack(fill="both", expand=True)
        self.text_frame.pack(fill="both", expand=True)

        self.file_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        SectionLabel(self.file_frame, text="Encrypted File").pack(anchor="w", pady=(0, 6))
        self.file_zone = FileDropZone(
            self.file_frame, command=self._select_file,
            label="Click to select .enc file",
        )
        self.file_zone.pack(fill="x")

        self.decrypt_btn = NeonButton(
            left, text="DECRYPT DATA", color=NEON_GREEN, height=44,
            command=self._do_decrypt,
        )
        self.decrypt_btn.pack(fill="x")

        # ── Right ──
        header_right = ctk.CTkFrame(right, fg_color="transparent")
        header_right.pack(fill="x", pady=(0, 6))
        SectionLabel(header_right, text="Decrypted Output").pack(side="left")

        self.copy_btn = NeonButton(
            header_right, text="COPY", color=NEON_GREEN, width=70, height=26,
            command=self._copy_output,
        )

        self.output_text = CyberTextBox(right, height=340, text_color=TEXT_MAIN)
        self.output_text.pack(fill="both", expand=True, pady=(0, 10))
        self.output_text.configure(state="disabled")

        info = CyberPanel(right)
        info.pack(fill="x")
        ctk.CTkLabel(
            info,
            text="[INFO] Decryption uses the stored encryption key. Digital signature is verified automatically.",
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
        path = filedialog.askopenfilename(
            title="Select encrypted file",
            filetypes=[("Encrypted files", "*.enc"), ("All files", "*.*")],
        )
        if path:
            self.file_zone.set_file(path)

    def _do_decrypt(self):
        try:
            if self.input_mode == "text":
                ct = self.input_text.get_text()
                if not ct:
                    self.status_bar.set_error("Input is empty")
                    return
                result = self.engine.decrypt_text(ct)
                self.output_text.configure(state="normal")
                self.output_text.set_text(result)
                self.output_text.configure(state="disabled")
                self.copy_btn.pack(side="right")
                self.status_bar.set_success("Decrypted successfully. Signature: VALID")
            else:
                if not self.file_zone.filepath:
                    self.status_bar.set_error("No file selected")
                    return
                out_path = self.engine.decrypt_file(self.file_zone.filepath)
                self.output_text.configure(state="normal")
                self.output_text.set_text(f"File decrypted successfully!\n\nSaved to:\n{out_path}")
                self.output_text.configure(state="disabled")
                self.status_bar.set_success(f"File decrypted: {os.path.basename(out_path)}")
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

    def clear(self):
        self.input_text.set_text("")
        self.output_text.configure(state="normal")
        self.output_text.set_text("")
        self.output_text.configure(state="disabled")
        self.file_zone.clear()
