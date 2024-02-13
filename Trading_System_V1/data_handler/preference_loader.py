import tkinter as tk
from gui_manager import GUIManager
from csv_loader import CSVLoader
from selection_manager import SelectionManager
from search_manager import SearchManager


def main():
    try:
        root = tk.Tk()
        root.title("Security Search Application")
        root.geometry("800x600")

        # Initialize the CSV loader with the root Tkinter object
        csv_loader = CSVLoader(root)
        # Initialize the selection manager
        selection_manager = SelectionManager()
        # Initialize the search manager with the root Tkinter object
        search_manager = SearchManager(root)

        # Create the GUI manager with all the components
        app = GUIManager(root, csv_loader, selection_manager, search_manager)

        # Start the Tkinter event loop
        root.mainloop()

    except Exception as e:
        print(f"An error occurred during initialization: {e}")


if __name__ == "__main__":
    main()
