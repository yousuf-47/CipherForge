"""
CipherForge - Cyberpunk Theme & Custom Widgets
Dark void backgrounds, neon cyan/purple/green accents, glow effects.
"""

import customtkinter as ctk
import tkinter as tk


# ── Color Palette ──
VOID_900 = "#030712"
VOID_800 = "#0B101B"
VOID_700 = "#111827"
VOID_600 = "#1E293B"
SURFACE = "#0F1729"

NEON_CYAN = "#00F3FF"
NEON_CYAN_DIM = "#005F66"
NEON_CYAN_DARK = "#003338"
NEON_PURPLE = "#BC13FE"
NEON_PURPLE_DIM = "#4A0566"
NEON_GREEN = "#00FF41"
NEON_GREEN_DIM = "#004D13"
NEON_RED = "#FF003C"
NEON_RED_DIM = "#4D0012"
NEON_YELLOW = "#FAFF00"
NEON_YELLOW_DIM = "#4D4E00"

TEXT_MAIN = "#F8FAFC"
TEXT_MUTED = "#64748B"
TEXT_DIM = "#334155"

# ── Fonts ──
FONT_HEADING = ("Consolas", 18, "bold")
FONT_HEADING_SM = ("Consolas", 14, "bold")
FONT_BODY = ("Consolas", 12)
FONT_BODY_SM = ("Consolas", 11)
FONT_MONO = ("Consolas", 10)
FONT_MONO_SM = ("Consolas", 9)
FONT_LABEL = ("Consolas", 10, "bold")
FONT_TINY = ("Consolas", 8)
FONT_TITLE = ("Consolas", 28, "bold")
FONT_TITLE_LG = ("Consolas", 42, "bold")


