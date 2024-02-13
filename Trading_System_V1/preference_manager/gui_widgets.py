import tkinter as tk
from tkinter import ttk


# Custom combobox for CSV file selection
class CSVSelectionCombobox(ttk.Combobox):
    def __init__(self, parent, csv_loader, **kwargs):
        super().__init__(parent, state="readonly", **kwargs)
        self.csv_loader = csv_loader
        self['values'] = self.csv_loader.load_csv_files()


# Custom table for viewing data
class DataViewTable(ttk.Treeview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, show="headings", selectmode='browse', **kwargs)
        # Assuming you want vertical and horizontal scrollbars
        self.v_scroll = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.v_scroll.pack(side="right", fill="y")
        self.configure(yscrollcommand=self.v_scroll.set)

        self.h_scroll = ttk.Scrollbar(parent, orient="horizontal", command=self.xview)
        self.h_scroll.pack(side="bottom", fill="x")
        self.configure(xscrollcommand=self.h_scroll.set)

    def set_dataframe(self, dataframe):
        self.delete(*self.get_children())
        self['columns'] = list(dataframe.columns)
        for col in dataframe.columns:
            self.heading(col, text=col)
            self.column(col, width=100)  # Default width, modify as needed
        for row in dataframe.itertuples(index=False, name=None):
            self.insert('', 'end', values=row)


# Custom text view for preferences
class PreferenceTextView(tk.Text):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)


# Custom entry for search functionality
class SearchEntry(ttk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)


# Custom button for removing selections
class RemoveSelectionButton(ttk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="Remove Selection", **kwargs)
