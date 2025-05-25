import tkinter as tk

class ToolTip:
    def __init__(self, widget : tk.Widget, text : str) -> None:
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event: tk.Event = None) -> None:
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw, text=self.text, background="lightyellow", relief="solid", borderwidth=1,
            font=("tahoma", "9", "normal")
        )
        label.pack(ipadx=4, ipady=2)

    def hide_tip(self, event : tk.Event =None) -> None:
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
