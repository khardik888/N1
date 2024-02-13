import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from search_manager import SearchManager
from csv_creator import CSVLoader
from selection_manager import SelectionManager

# GUI Components
class CSVSelectionCombobox(ttk.Combobox):
    def __init__(self, parent, csv_loader, *args, **kwargs):
        super().__init__(parent, state="readonly", *args, **kwargs)
        self.csv_loader = csv_loader
        self.initialize_values()

    def initialize_values(self):
        self['values'] = self.csv_loader.load_csv_files()

class DataViewTable(ttk.Treeview):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, show="headings", selectmode='browse', *args, **kwargs)
        self.config(yscrollcommand=ttk.Scrollbar(parent, orient="vertical", command=self.yview).set)
        self.config(xscrollcommand=ttk.Scrollbar(parent, orient="horizontal", command=self.xview).set)

    def set_dataframe(self, dataframe):
        self.delete(*self.get_children())
        self['columns'] = dataframe.columns.tolist()
        for col in dataframe.columns:
            self.heading(col, text=col, anchor='w')
            self.column(col, width=tkfont.Font().measure(col.title()))
        for row in dataframe.itertuples(index=False, name=None):
            self.insert("", "end", values=row)

class PreferenceTextView(tk.Text):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, height=5, *args, **kwargs)

class SearchEntry(ttk.Entry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, textvariable=tk.StringVar(), *args, **kwargs)

class RemoveSelectionButton(ttk.Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, text="Remove Selection", *args, **kwargs)

# Main GUI Application
class GUIManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automated Trading System: Security Master Management")
        self.geometry("800x600")

        # Initialize CSVLoader with the directory path from the configuration file
        self.csv_loader = CSVLoader(CSV_DIR)
        self.selection_manager = SelectionManager()
        self.search_manager = None  # Will be set once a CSV is selected

        self.setup_ui()
        self.setup_bindings()

    def setup_ui(self):
        self.csv_dropdown = CSVSelectionCombobox(self, self.csv_loader)
        self.csv_dropdown.pack(pady=10)

        self.data_view_table = DataViewTable(self)
        self.data_view_table.pack(expand=True, fill=tk.BOTH, pady=10)

        self.preference_text_view = PreferenceTextView(self)
        self.preference_text_view.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

        self.remove_selection_button = RemoveSelectionButton(self, command=self.remove_selected_items)
        self.remove_selection_button.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

        self.search_entry = SearchEntry(self)
        self.search_entry.pack(side=tk.TOP, fill=tk.X, expand=True, pady=(0, 5))

    def setup_bindings(self):
        self.csv_dropdown.bind("<<ComboboxSelected>>", self.on_csv_selected)
        self.data_view_table.bind('<<TreeviewSelect>>', self.on_selection_changed)
        self.search_entry.bind('<KeyRelease>', self.on_search)

    def on_csv_selected(self, event=None):
        selected_csv = self.csv_dropdown.get()
        self.csv_loader.load_csv_to_df(selected_csv)
        self.data_view_table.set_dataframe(self.csv_loader.df)
        # Initialize SearchManager with the loaded DataFrame
        self.search_manager = SearchManager(self.csv_loader.df)

    def on_search(self, event):
        search_term = self.search_entry.get()
        if self.search_manager:
            filtered_df = self.search_manager.search(search_term)
            self.data_view_table.set_dataframe(filtered_df)

    def on_selection_changed(self, event):
        selected_items = self.data_view_table.selection()
        selected_indices = [self.data_view_table.item(item, 'values')[0] for item in selected_items]
        self.selection_manager.update_selections(selected_indices)
        self.display_preferences()

    def display_preferences(self):
        preferences = self.selection_manager.fetch_preferences()
        self.preference_text_view.delete(1.0, tk.END)
        for preference in preferences:
            self.preference_text_view.insert(tk.END, f"{preference}\n")

    def remove_selected_items(self):
        selected_items = self.data_view_table.selection()
        self.selection_manager.remove_selections([item for item in selected_items])
        self.display_preferences()

if __name__ == "__main__":
    app = GUIManager()
    app.mainloop()