def configure_theme():
    """Set up the global CustomTkinter theme."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")


class NeonButton(ctk.CTkButton):
    """Cyberpunk neon-bordered button with glow hover effect."""

    def __init__(self, master, text="", color=NEON_CYAN, hover_color=None, **kwargs):
        font = kwargs.pop("font", None)  # (keep this if you applied the previous fix)

        super().__init__(
            master,
            text=text.upper(),
            font=font or FONT_LABEL,
            fg_color="transparent",
            text_color=color,
            border_color=color,
            border_width=1,
            hover_color=self._dim(color),
            corner_radius=0,
            **kwargs,
        )
        self._color = color

        # ✅ Use different method names (don’t override CTkButton._on_enter/_on_leave)
        self.bind("<Enter>", self._hover_enter)
        self.bind("<Leave>", self._hover_leave)

    def _dim(self, color):
        mapping = {
            NEON_CYAN: NEON_CYAN_DARK,
            NEON_GREEN: NEON_GREEN_DIM,
            NEON_PURPLE: NEON_PURPLE_DIM,
            NEON_RED: NEON_RED_DIM,
            NEON_YELLOW: NEON_YELLOW_DIM,
        }
        return mapping.get(color, VOID_700)

    def _hover_enter(self, event=None):
        self.configure(border_width=2)

    def _hover_leave(self, event=None):
        self.configure(border_width=1)



class NeonSegmentedButton(ctk.CTkFrame):
    """Segmented button bar with neon styling."""

    def __init__(self, master, values, command=None, color=NEON_CYAN, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.buttons = []
        self.selected = ctk.StringVar(value=values[0] if values else "")
        self._command = command
        self._color = color

        for val in values:
            btn = ctk.CTkButton(
                self,
                text=val.upper(),
                font=FONT_MONO,
                fg_color="transparent",
                text_color=TEXT_MUTED,
                border_color=VOID_600,
                border_width=1,
                hover_color=VOID_700,
                corner_radius=0,
                width=100,
                height=34,
                command=lambda v=val: self._select(v),
            )
            btn.pack(side="left", padx=(0, 2))
            self.buttons.append((val, btn))

        self._update_visuals()

    def _select(self, value):
        self.selected.set(value)
        self._update_visuals()
        if self._command:
            self._command(value)

    def _update_visuals(self):
        current = self.selected.get()
        for val, btn in self.buttons:
            if val == current:
                btn.configure(
                    fg_color=self._dim_bg(self._color),
                    text_color=self._color,
                    border_color=self._color,
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=TEXT_MUTED,
                    border_color=VOID_600,
                )

    def _dim_bg(self, color):
        mapping = {
            NEON_CYAN: NEON_CYAN_DARK,
            NEON_GREEN: NEON_GREEN_DIM,
            NEON_PURPLE: NEON_PURPLE_DIM,
            NEON_YELLOW: NEON_YELLOW_DIM,
        }
        return mapping.get(color, VOID_700)

    def get(self):
        return self.selected.get()

    def set(self, value):
        self.selected.set(value)
        self._update_visuals()


class CyberTextBox(ctk.CTkTextbox):
    """Styled monospace text area with cyber look."""

    def __init__(self, master, **kwargs):
        defaults = {
            "font": FONT_MONO,
            "fg_color": VOID_900,
            "text_color": TEXT_MAIN,
            "border_color": VOID_600,
            "border_width": 1,
            "corner_radius": 0,
            "scrollbar_button_color": NEON_CYAN_DIM,
            "scrollbar_button_hover_color": NEON_CYAN,
        }
        defaults.update(kwargs)
        super().__init__(master, **defaults)

    def set_text(self, text):
        self.delete("1.0", "end")
        self.insert("1.0", text)

    def get_text(self):
        return self.get("1.0", "end").strip()


class CyberEntry(ctk.CTkEntry):
    """Styled entry with cyber look."""

    def __init__(self, master, **kwargs):
        defaults = {
            "font": FONT_MONO,
            "fg_color": VOID_900,
            "text_color": TEXT_MAIN,
            "border_color": VOID_600,
            "border_width": 1,
            "corner_radius": 0,
            "placeholder_text_color": TEXT_DIM,
        }
        defaults.update(kwargs)
        super().__init__(master, **defaults)


class GlowLabel(ctk.CTkLabel):
    """Label with neon text color."""

    def __init__(self, master, text="", color=NEON_CYAN, font=None, **kwargs):
        super().__init__(
            master,
            text=text,
            font=font or FONT_BODY,
            text_color=color,
            **kwargs,
        )


class SectionLabel(ctk.CTkLabel):
    """Tiny uppercase section label."""

    def __init__(self, master, text="", **kwargs):
        super().__init__(
            master,
            text=text.upper(),
            font=FONT_TINY,
            text_color=TEXT_MUTED,
            anchor="w",
            **kwargs,
        )


class CyberPanel(ctk.CTkFrame):
    """Styled panel with subtle border."""

    def __init__(self, master, **kwargs):
        defaults = {
            "fg_color": SURFACE,
            "border_color": VOID_600,
            "border_width": 1,
            "corner_radius": 0,
        }
        defaults.update(kwargs)
        super().__init__(master, **defaults)


class StatusStrip(ctk.CTkFrame):
    """Bottom status strip with typing indicator."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=VOID_800, height=28, corner_radius=0, **kwargs)
        self.pack_propagate(False)

        self.label = ctk.CTkLabel(
            self,
            text="> system.ready_",
            font=FONT_TINY,
            text_color=TEXT_DIM,
            anchor="w",
        )
        self.label.pack(side="left", padx=10, fill="x")

        self.right_label = ctk.CTkLabel(
            self,
            text="CIPHERFORGE v2.0",
            font=FONT_TINY,
            text_color=TEXT_DIM,
            anchor="e",
        )
        self.right_label.pack(side="right", padx=10)

    def set_status(self, text, color=TEXT_DIM):
        self.label.configure(text=f"> {text}_", text_color=color)

    def set_info(self, text, color=NEON_CYAN):
        self.set_status(text, color)
        self.after(4000, lambda: self.set_status("system.ready", TEXT_DIM))

    def set_success(self, text):
        self.set_info(text, NEON_GREEN)

    def set_error(self, text):
        self.set_info(text, NEON_RED)


