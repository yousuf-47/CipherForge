"""
CipherForge - Key Management Panel
"""

import customtkinter as ctk

from theme import (
    VOID_900, VOID_600, NEON_YELLOW, NEON_CYAN, NEON_GREEN, NEON_RED,
    TEXT_MAIN, TEXT_MUTED, TEXT_DIM,
    FONT_HEADING_SM, FONT_LABEL, FONT_MONO, FONT_MONO_SM, FONT_TINY,
    NeonButton, CyberTextBox, SectionLabel, CyberPanel, SURFACE,
)


class KeysPanel(ctk.CTkFrame):
    def __init__(self, master, engine, status_bar, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.engine = engine
        self.status_bar = status_bar
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        icon_frame = ctk.CTkFrame(header, fg_color=VOID_900, border_color=NEON_YELLOW,
                                   border_width=1, corner_radius=0, width=36, height=36)
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="K", font=FONT_HEADING_SM, text_color=NEON_YELLOW).place(
            relx=0.5, rely=0.5, anchor="center")

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        ctk.CTkLabel(title_frame, text="KEY MANAGEMENT", font=FONT_HEADING_SM,
                     text_color=TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="RSA & ENCRYPTION KEY INFORMATION",
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

        # ── Left - Key Info ──
        info_panel = CyberPanel(left)
        info_panel.pack(fill="x", pady=(0, 12))

        SectionLabel(info_panel, text="Key Storage Location").pack(
            anchor="w", padx=12, pady=(12, 4))

        self.path_label = ctk.CTkLabel(
            info_panel, text=self.engine.key_dir,
            font=FONT_MONO_SM, text_color=NEON_CYAN, anchor="w", wraplength=350,
        )
        self.path_label.pack(anchor="w", padx=12, pady=(0, 4))

        # Separator
        ctk.CTkFrame(info_panel, fg_color=VOID_600, height=1).pack(fill="x", padx=12, pady=8)

        SectionLabel(info_panel, text="Encryption Key Status").pack(
            anchor="w", padx=12, pady=(0, 4))

        self.key_status_frame = ctk.CTkFrame(info_panel, fg_color="transparent")
        self.key_status_frame.pack(anchor="w", padx=12, pady=(0, 12))

        self.status_indicator = ctk.CTkLabel(
            self.key_status_frame, text="", font=FONT_MONO, width=20,
        )
        self.status_indicator.pack(side="left")

        self.status_text = ctk.CTkLabel(
            self.key_status_frame, text="", font=FONT_MONO,
        )
        self.status_text.pack(side="left", padx=(4, 0))

        self._update_key_status()

        # Warning box
        warn_panel = CyberPanel(left, border_color=NEON_YELLOW)
        warn_panel.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(
            warn_panel,
            text="[WARNING] Never share your encryption key. It is required for decryption and is unique per session.",
            font=FONT_TINY, text_color=NEON_YELLOW, wraplength=350, anchor="w", justify="left",
        ).pack(padx=12, pady=10, anchor="w")

        # Refresh button
        NeonButton(left, text="REFRESH STATUS", color=NEON_YELLOW, height=36,
                   command=self._update_key_status).pack(fill="x")

        # ── Right - RSA Public Key ──
        header_right = ctk.CTkFrame(right, fg_color="transparent")
        header_right.pack(fill="x", pady=(0, 6))
        SectionLabel(header_right, text="RSA Public Key (2048-bit)").pack(side="left")

        NeonButton(header_right, text="COPY", color=NEON_CYAN, width=70, height=26,
                   command=self._copy_key).pack(side="right")

        self.key_text = CyberTextBox(right, height=360, text_color=NEON_GREEN)
        self.key_text.pack(fill="both", expand=True)

        try:
            pub_key = self.engine.get_public_key()
            self.key_text.set_text(pub_key)
        except Exception:
            self.key_text.set_text("Failed to load public key")

        self.key_text.configure(state="disabled")

    def _update_key_status(self):
        has_key = self.engine.has_encryption_key()
        if has_key:
            self.status_indicator.configure(text="*", text_color=NEON_GREEN)
            self.status_text.configure(text="Available", text_color=NEON_GREEN)
        else:
            self.status_indicator.configure(text="*", text_color=TEXT_DIM)
            self.status_text.configure(text="Not yet generated", text_color=TEXT_MUTED)

    def _copy_key(self):
        self.key_text.configure(state="normal")
        text = self.key_text.get_text()
        self.key_text.configure(state="disabled")
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.status_bar.set_info("Public key copied to clipboard")

    def refresh(self):
        self._update_key_status()
