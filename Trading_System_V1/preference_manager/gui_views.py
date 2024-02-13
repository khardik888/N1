import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from gui_widgets import CSVSelectionCombobox, DataViewTable, PreferenceTextView, SearchEntry, RemoveSelectionButton
from search_manager import SearchManager
from csv_creator import CSVLoader
from selection_manager import SelectionManager
class MainFrameView(tk.Frame):
    def __init__(self, parent, csv_loader, **kwargs):
        super().__init__(parent, **kwargs)
        self.csv_loader = csv_loader

        # Create and place all widgets
        self.csv_dropdown = CSVSelectionCombobox(self, self.csv_loader)
        self.csv_dropdown.pack(pady=10)

        self.data_view_table = DataViewTable(self)
        self.data_view_table.pack(expand=True, fill=tk.BOTH, pady=10)

        self.preference_text_view = PreferenceTextView(self)
        self.preference_text_view.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

        self.remove_selection_button = RemoveSelectionButton(self)
        self.remove_selection_button.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

        self.search_entry = SearchEntry(self)
        self.search_entry.pack(side=tk.TOP, fill=tk.X, expand=True, pady=(0, 5))
class GUIManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automated Trading System: Security Master Management")
        self.geometry("800x600")

        self.csv_loader = CSVLoader()
        self.selection_manager = SelectionManager()
        self.search_manager = SearchManager(self)

        self.main_frame_view = MainFrameView(self)
        self.setup_bindings()

    def setup_bindings(self):
        self.main_frame_view.csv_dropdown.bind("<<ComboboxSelected>>", self.on_csv_selected)
        self.main_frame_view.data_view_table.bind('<<TreeviewSelect>>', self.on_selection_changed)
        self.main_frame_view.search_entry.bind('<KeyRelease>', self.on_search)
        self.main_frame_view.remove_selection_button['command'] = self.remove_selected_items

    def on_csv_selected(self, event=None):
        selected_csv = self.main_frame_view.csv_dropdown.get()
        df = self.csv_loader.load_csv_to_df(selected_csv)
        self.main_frame_view.data_view_table.set_dataframe(df)

    def on_search(self, event):
        search_term = self.main_frame_view.search_entry.get()
        filtered_df = self.search_manager.search(search_term, self.csv_loader.df)
        self.main_frame_view.data_view_table.set_dataframe(filtered_df)

    def on_selection_changed(self, event):
        selected_items = self.main_frame_view.data_view_table.selection()
        selected_indices = [self.main_frame_view.data_view_table.item(item, 'values')[0] for item in selected_items]
        self.selection_manager.update_selections(selected_indices)
        self.display_preferences()

    def display_preferences(self):
        preferences = self.selection_manager.fetch_preferences()
        self.main_frame_view.preference_text_view.delete(1.0, tk.END)
        for preference in preferences:
            self.main_frame_view.preference_text_view.insert(tk.END, f"{preference}\n")

    def remove_selected_items(self):
        selected_items = self.main_frame_view.data_view_table.selection()
        self.selection_manager.remove_selections([item for item in selected_items])
        self.display_preferences()

if __name__ == "__main__":
    app = GUIManager()
    app.mainloop()