class AlgorithmSelector(ctk.CTkFrame):
    """Three-option algorithm selector with descriptions."""

    ALGOS = [
        ("AES-GCM", "Authenticated encryption", NEON_CYAN),
        ("AES-CBC", "Block cipher mode", NEON_PURPLE),
        ("ChaCha20", "Stream cipher", NEON_GREEN),
    ]

    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.selected = ctk.StringVar(value="AES-GCM")
        self._command = command
        self._buttons = []

        for algo, desc, color in self.ALGOS:
            frame = ctk.CTkFrame(self, fg_color="transparent", border_color=VOID_600,
                                 border_width=1, corner_radius=0)
            frame.pack(side="left", padx=(0, 6), fill="x", expand=True)

            inner = ctk.CTkFrame(frame, fg_color="transparent")
            inner.pack(padx=12, pady=8)

            name_lbl = ctk.CTkLabel(inner, text=algo, font=FONT_LABEL, text_color=TEXT_MUTED, anchor="w")
            name_lbl.pack(anchor="w")

            desc_lbl = ctk.CTkLabel(inner, text=desc, font=FONT_TINY, text_color=TEXT_DIM, anchor="w")
            desc_lbl.pack(anchor="w")

            self._buttons.append((algo, color, frame, name_lbl))

            # Make the whole frame clickable
            for widget in [frame, inner, name_lbl, desc_lbl]:
                widget.bind("<Button-1>", lambda e, a=algo: self._select(a))
                widget.configure(cursor="hand2")

        self._update_visuals()

    def _select(self, algo):
        self.selected.set(algo)
        self._update_visuals()
        if self._command:
            self._command(algo)

    def _update_visuals(self):
        current = self.selected.get()
        for algo, color, frame, name_lbl in self._buttons:
            if algo == current:
                frame.configure(border_color=color, fg_color=VOID_800)
                name_lbl.configure(text_color=color)
            else:
                frame.configure(border_color=VOID_600, fg_color="transparent")
                name_lbl.configure(text_color=TEXT_MUTED)

    def get(self):
        return self.selected.get()


class FileDropZone(ctk.CTkFrame):
    """File selection area styled as a drop zone."""

    def __init__(self, master, command=None, label="Click to select file", **kwargs):
        super().__init__(master, fg_color=VOID_900, border_color=VOID_600,
                         border_width=1, corner_radius=0, height=120, **kwargs)
        self.pack_propagate(False)
        self._command = command
        self.filepath = None

        self.inner = ctk.CTkFrame(self, fg_color="transparent")
        self.inner.place(relx=0.5, rely=0.5, anchor="center")

        self.icon_label = ctk.CTkLabel(self.inner, text="[ + ]", font=FONT_HEADING,
                                       text_color=TEXT_DIM)
        self.icon_label.pack()

        self.text_label = ctk.CTkLabel(self.inner, text=label, font=FONT_MONO_SM,
                                       text_color=TEXT_MUTED)
        self.text_label.pack(pady=(4, 0))

        self.size_label = ctk.CTkLabel(self.inner, text="", font=FONT_TINY,
                                       text_color=NEON_CYAN_DIM)
        self.size_label.pack()

        for w in [self, self.inner, self.icon_label, self.text_label, self.size_label]:
            w.bind("<Button-1>", self._on_click)
            w.configure(cursor="hand2")

    def _on_click(self, event=None):
        if self._command:
            self._command()

    def set_file(self, filepath):
        self.filepath = filepath
        name = os.path.basename(filepath) if filepath else ""
        if filepath and os.path.exists(filepath):
            size = os.path.getsize(filepath)
            if size > 1024 * 1024:
                size_str = f"{size / (1024*1024):.1f} MB"
            else:
                size_str = f"{size / 1024:.1f} KB"
            self.text_label.configure(text=name)
            self.size_label.configure(text=size_str)
            self.icon_label.configure(text_color=NEON_CYAN)
            self.configure(border_color=NEON_CYAN_DIM)
        else:
            self.text_label.configure(text="Click to select file")
            self.size_label.configure(text="")
            self.icon_label.configure(text_color=TEXT_DIM)
            self.configure(border_color=VOID_600)

    def clear(self):
        self.filepath = None
        self.set_file(None)


import os
