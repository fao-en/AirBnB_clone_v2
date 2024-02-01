#!/usr/bin/python3
# Fabfile to generate a .tgz archive from the contents of web_static.
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """
    Create a tar gzipped archive of the directory web_static.

    Returns:
        str: Path to the generated archive on success, None on failure.
    """
    # Get the current UTC time
    dt = datetime.utcnow()

    # Generate a filename based on the current date and time
    file_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                              dt.month,
                                                              dt.day,
                                                              dt.hour,
                                                              dt.minute,
                                                              dt.second)

    # Create the 'versions' directory if it doesn't exist
    if os.path.isdir("versions") is False:
        # Create 'versions' directory, return None on failure
        if local("mkdir -p versions").failed is True:
            return None

    # Create a tar gzipped archive of the 'web_static' directory
    if local("tar -cvzf {} web_static".format(file_name)).failed is True:
        return None

    # Return the path to the generated archive
    return file_name
