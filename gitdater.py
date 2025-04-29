#!/usr/bin/env python3

import re
import argparse
import os
import sys
import concurrent.futures
from os import walk
from sys import stdout as sys_stdout
from subprocess import Popen, PIPE


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Update multiple git repositories at once"
    )
    parser.add_argument(
        "-d", "--directory", 
        default=".", 
        help="Root directory to search for git repositories (default: current directory)"
    )
    parser.add_argument(
        "-p", "--parallel", 
        action="store_true", 
        help="Update repositories in parallel"
    )
    parser.add_argument(
        "-m", "--max-workers", 
        type=int, 
        default=5, 
        help="Maximum number of parallel workers (default: 5)"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Verbose output"
    )
    parser.add_argument(
        "-y", "--yes", 
        action="store_true", 
        help="Answer yes to all prompts"
    )
    return parser.parse_args()


def run_git_command(command, cwd):
    """Run a git command and return its output."""
    process = Popen(command, cwd=cwd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode(), process.returncode


def update_repo(root, auto_yes=False, verbose=False):
    """
    Updates a git repository via git pull.
    Returns a tuple of (repo_path, success, message)
    """
    results = []
    
    if verbose:
        results.append(f"\"{root}\" checking for updates...")
    else:
        results.append(f"Checking updates for \"{root}\"...")

    # Check if we're on a branch
    branch_stdout, branch_stderr, branch_return_code = run_git_command("git symbolic-ref --short HEAD 2>/dev/null || echo 'DETACHED'", root)
    branch_name = branch_stdout.strip()
    
    if branch_name == 'DETACHED':
        stdout, stderr, return_code = run_git_command("git fetch && git merge --ff-only @{u}", root)
    else:
        stdout, stderr, return_code = run_git_command("git pull", root)
    
    success = not return_code

    if success:
        updated = "Already" not in stdout
        stdout, _, _ = run_git_command("git rev-parse --verify HEAD", root)
        revision = (stdout[:7] if stdout and
                    re.search(r"(?i)[0-9a-f]{32}", stdout) else "-")
        results.append(f"{('Already at' if not updated else 'Updated to')} the latest revision '{revision}'.")
    else:
        results.append("Problem occurred while updating repository.")

        match = re.search(r"error:.*files would be overwritten by merge", stderr)
        if match:
            results.append("Error: Files would be overwritten by merge.")

            if auto_yes or question(root):
                if "untracked" in stderr:
                    cmd = "git clean -df"
                else:
                    cmd = "git reset --hard"

                stdout, _, _ = run_git_command(cmd, root)

                if "HEAD is now at" in stdout:
                    results.append("\nLocal copy reset to current git branch.")
                    results.append("Attempting to run update again...\n")
                    
                    # Try updating again
                    _, success, new_message = update_repo(root, auto_yes, verbose)
                    results.append(new_message)
                else:
                    results.append("Unable to reset local copy to current git branch.")
            else:
                results.append("Update skipped by user.")
        else:
            # Check for detached HEAD state - various error messages
            detached_errors = [
                "You are not currently on a branch",
                "HEAD does not point to a branch",
                "detached HEAD"
            ]
            
            if any(error in stderr for error in detached_errors):
                results.append("Repository is in detached HEAD state.")
                # Try to fetch updates without merging
                fetch_stdout, fetch_stderr, _ = run_git_command("git fetch", root)
                results.append("Fetched updates but cannot merge (detached HEAD).")
                if verbose:
                    results.append(fetch_stdout)
                    if fetch_stderr.strip():
                        results.append(fetch_stderr)
            else:
                results.append("Please make sure that you have a 'git' package installed.")
            if verbose:
                results.append(stderr)

    return (root, success, "\n".join(results))


def question(repo_path):
    """Asks question until a valid answer of y or n is provided."""
    print(f"\nRepository: {repo_path}")
    print("Would you like to overwrite your changes and set "
          "your local copy to the latest commit?")
    sys_stdout.write("ALL of your local changes will be deleted"
                    " [Y/n]: ")
    answer = input()

    if not answer:
        answer = "y"

    if answer.lower() == "n":
        return False
    elif answer.lower() == "y":
        return True
    else:
        print("Did not understand your answer! Try again.")
        return question(repo_path)


def find_git_repos(root_dir):
    """Find all git repositories under the root directory."""
    git_repos = []
    
    for root, dirs, _ in walk(root_dir):
        if ".git" in dirs:
            git_repos.append(os.path.abspath(root))
            dirs.remove('.git')  # Don't recurse into .git directories
    
    return git_repos


def check_git_installed():
    """Check if git is installed and available."""
    try:
        process = Popen(["git", "--version"], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print("Error: Git not found. Please install git and try again.")
            return False
        return True
    except FileNotFoundError:
        print("Error: Git not found. Please install git and try again.")
        return False


def main():
    args = parse_args()
    
    # Check if git is installed
    if not check_git_installed():
        sys.exit(1)
    
    print(f"Searching for git repositories in {os.path.abspath(args.directory)}...\n")
    repos = find_git_repos(args.directory)
    
    if not repos:
        print("No git repositories found.")
        return
    
    print(f"Found {len(repos)} git repositories.\n")
    
    if args.parallel:
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            future_to_repo = {
                executor.submit(update_repo, repo, args.yes, args.verbose): repo 
                for repo in repos
            }
            for future in concurrent.futures.as_completed(future_to_repo):
                results.append(future.result())
        
        # Print results in original order
        for repo in repos:
            for result_repo, success, message in results:
                if result_repo == repo:
                    print(f"\n{message}")
                    break
    else:
        for repo in repos:
            _, _, message = update_repo(repo, args.yes, args.verbose)
            print(f"\n{message}")
            print()
    
    print(f"\nCompleted updating {len(repos)} repositories.")


if __name__ == "__main__":
    main()
