# Beancount Autocomplete

A Sublime Text plugin that provides intelligent autocomplete for Beancount account names.

## Features

- **Smart Account Discovery**: Automatically scans your Beancount file for account definitions
- **Cached Performance**: Intelligently caches accounts and only reloads when your Beancount file changes
- **Instant Completions**: Get autocomplete suggestions for all your accounts as you type
- **Hierarchical Account Support**: Handles Beancount's hierarchical account structure (e.g., `Assets:Bank:Checking`, `Expenses:Food:Groceries`)

## Installation

### Via Package Control (Recommended)

1. Open the Command Palette (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows/Linux)
2. Select "Package Control: Install Package"
3. Search for "BeancountAutocomplete"
4. Press Enter to install

### Manual Installation

1. Clone this repository into your Sublime Text Packages directory:

   **macOS:**
   ```bash
   cd ~/Library/Application\ Support/Sublime\ Text/Packages/
   git clone https://github.com/rhydlewis/BeancountAutocomplete.git
   ```

   **Linux:**
   ```bash
   cd ~/.config/sublime-text/Packages/
   git clone https://github.com/rhydlewis/BeancountAutocomplete.git
   ```

   **Windows:**
   ```bash
   cd %APPDATA%\Sublime Text\Packages\
   git clone https://github.com/rhydlewis/BeancountAutocomplete.git
   ```

2. Restart Sublime Text

## Configuration

To use this plugin, you must configure the path to your main Beancount file.

### Global Configuration

1. Open Sublime Text preferences: `Preferences → Settings`
2. Add the following configuration:

```json
{
    "beancount_file": "/absolute/path/to/your/accounts.beancount"
}
```

### Project-Specific Configuration

For project-specific settings, add to your `.sublime-project` file:

```json
{
    "folders": [
        {
            "path": "."
        }
    ],
    "settings": {
        "beancount_file": "/absolute/path/to/your/accounts.beancount"
    }
}
```

**Important:** The `beancount_file` path must be an absolute path, not a relative path.

## Usage

Once configured, the plugin works automatically:

1. Open any file in Sublime Text
2. Start typing an account name (e.g., `Assets:`)
3. Autocomplete suggestions will appear showing all matching accounts
4. Press `Tab` or `Enter` to insert the selected account

The plugin specifically looks for `open` directives in your Beancount file to build the list of valid accounts:

```beancount
2020-01-01 open Assets:Bank:Checking
2020-01-01 open Expenses:Food:Groceries
2020-01-01 open Income:Salary
```

## How It Works

- The plugin scans your configured Beancount file for account definitions
- Accounts are cached in memory for performance
- The cache automatically refreshes when your Beancount file is modified
- Only accounts from `open` directives are included for cleaner suggestions

## Requirements

- Sublime Text 3 or 4
- A Beancount ledger file

## Development

### Running Tests

The plugin includes a comprehensive test suite using Python's `unittest` framework. To run the tests:

```bash
python3 -m unittest tests.test_beancount_autocomplete -v
```

The tests cover:
- Account name regex pattern matching
- Loading accounts from Beancount files
- File caching behavior
- Completion filtering by prefix
- Case-insensitive matching
- Error handling for missing files

All tests use mocks for Sublime Text's API, so they can run independently without Sublime Text installed.

## Troubleshooting

### No completions appear

1. Verify your `beancount_file` setting points to the correct file path
2. Check that the file exists and is readable
3. Ensure your Beancount file contains `open` directives
4. View the Sublime Text console (`View → Show Console`) for any error messages

### Completions are outdated

The plugin caches accounts for performance. If you've added new accounts, they should appear automatically after saving your Beancount file. If not, restart Sublime Text.

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## About Beancount

[Beancount](https://github.com/beancount/beancount) is a double-entry bookkeeping system that uses plain text files. Learn more at [beancount.github.io](https://beancount.github.io/).
