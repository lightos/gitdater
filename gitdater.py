#!/usr/bin/python

import re

from os import walk
from sys import stdout as sys_stdout
from subprocess import Popen, PIPE


def main():
    for root, dirs, _ in walk("."):
        if ".git" in dirs:
            print("\"%s\" has git dir: \"%s\"" % (root, dirs))
            dirs.remove('.git')

            update(root)
            print


def update(root):
    """
    Updates the program via git pull.
    """

    print("Checking for updates...")

    process = Popen("git pull", cwd=root, shell=True,
                    stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    success = not process.returncode

    if success:
        updated = "Already" not in stdout
        process = Popen("git rev-parse --verify HEAD", cwd=root, shell=True,
                        stdout=PIPE, stderr=PIPE)
        stdout, _ = process.communicate()
        revision = (stdout[:7] if stdout and
                    re.search(r"(?i)[0-9a-f]{32}", stdout) else "-")
        print("%s the latest revision '%s'." %
              ("Already at" if not updated else "Updated to", revision))
    else:
        print("Problem occurred while updating program.\n")

        _ = re.search(r"(?P<error>error:[^:]*files\swould\sbe\soverwritten"
                      r"\sby\smerge:(?:\n\t[^\n]+)*)", stderr)
        if _:
            def question():
                """Asks question until a valid answer of y or n is provided."""
                print("\nWould you like to overwrite your changes and set "
                      "your local copy to the latest commit?")
                sys_stdout.write("ALL of your local changes will be deleted"
                                 " [Y/n]: ")
                _ = raw_input()

                if not _:
                    _ = "y"

                if _.lower() == "n":
                    return False
                elif _.lower() == "y":
                    return True
                else:
                    print("Did not understand your answer! Try again.")
                    question()

            print("%s" % _.group("error"))

            if not question():
                return

            if "untracked" in stderr:
                cmd = "git clean -df"
            else:
                cmd = "git reset --hard"

            process = Popen(cmd, cwd=root, shell=True,
                            stdout=PIPE, stderr=PIPE)
            stdout, _ = process.communicate()

            if "HEAD is now at" in stdout:
                print("\nLocal copy reset to current git branch.")
                print("Attemping to run update again...\n")
            else:
                print("Unable to reset local copy to current git branch.")
                return

            update(root)
        else:
            print("Please make sure that you have a 'git' package installed.")
            print(stderr)


if __name__ == "__main__":
    main()
