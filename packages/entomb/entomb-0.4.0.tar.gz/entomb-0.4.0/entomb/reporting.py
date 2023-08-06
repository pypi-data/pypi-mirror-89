import datetime
import math
import os

from entomb import (
    constants,
    exceptions,
    utilities,
)


@utilities.hide_cursor()
def produce_report(path, include_git):
    """Print a report.

    Parameters
    ----------
    path : str
        An absolute path.
    include_git: bool
        Whether to include git files and directories.

    Returns
    -------
    None

    Raises
    ------
    AssertionError
        If the path does not exist.

    """
    # Parameter check.
    assert os.path.exists(path)

    # Set up.
    directory_count = 0
    immutable_file_count = 0
    inaccessible_file_count = 0
    link_count = 0
    mutable_file_count = 0

    # Print the operation.
    print("Produce report")
    print()

    # If the path is not a directory, print an abbreviated report then return.
    if not os.path.isdir(path):
        _print_abbreviated_report(path)
        return

    # Print the progress header and set up the progress bar.
    utilities.print_header("Progress")
    total_file_paths = utilities.count_file_paths(path, include_git)
    start_time = datetime.datetime.now()
    utilities.print_progress_bar(start_time, 0, total_file_paths)

    # Walk the tree.
    for root_dir, dirnames, filenames in os.walk(path):

        # Exclude git files and directories if directed.
        if not include_git:
            dirnames[:] = [d for d in dirnames if d != ".git"]

        # Count the directory.
        directory_count += 1

        # Examine each file path.
        for filename in filenames:
            file_path = os.path.join(root_dir, filename)

            # Count the link.
            if os.path.islink(file_path):
                link_count += 1

            # Count the file.
            else:
                try:
                    if utilities.file_is_immutable(file_path):
                        immutable_file_count += 1
                    else:
                        mutable_file_count += 1
                except exceptions.GetAttributeError:
                    inaccessible_file_count += 1

            # Update the progress bar.
            total_count = (
                immutable_file_count
                + inaccessible_file_count
                + link_count
                + mutable_file_count
            )
            utilities.print_progress_bar(
                start_time,
                total_count,
                total_file_paths,
            )

    print()
    print()

    _print_full_report(
        directory_count,
        link_count,
        immutable_file_count,
        inaccessible_file_count,
        mutable_file_count,
    )


def _print_abbreviated_report(path):
    """Print a report for a path which is not a directory.

    Parameters
    ----------
    path : str
        An absolute path.

    Returns
    -------
    None

    Raises
    ------
    AssertionError
        If the path is a directory or does not exist.

    """
    # Parameter check.
    assert not os.path.isdir(path)
    assert os.path.exists(path)

    utilities.print_header("Report")

    if os.path.islink(path):
        print("A link has no immutable attribute")
    else:
        try:
            if utilities.file_is_immutable(path):
                print("File is immutable")
            else:
                print("File is mutable")
        except exceptions.GetAttributeError:
            print("Immutable attribute could not be accessed")

    print()


def _print_full_report(directory_count, link_count, immutable_file_count,
                       inaccessible_file_count, mutable_file_count):
    """Print a report for a path which is a file or a link.

    Parameters
    ----------
    directory_count : int
        The number of directories counted.
    link_count : int
        The number of links counted.
    immutable_file_count : int
        The number of immutable files counted.
    inaccessible_file_count : int
        The number of files for which the immutability attribute could not be
        accessed.
    mutable_file_count : int
        The number of mutable files counted.

    Returns
    -------
    None

    """
    # Do calculations.
    subdirectory_count = directory_count - 1
    total_file_count = (
        immutable_file_count
        + inaccessible_file_count
        + mutable_file_count
    )

    try:
        entombed_proportion = immutable_file_count / total_file_count
        entombed_percentage_integer = math.floor(entombed_proportion * 100)
        entombed_percentage = "{}%".format(entombed_percentage_integer)
    except ZeroDivisionError:
        entombed_percentage = "n/a"

    # Print the report.
    _print_report_line("Report")
    _print_report_line("Entombed", entombed_percentage)
    if mutable_file_count:
        _print_report_line("Mutable files", _stringify_int(mutable_file_count))
    if inaccessible_file_count:
        _print_report_line(
            "Inaccessible files",
            _stringify_int(inaccessible_file_count),
        )
    _print_report_line("Total files", _stringify_int(total_file_count))
    if link_count:
        _print_report_line("Links", _stringify_int(link_count))
    if subdirectory_count:
        _print_report_line(
            "Sub-directories",
            _stringify_int(subdirectory_count),
        )
    print()


def _print_report_line(label, value=None):
    """Print a line in the full report followed by a separator line.

    Parameters
    ----------
    label : str
        The label to print on the left.
    value : str, optional
        The value, if any, to print on the right.

    Returns
    -------
    None

    """
    if value is None:
        print(label)
    else:
        value_width = constants.TABLE_WIDTH - (len(label) + 1)
        print(label, value.rjust(value_width))
    print("-" * constants.TABLE_WIDTH)


def _stringify_int(integer):
    """Convert an integer into a string formatted with thousand separators.

    Parameters
    ----------
    integer : int
        The integer.

    Returns
    -------
    str
        The integer turned into a string.

    """
    return "{:,}".format(integer)
