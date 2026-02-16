#!/usr/bin/env python3
"""
CipherForge - Comprehensive Encryption Tool
A cyberpunk-themed desktop application for AES-GCM, AES-CBC, ChaCha20
encryption with RSA-2048 digital signatures.
"""

import customtkinter as ctk
import sys
import os

# Ensure the desktop_app directory is in path
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from theme import (
    configure_theme, VOID_900, VOID_800, VOID_600, VOID_700, SURFACE,
    NEON_CYAN, NEON_CYAN_DIM, NEON_GREEN, NEON_PURPLE, NEON_YELLOW,
    TEXT_MAIN, TEXT_MUTED, TEXT_DIM,
    FONT_TITLE, FONT_TITLE_LG, FONT_HEADING_SM, FONT_HEADING, FONT_LABEL,
    FONT_BODY, FONT_MONO, FONT_MONO_SM, FONT_TINY,
    NeonButton, StatusStrip, GlowLabel,
)
from crypto_engine import CryptoEngine
from panels.encrypt_panel import EncryptPanel
from panels.decrypt_panel import DecryptPanel
from panels.verify_panel import VerifyPanel
from panels.keys_panel import KeysPanel
from panels.history_panel import HistoryPanel


class CipherForgeApp(ctk.CTk):
    TAB_CONFIG = [
        ("ENCRYPT", NEON_CYAN, "E"),
        ("DECRYPT", NEON_GREEN, "D"),
        ("VERIFY SIG", NEON_PURPLE, "V"),
        ("KEYS", NEON_YELLOW, "K"),
        ("HISTORY", NEON_CYAN, "H"),
    ]

    def __init__(self):
        super().__init__()
        configure_theme()

        self.title("CipherForge - Encryption Tool")
        self.geometry("1200x780")
        self.minsize(1000, 650)
        self.configure(fg_color=VOID_900)

        # Try to set dark title bar on Windows
        try:
            self.attributes("-alpha", 0.98)
        except Exception:
            pass

        self.engine = CryptoEngine()
        self.active_tab = None
        self.tab_buttons = {}
        self.panels = {}
        self.started = False

        self._build_ui()
        self._show_landing()

    def _build_ui(self):
        # ── Top Navbar ──
        self.navbar = ctk.CTkFrame(self, fg_color=VOID_800, height=46, corner_radius=0,
                                    border_color=VOID_600, border_width=0)
        self.navbar.pack(fill="x")
        self.navbar.pack_propagate(False)

        nav_inner = ctk.CTkFrame(self.navbar, fg_color="transparent")
        nav_inner.pack(fill="x", padx=16)

        # Logo
        logo_frame = ctk.CTkFrame(nav_inner, fg_color="transparent")
        logo_frame.pack(side="left", pady=8)

        ctk.CTkLabel(logo_frame, text="//", font=("Consolas", 18, "bold"),
                     text_color=NEON_CYAN).pack(side="left")
        ctk.CTkLabel(logo_frame, text=" CIPHERFORGE ", font=("Consolas", 13, "bold"),
                     text_color=TEXT_MAIN).pack(side="left")

        version_frame = ctk.CTkFrame(logo_frame, fg_color="transparent",
                                      border_color=NEON_CYAN_DIM, border_width=1, corner_radius=0)
        version_frame.pack(side="left", padx=(4, 0))
        ctk.CTkLabel(version_frame, text="v2.0", font=FONT_TINY,
                     text_color=NEON_CYAN_DIM).pack(padx=6, pady=1)

        # Right side - status
        self.nav_status = ctk.CTkLabel(nav_inner, text="", font=FONT_TINY,
                                        text_color=TEXT_DIM)
        self.nav_status.pack(side="right", padx=(0, 4))

        self.nav_indicator = ctk.CTkLabel(nav_inner, text="", font=FONT_TINY, width=16)
        self.nav_indicator.pack(side="right")

        # Bottom separator line
        ctk.CTkFrame(self, fg_color=VOID_600, height=1, corner_radius=0).pack(fill="x")

        # ── Main Content Area ──
        self.content_area = ctk.CTkFrame(self, fg_color=VOID_900, corner_radius=0)
        self.content_area.pack(fill="both", expand=True)

        # ── Status Bar ──
        self.status_bar = StatusStrip(self)
        self.status_bar.pack(fill="x", side="bottom")

    def _show_landing(self):
        """Show the landing/hero screen."""
        self.nav_indicator.configure(text="*", text_color=TEXT_DIM)
        self.nav_status.configure(text="OFFLINE", text_color=TEXT_DIM)

        self.landing = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.landing.pack(fill="both", expand=True)

        # Center content
        center = ctk.CTkFrame(self.landing, fg_color="transparent")
        center.place(relx=0.35, rely=0.5, anchor="center")

        # Badge
        badge = ctk.CTkFrame(center, fg_color="transparent", border_color=NEON_CYAN_DIM,
                              border_width=1, corner_radius=0)
        badge.pack(anchor="w", pady=(0, 24))
        ctk.CTkLabel(badge, text="  MILITARY-GRADE ENCRYPTION  ", font=FONT_TINY,
                     text_color=NEON_CYAN).pack(padx=8, pady=4)

        # Title
        ctk.CTkLabel(center, text="CIPHER", font=FONT_TITLE_LG,
                     text_color=TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(center, text="FORGE", font=FONT_TITLE_LG,
                     text_color=NEON_CYAN).pack(anchor="w", pady=(0, 16))

        # Description
        desc = ctk.CTkLabel(
            center,
            text=(
                "Comprehensive encryption toolkit supporting AES-GCM,\n"
                "AES-CBC, and ChaCha20 algorithms with RSA digital\n"
                "signature verification. Encrypt text and files with\n"
                "military-grade security."
            ),
            font=FONT_MONO_SM, text_color=TEXT_MUTED, anchor="w", justify="left",
        )
        desc.pack(anchor="w", pady=(0, 20))

        # Feature pills
        pills = ctk.CTkFrame(center, fg_color="transparent")
        pills.pack(anchor="w", pady=(0, 28))
        for feat in ["AES-256-GCM", "AES-256-CBC", "CHACHA20", "RSA-2048", "FILE & TEXT"]:
            pill = ctk.CTkFrame(pills, fg_color="transparent", border_color=VOID_600,
                                border_width=1, corner_radius=0)
            pill.pack(side="left", padx=(0, 6))
            ctk.CTkLabel(pill, text=feat, font=FONT_TINY,
                         text_color=TEXT_MUTED).pack(padx=8, pady=3)

        # Start button
        start_btn = NeonButton(
            center, text="  INITIALIZE SESSION  >>  ", color=NEON_CYAN,
            height=48, font=FONT_LABEL, command=self._start_session,
        )
        start_btn.pack(anchor="w", pady=(0, 24))

        # Terminal-style footer
        terminal = ctk.CTkFrame(center, fg_color="transparent")
        terminal.pack(anchor="w")
        for line in [
            "> system.encryption.ready",
            "> rsa_key_generation: standby",
            "> awaiting_session_init_",
        ]:
            ctk.CTkLabel(terminal, text=line, font=FONT_TINY,
                         text_color=TEXT_DIM, anchor="w").pack(anchor="w")

    def _start_session(self):
        """Initialize session and show main workspace."""
        self.started = True
        self.landing.destroy()

        self.nav_indicator.configure(text="*", text_color=NEON_GREEN)
        self.nav_status.configure(text="SECURE  //  SESSION ACTIVE", text_color=NEON_GREEN)
        self.status_bar.set_success("Session initialized. RSA-2048 keys loaded.")

        self._build_workspace()
        self._switch_tab("ENCRYPT")

    def _build_workspace(self):
        """Build the tabbed workspace."""
        # Tab bar
        self.tab_bar = ctk.CTkFrame(self.content_area, fg_color=VOID_800, height=42, corner_radius=0)
        self.tab_bar.pack(fill="x")
        self.tab_bar.pack_propagate(False)

        tab_inner = ctk.CTkFrame(self.tab_bar, fg_color="transparent")
        tab_inner.pack(fill="x", padx=8, pady=4)

        for name, color, icon_letter in self.TAB_CONFIG:
            btn = ctk.CTkButton(
                tab_inner,
                text=f" {icon_letter}  {name} ",
                font=FONT_TINY,
                fg_color="transparent",
                text_color=TEXT_MUTED,
                hover_color=VOID_700,
                corner_radius=0,
                height=32,
                border_width=1,
                border_color=VOID_800,
                command=lambda n=name: self._switch_tab(n),
            )
            btn.pack(side="left", padx=(0, 2))
            self.tab_buttons[name] = (btn, color)

        # Clear button on right
        NeonButton(
            tab_inner, text="CLEAR", color=NEON_CYAN, width=70, height=28,
            command=self._clear_active,
        ).pack(side="right")

        ctk.CTkFrame(self.content_area, fg_color=VOID_600, height=1, corner_radius=0).pack(fill="x")

        # Panel container
        self.panel_container = ctk.CTkFrame(self.content_area, fg_color=VOID_900, corner_radius=0)
        self.panel_container.pack(fill="both", expand=True, padx=20, pady=16)

        # Create panels
        self.panels["ENCRYPT"] = EncryptPanel(self.panel_container, self.engine, self.status_bar)
        self.panels["DECRYPT"] = DecryptPanel(self.panel_container, self.engine, self.status_bar)
        self.panels["VERIFY SIG"] = VerifyPanel(self.panel_container, self.engine, self.status_bar)
        self.panels["KEYS"] = KeysPanel(self.panel_container, self.engine, self.status_bar)
        self.panels["HISTORY"] = HistoryPanel(self.panel_container, self.engine, self.status_bar)

    def _switch_tab(self, tab_name):
        if self.active_tab == tab_name:
            return

        # Hide all panels
        for panel in self.panels.values():
            panel.pack_forget()

        # Update button styles
        for name, (btn, color) in self.tab_buttons.items():
            if name == tab_name:
                btn.configure(
                    text_color=color,
                    border_color=color,
                    fg_color=VOID_700,
                )
            else:
                btn.configure(
                    text_color=TEXT_MUTED,
                    border_color=VOID_800,
                    fg_color="transparent",
                )

        # Show selected panel
        self.panels[tab_name].pack(fill="both", expand=True)
        self.active_tab = tab_name

        # Refresh dynamic panels
        if tab_name == "HISTORY":
            self.panels["HISTORY"].refresh()
        elif tab_name == "KEYS":
            self.panels["KEYS"].refresh()

    def _clear_active(self):
        if self.active_tab and self.active_tab in self.panels:
            panel = self.panels[self.active_tab]
            if hasattr(panel, "clear"):
                panel.clear()
                self.status_bar.set_info("Panel cleared")


def main():
    app = CipherForgeApp()
    app.mainloop()


if __name__ == "__main__":
    main()
