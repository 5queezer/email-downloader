# IMAP Email Downloader

A Python-based tool to download emails from an IMAP server and save them to a directory while also providing some additional features related to email analysis.

## Features

- **Download emails**: Easily connect and fetch emails from any IMAP server.
- **Save to Directory**: Specify a directory where emails are saved.
- **Clear Directory**: Has an option to delete directory contents before downloading new emails.
- **Overwrite Option**: Decide whether to overwrite existing files in the target directory.
- **Analyze Emails**: Extract and count the number of emails from senders and tally unsubscribe links.
- **Generate Report**: Produce a CSV report containing details of senders.

## Dependencies

This tool leverages several external libraries including:

- `imap_tools`: For interacting with IMAP servers and fetching emails.
- `tqdm`: To show a progress bar when downloading emails.
- `click`: Facilitates creating a user-friendly command-line interface.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install Required Libraries**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Execute the main script:

```bash
python3 main.py
```

Upon running, you'll be prompted to input several details such as the IMAP host, username, password, and a directory for saving the emails. Follow the on-screen prompts and options.

### Command Line Options

- `--host`: Specify the IMAP server host. This is a required field.
- `--user`: Your IMAP server username or email. Also required.
- `--password`: Your IMAP server password. This will be hidden as you type.
- `--directory`: Choose a directory to save the downloaded emails. If not provided, it defaults to the format `username@host`.
- `--delete-contents`: Decide if you want to clear the save directory before downloading. Defaults to False.
- `--overwrite`: Decide whether to overwrite files in the save directory if they already exist. Defaults to True.

## License

This project and its contents are open source and are licensed under the MIT License. Kindly check the `LICENSE` file in the repository for more details.

## Contributing

We welcome contributions to this project. If you have improvements, features, or bug fixes, kindly follow our contributing guidelines and submit a pull request.

## Get in Touch

If you have queries, feedback, or suggestions related to this tool, kindly open an issue on this GitHub repository, and we'll get back to you.

---

Please ensure you replace placeholders like `<repository_url>` and `<repository_name>` with the actual details of your repository.