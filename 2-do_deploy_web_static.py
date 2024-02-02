#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run

# List of web server IP addresses
env.hosts = ["52.87.28.205", "34.229.69.104"]


def do_deploy(archive_path):
    """Distributes an archive to a web server."""
    if not os.path.isfile(archive_path):
        return False

    # Extract the file and directory names
    file_name = archive_path.split("/")[-1]
    name = file_name.split(".")[0]

    # Upload the archive to the server's /tmp/ directory
    if put(archive_path, "/tmp/{}".format(file_name)).failed:
        return False

    # Remove the existing release directory
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
        return False

    # Create a new release directory
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False

    if run("tar -xzf /tmp/{} -C/data/web_static/releases/{}/"
           .format(file_name, name)).failed:
        return False

    # Remove the temporary archive file
    if run("rm /tmp/{}".format(file_name)).failed:
        return False

    # Move the contents of web_static to the release directory
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".
           format(name, name)).failed:
        return False

    # Remove the web_static directory within the release directory
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed:
        return False

    # Remove the current symbolic link
    if run("rm -rf /data/web_static/current").failed:
        return False

    # Create a new symbolic link pointing to the latest release
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed:
        return False

    # Deployment successful
    return True
