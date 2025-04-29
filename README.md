# gitdater

A Python script that recursively finds and updates multiple Git repositories. Ideal for maintaining multiple pentest tools or other Git-based projects.

## Warning

Use this project at your own risk. The author is not responsible for any data loss, repository corruption, or other issues. Ensure you have proper backups before using this script.

## Features

- Recursively finds and updates all Git repositories in a directory
- Parallel repository updates for speed (optional)
- Automatically handles merge conflicts with interactive prompts
- Command-line arguments for customization
- Verbose output option for debugging

## Requirements

- Python 3.6+
- Git installed and in PATH

## Usage

Basic usage:

```bash
python3 gitdater.py
```

Advanced options:

```bash
python3 gitdater.py [-h] [-d DIRECTORY] [-p] [-m MAX_WORKERS] [-v] [-y]
```

### Command-line arguments

- `-h, --help`: Show help message
- `-d, --directory`: Root directory to search for git repositories (default: current directory)
- `-p, --parallel`: Update repositories in parallel
- `-m, --max-workers`: Maximum number of parallel workers (default: 5)
- `-v, --verbose`: Verbose output
- `-y, --yes`: Answer yes to all prompts

## Examples

Update all repositories in the current directory:
```bash
python3 gitdater.py
```

Update repositories in parallel with verbose output:
```bash
python3 gitdater.py -p -v
```

Update all repositories in a specific directory, automatically accept all prompts:
```bash
python3 gitdater.py -d /home/user/pentesting-tools -y
```

### Sample Output From "Pentesting Tools" Folder:

```
Searching for git repositories in /home/user/pentesting-tools...

Found 42 git repositories.

Checking updates for "/home/user/pentesting-tools/credmap"...
Already at the latest revision 'f28e46e'.

Checking updates for "/home/user/pentesting-tools/ntdsxtract"...
Updated to the latest revision '7fa1c8c'.

Checking updates for "/home/user/pentesting-tools/PowerSploit"...
Updated to the latest revision '262a260'.

Checking updates for "/home/user/pentesting-tools/sqlmap"...
Updated to the latest revision '7cca56e'.

Completed updating 42 repositories.
```
