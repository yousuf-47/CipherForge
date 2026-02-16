"""
CipherForge - Verify Signature Panel
"""

import customtkinter as ctk
from tkinter import filedialog

from theme import (
    VOID_900, VOID_600, NEON_PURPLE, NEON_GREEN, NEON_GREEN_DIM, NEON_RED,
    NEON_RED_DIM, TEXT_MAIN, TEXT_MUTED, TEXT_DIM,
    FONT_HEADING_SM, FONT_HEADING, FONT_LABEL, FONT_TINY, FONT_MONO,
    NeonButton, NeonSegmentedButton, CyberTextBox, FileDropZone,
    SectionLabel, CyberPanel, SURFACE,
)


class VerifyPanel(ctk.CTkFrame):
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

        icon_frame = ctk.CTkFrame(header, fg_color=VOID_900, border_color=NEON_PURPLE,
                                   border_width=1, corner_radius=0, width=36, height=36)
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="V", font=FONT_HEADING_SM, text_color=NEON_PURPLE).place(
            relx=0.5, rely=0.5, anchor="center")

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        ctk.CTkLabel(title_frame, text="VERIFY SIGNATURE", font=FONT_HEADING_SM,
                     text_color=TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="VALIDATE RSA DIGITAL SIGNATURES ON ENCRYPTED DATA",
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
            command=self._on_mode_change, color=NEON_PURPLE,
        )
        self.mode_selector.pack(anchor="w", pady=(0, 16))

        self.input_container = ctk.CTkFrame(left, fg_color="transparent")
        self.input_container.pack(fill="both", expand=True, pady=(0, 16))

        self.text_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        SectionLabel(self.text_frame, text="Encrypted Data").pack(anchor="w", pady=(0, 6))
        self.input_text = CyberTextBox(self.text_frame, height=240)
        self.input_text.pack(fill="both", expand=True)
        self.text_frame.pack(fill="both", expand=True)

        self.file_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        SectionLabel(self.file_frame, text="Encrypted File").pack(anchor="w", pady=(0, 6))
        self.file_zone = FileDropZone(self.file_frame, command=self._select_file)
        self.file_zone.pack(fill="x")

        self.verify_btn = NeonButton(
            left, text="VERIFY SIGNATURE", color=NEON_PURPLE, height=44,
            command=self._do_verify,
        )
        self.verify_btn.pack(fill="x")

        # ── Right - Result Display ──
        self.result_frame = ctk.CTkFrame(right, fg_color="transparent")
        self.result_frame.pack(fill="both", expand=True)

        # Initial empty state
        self._show_empty_state()

    def _show_empty_state(self):
        for w in self.result_frame.winfo_children():
            w.destroy()

        center = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(center, text="[ ? ]", font=FONT_HEADING,
                     text_color=TEXT_DIM).pack()
        ctk.CTkLabel(center, text="AWAITING VERIFICATION", font=FONT_TINY,
                     text_color=TEXT_DIM).pack(pady=(8, 0))

    def _show_result(self, valid, algorithm="unknown"):
        for w in self.result_frame.winfo_children():
            w.destroy()

        if valid:
            color = NEON_GREEN
            bg = NEON_GREEN_DIM
            icon = "[  OK  ]"
            title = "VERIFIED"
            msg1 = "Digital signature is authentic."
            msg2 = "Data integrity confirmed."
        else:
            color = NEON_RED
            bg = NEON_RED_DIM
            icon = "[ FAIL ]"
            title = "FAILED"
            msg1 = "Signature verification failed."
            msg2 = "Data may be tampered or corrupted."

        panel = CyberPanel(self.result_frame, border_color=color)
        panel.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.7)

        inner = ctk.CTkFrame(panel, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(inner, text=icon, font=("Consolas", 32, "bold"),
                     text_color=color).pack()
        ctk.CTkLabel(inner, text=title, font=FONT_HEADING,
                     text_color=color).pack(pady=(12, 4))
        ctk.CTkLabel(inner, text=msg1, font=FONT_MONO,
                     text_color=TEXT_MUTED).pack()
        ctk.CTkLabel(inner, text=msg2, font=FONT_MONO,
                     text_color=TEXT_MUTED).pack()

        if algorithm != "unknown":
            algo_frame = ctk.CTkFrame(inner, fg_color="transparent", border_color=VOID_600,
                                       border_width=1, corner_radius=0)
            algo_frame.pack(pady=(16, 0))
            ctk.CTkLabel(algo_frame, text=f"Algorithm: {algorithm}", font=FONT_TINY,
                         text_color=TEXT_MUTED).pack(padx=12, pady=4)

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
            title="Select encrypted file to verify",
            filetypes=[("Encrypted files", "*.enc"), ("All files", "*.*")],
        )
        if path:
            self.file_zone.set_file(path)

    def _do_verify(self):
        try:
            if self.input_mode == "text":
                ct = self.input_text.get_text()
                if not ct:
                    self.status_bar.set_error("Input is empty")
                    return
                result = self.engine.verify_signature_text(ct)
            else:
                if not self.file_zone.filepath:
                    self.status_bar.set_error("No file selected")
                    return
                result = self.engine.verify_signature_file(self.file_zone.filepath)

            self._show_result(result["valid"], result.get("algorithm", "unknown"))

            if result["valid"]:
                self.status_bar.set_success("Signature verified successfully!")
            else:
                self.status_bar.set_error("Signature verification FAILED")
        except Exception as e:
            self.status_bar.set_error(str(e))
            self._show_result(False)

    def clear(self):
        self.input_text.set_text("")
        self.file_zone.clear()
        self._show_empty_state()
