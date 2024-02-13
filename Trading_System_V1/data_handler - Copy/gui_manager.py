import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import pandas as pd

# Ensure that the following modules are correctly implemented and imported
from search_manager import SearchManager
from csv_loader import CSVLoader
from selection_manager import SelectionManager

class GUIManager:
    def __init__(self, root, csv_loader, selection_manager, search_manager):
        self.root = root
        self.csv_loader = csv_loader
        self.selection_manager = selection_manager
        self.search_manager = search_manager
        self.setup_ui()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.csv_label = ttk.Label(self.main_frame, text="Select CSV file:")
        self.csv_label.pack(side=tk.TOP, anchor='w', pady=(0, 5))

        self.csv_dropdown = ttk.Combobox(self.main_frame, state='readonly', width=50)
        self.csv_dropdown['values'] = self.csv_loader.load_csv_files()
        self.csv_dropdown.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        self.csv_dropdown.bind('<<ComboboxSelected>>', self.on_csv_selected)

        self.search_label = ttk.Label(self.main_frame, text="Search:")
        self.search_label.pack(side=tk.TOP, anchor='w', pady=(5, 5))

        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(side=tk.TOP, fill=tk.X)

        self.search_entry = ttk.Entry(search_frame, textvariable=tk.StringVar())
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(0, 5))
        self.search_entry.bind('<KeyRelease>', self.on_search)

        self.table = ttk.Treeview(self.main_frame, show='headings', selectmode='extended')
        self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 5))
        self.table.bind('<<TreeviewSelect>>', self.on_selection_changed)

        self.v_scroll = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.table.yview)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.configure(yscrollcommand=self.v_scroll.set)

        self.h_scroll = ttk.Scrollbar(self.main_frame, orient="horizontal", command=self.table.xview)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.table.configure(xscrollcommand=self.h_scroll.set)

        self.preference_label = ttk.Label(self.main_frame, text="Selected Preferences:")
        self.preference_label.pack(side=tk.TOP, anchor='w', pady=(5, 5))

        self.preference_text = tk.Text(self.main_frame, height=5)
        self.preference_text.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

        self.remove_button = ttk.Button(self.main_frame, text="Remove Selection", command=self.remove_selected_items)
        self.remove_button.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

        # Set a style for selected rows for better visibility
        style = ttk.Style(self.root)
        style.map('Treeview', background=[('selected', '#e1e1e1')])  # Light grey background

    def on_csv_selected(self, event):
        selected_csv = self.csv_dropdown.get()
        self.csv_loader.load_csv_to_df_async(selected_csv, self.update_table)

    def on_search(self, event):
        search_term = self.search_entry.get()
        if search_term:
            self.search_manager.debounced_search(search_term, self.csv_loader.df, self.update_table)
        else:
            self.display_table(self.csv_loader.df)

    def update_table(self, dataframe):
        self.display_table(dataframe)

    def display_table(self, dataframe):
        self.table.delete(*self.table.get_children())
        if dataframe is not None and not dataframe.empty:
            self.table['columns'] = dataframe.columns.tolist()

            for col in dataframe.columns:
                self.table.heading(col, text=col, anchor='center')
                self.table.column(col, anchor='center', width=tkfont.Font().measure(col.title()))

            for row in dataframe.itertuples(index=True, name=None):
                self.table.insert("", "end", values=row[1:])

            self.adjust_column_widths(dataframe)

    def adjust_column_widths(self, dataframe):
        for col in dataframe.columns:
            col_width = max(self.table.column(col, 'width'), max([len(str(val)) for val in dataframe[col]]) * 6)
            self.table.column(col, width=col_width)

    def on_selection_changed(self, event):
        selected_items = self.table.selection()
        selected_indices = [self.table.item(item, 'values')[0] for item in selected_items]
        self.selection_manager.update_selections(selected_indices)
        self.display_preferences()
        self.save_preferences_to_file()

    def display_preferences(self):
        preferences = self.selection_manager.fetch_preferences(self.csv_loader.df)
        self.preference_text.delete(1.0, tk.END)
        for idx, preference in enumerate(preferences, 1):
            self.preference_text.insert(tk.END, f"{idx}. {preference}\n")

    def remove_selected_items(self):
        selected_items = self.table.selection()
        selected_indices = [self.table.item(item, 'values')[0] for item in selected_items]
        self.selection_manager.remove_selections(selected_indices)
        self.display_preferences()
        self.save_preferences_to_file()

    def save_preferences_to_file(self):
        preferences = self.selection_manager.fetch_preferences(self.csv_loader.df)
        self.selection_manager.save_preferences(preferences)