"""
CipherForge - Activity History Panel
"""

import customtkinter as ctk

from theme import (
    VOID_900, VOID_600, VOID_700, NEON_CYAN, NEON_GREEN, NEON_RED,
    NEON_YELLOW, NEON_PURPLE, TEXT_MAIN, TEXT_MUTED, TEXT_DIM,
    FONT_HEADING_SM, FONT_LABEL, FONT_MONO, FONT_MONO_SM, FONT_TINY,
    NeonButton, SectionLabel, CyberPanel, SURFACE,
)


class HistoryPanel(ctk.CTkFrame):
    def __init__(self, master, engine, status_bar, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.engine = engine
        self.status_bar = status_bar
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        icon_frame = ctk.CTkFrame(header, fg_color=VOID_900, border_color=NEON_CYAN,
                                   border_width=1, corner_radius=0, width=36, height=36)
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="H", font=FONT_HEADING_SM, text_color=NEON_CYAN).place(
            relx=0.5, rely=0.5, anchor="center")

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(title_frame, text="ACTIVITY LOG", font=FONT_HEADING_SM,
                     text_color=TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="SESSION ENCRYPTION HISTORY",
                     font=FONT_TINY, text_color=TEXT_MUTED).pack(anchor="w")

        NeonButton(header, text="REFRESH", color=NEON_CYAN, width=100, height=32,
                   command=self.refresh).pack(side="right")

        # Table header
        table_header = ctk.CTkFrame(self, fg_color=VOID_700, corner_radius=0, height=30)
        table_header.pack(fill="x", pady=(0, 2))
        table_header.pack_propagate(False)

        cols = [("TIME", 80), ("ACTION", 100), ("ALGORITHM", 110),
                ("TYPE", 70), ("STATUS", 80), ("DETAILS", 300)]
        for text, width in cols:
            ctk.CTkLabel(
                table_header, text=text, font=FONT_TINY, text_color=TEXT_MUTED,
                width=width, anchor="w",
            ).pack(side="left", padx=(8, 0))

        # Scrollable rows
        self.rows_frame = ctk.CTkScrollableFrame(
            self, fg_color=VOID_900, corner_radius=0,
            scrollbar_button_color=NEON_CYAN_DIM,
            scrollbar_button_hover_color=NEON_CYAN,
        )
        self.rows_frame.pack(fill="both", expand=True)

        self.refresh()

    def refresh(self):
        for w in self.rows_frame.winfo_children():
            w.destroy()

        history = self.engine.get_history()

        if not history:
            empty = ctk.CTkFrame(self.rows_frame, fg_color="transparent")
            empty.pack(fill="both", expand=True, pady=60)
            ctk.CTkLabel(empty, text="[ EMPTY ]", font=FONT_HEADING_SM,
                         text_color=TEXT_DIM).pack()
            ctk.CTkLabel(empty, text="No activity recorded yet", font=FONT_MONO,
                         text_color=TEXT_DIM).pack(pady=(8, 0))
            ctk.CTkLabel(empty, text="Encrypt or decrypt data to see activity here",
                         font=FONT_TINY, text_color=TEXT_DIM).pack()
            return

        for item in history:
            row = ctk.CTkFrame(self.rows_frame, fg_color="transparent",
                               corner_radius=0, height=32)
            row.pack(fill="x", pady=(0, 1))
            row.pack_propagate(False)

            # Status color for row border
            status = item.get("status", "")
            if status == "success":
                border_color = NEON_GREEN
                status_color = NEON_GREEN
            elif status == "failed":
                border_color = NEON_RED
                status_color = NEON_RED
            else:
                border_color = NEON_YELLOW
                status_color = NEON_YELLOW

            # Left accent bar
            accent = ctk.CTkFrame(row, fg_color=border_color, width=2, corner_radius=0)
            accent.pack(side="left", fill="y")

            # Time
            ctk.CTkLabel(
                row, text=item.get("timestamp", ""), font=FONT_TINY,
                text_color=TEXT_MUTED, width=80, anchor="w",
            ).pack(side="left", padx=(8, 0))

            # Action
            action = item.get("action", "").upper()
            action_colors = {"ENCRYPT": NEON_CYAN, "DECRYPT": NEON_GREEN, "VERIFY": NEON_PURPLE}
            ctk.CTkLabel(
                row, text=action, font=FONT_TINY,
                text_color=action_colors.get(action, TEXT_MUTED), width=100, anchor="w",
            ).pack(side="left", padx=(8, 0))

            # Algorithm
            ctk.CTkLabel(
                row, text=item.get("algorithm", ""), font=FONT_TINY,
                text_color=NEON_CYAN, width=110, anchor="w",
            ).pack(side="left", padx=(8, 0))

            # Type
            ctk.CTkLabel(
                row, text=item.get("input_type", "").upper(), font=FONT_TINY,
                text_color=TEXT_MUTED, width=70, anchor="w",
            ).pack(side="left", padx=(8, 0))

            # Status
            ctk.CTkLabel(
                row, text=status.upper(), font=FONT_TINY,
                text_color=status_color, width=80, anchor="w",
            ).pack(side="left", padx=(8, 0))

            # Details
            ctk.CTkLabel(
                row, text=item.get("details", ""), font=FONT_TINY,
                text_color=TEXT_DIM, width=300, anchor="w",
            ).pack(side="left", padx=(8, 0))


# Need the dim constant
NEON_CYAN_DIM = "#005F66"
NEON_CYAN = "#00F3FF"
