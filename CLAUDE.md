# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BeancountAutocomplete is a Sublime Text plugin that provides intelligent autocomplete for Beancount account names. It scans a configured Beancount file for `open` directives, caches the discovered accounts, and provides them as autocomplete suggestions while editing Beancount files.

## Architecture

### Core Components

**beancount_autocomplete.py** - The single-file plugin implementation
- `BeancountAutocompleteListener`: Sublime Text EventListener that hooks into the editor's autocomplete system
- Account caching: Loads accounts from the configured Beancount file, with file modification time-based cache invalidation
- Regex pattern matching: Uses `(?:[A-Z][A-Za-z0-9-]+)(?::[A-Z][A-Za-z0-9-]+)+` to extract hierarchical account names (e.g., `Assets:Checking`, `Expenses:Food`)

### Plugin Flow

1. User triggers autocomplete in Sublime Text
2. `on_query_completions()` is called
3. Plugin checks if accounts need reloading (file modification time check)
4. If stale, `load_accounts()` reads the Beancount file and extracts account names from `open` directives
5. Accounts are filtered by the current prefix and returned as completions

### Configuration

**BeancountAutocomplete.sublime-settings** - User configuration file
- `beancount_file`: Absolute path to the user's main Beancount ledger file
- This path must be configured by each user in their Sublime Text settings

## Development Commands

### Testing the Plugin

Since this is a Sublime Text plugin, testing requires loading it into Sublime Text:

1. Place the plugin files in Sublime's Packages directory:
   - macOS: `~/Library/Application Support/Sublime Text/Packages/BeancountAutocomplete/`
   - Linux: `~/.config/sublime-text/Packages/BeancountAutocomplete/`
   - Windows: `%APPDATA%\Sublime Text\Packages\BeancountAutocomplete\`

2. Configure the plugin in Sublime Text preferences:
   ```json
   {
       "beancount_file": "/path/to/your/accounts.beancount"
   }
   ```

3. View plugin output/errors:
   - Open Sublime Text console: `View -> Show Console` or `` Ctrl+` ``
   - Python exceptions and print statements appear here

4. Reload the plugin after changes:
   - Open command palette (`Cmd+Shift+P` / `Ctrl+Shift+P`)
   - Run "Plugin Development: Reload Plugin"
   - Or restart Sublime Text

### No Build/Test Commands

This project has no automated tests or build commands. Testing is manual via Sublime Text.

## Key Implementation Details

### Account Name Regex

The pattern `(?:[A-Z][A-Za-z0-9-]+)(?::[A-Z][A-Za-z0-9-]+)+` matches Beancount's account naming convention:
- Must start with uppercase letter
- Hierarchical structure with colon separators
- Each segment starts with uppercase, contains letters/numbers/hyphens
- Examples: `Assets:Bank:Checking`, `Liabilities:CreditCard`, `Income:Salary`

### Caching Strategy

The plugin caches parsed accounts to avoid re-parsing the Beancount file on every keystroke. Cache invalidation uses `os.path.getmtime()` to detect file modifications. This is crucial for performance on large Beancount files (thousands of lines).

### Prioritizing `open` Directives

While account names appear throughout a Beancount file (in transactions, balance assertions, etc.), the plugin specifically looks for lines containing " open " to extract the canonical account definitions. This produces a cleaner list of valid accounts.

## Project Management

This project uses `bd` (beads) for issue tracking. See AGENTS.md for workflow details.

## Distribution

This plugin is intended for distribution via Sublime Text's Package Control:
- Requires a GitHub repository
- Needs semantic versioning via Git tags (e.g., `v1.0.0`)
- Submitted to the Package Control channel for public availability
