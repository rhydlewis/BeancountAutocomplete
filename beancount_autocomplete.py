import sublime
import sublime_plugin
import re
import os

class BeancountAutocompleteListener(sublime_plugin.EventListener):
    def __init__(self):
        self.accounts_cache = []
        self.last_load_time = 0

    def get_settings(self):
        return sublime.load_settings("BeancountAutocomplete.sublime-settings")

    def load_accounts(self):
        settings = self.get_settings()
        file_path = settings.get("beancount_file")
        
        # print(f"Checking path: {file_path}") # DEBUG LINE

        if not file_path or not os.path.exists(file_path):
            # print("File path not found!") # DEBUG LINE
            return []

        # Cache check: only reload if the file has been modified
        mtime = os.path.getmtime(file_path)
        if mtime <= self.last_load_time:
            return self.accounts_cache

        accounts = set()
        # Regex to find account names in 'open' directives or transactions
        # Matches: Assets:Checking, Expenses:Food, etc.
        account_pattern = re.compile(r'(?:[A-Z][A-Za-z0-9-]+)(?::[A-Z][A-Za-z0-9-]+)+')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # Prioritize 'open' directives for cleaner extraction
                    if " open " in line:
                        match = account_pattern.search(line)
                        if match:
                            accounts.add(match.group())
        except Exception as e:
            print(f"Beancount Autocomplete Error: {e}")

        self.accounts_cache = sorted(list(accounts))
        self.last_load_time = mtime
        return self.accounts_cache

    def on_query_completions(self, view, prefix, locations):
        # Only trigger for beancount files or if we are in a likely account position
        # You can refine this by checking view.scope_name(locations[0]) 
        # if you use a Beancount syntax package.
        
        accounts = self.load_accounts()
        if not accounts:
            return None

        # Format for Sublime's autocomplete: (trigger, insertion_text)
        completions = [
            (account + "\tAccount", account) 
            for account in accounts 
            if prefix.lower() in account.lower()
        ]

        return (completions, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)