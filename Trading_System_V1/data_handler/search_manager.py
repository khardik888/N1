import threading
import re

class SearchManager:
    def __init__(self, root):
        self.search_debounce_timer = None
        self.root = root  # Save the root to schedule callbacks in the main thread

    def debounced_search(self, search_term, dataframe, callback):
        if self.search_debounce_timer is not None:
            self.search_debounce_timer.cancel()
        self.search_debounce_timer = threading.Timer(0.5, self.perform_search, [search_term, dataframe, callback])
        self.search_debounce_timer.start()

    def perform_search(self, search_term, dataframe, callback):
        if not dataframe.empty and search_term:
            # Escape regex special characters in search term
            search_term = re.escape(search_term)
            string_df = dataframe.select_dtypes(include=[object, "string"]).fillna('')
            mask = string_df.apply(lambda col: col.str.contains(search_term, case=False, regex=True)).any(axis=1)
            filtered_df = dataframe[mask]
        else:
            filtered_df = dataframe
        # Ensure the callback is executed in the main thread
        self.root.after(0, lambda: callback(filtered_df))
