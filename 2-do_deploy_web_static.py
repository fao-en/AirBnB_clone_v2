#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run, warn

# List of web server IP addresses
env.hosts = ["52.87.28.205", "34.229.69.104"]


def do_deploy(archive_path):
    """Distributes an archive to a web server."""
    if not os.path.isfile(archive_path):
        warn(f"Error: Archive file '{archive_path}' does not exist.")
        return False

    # Extract the file and directory names
    file_name = archive_path.split("/")[-1]
    name = file_name.split(".")[0]

    try:
        # Upload the archive to the server's /tmp/ directory
        put(archive_path, "/tmp/{}".format(file_name))

        # Create a new release directory
        run("mkdir -p /data/web_static/releases/{}/".format(name))

        # Extract the archive to the new release directory
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, name))

        # Remove the temporary archive file
        run("rm /tmp/{}".format(file_name))

        # Move the contents of web_static to the new release directory
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name))

        # Remove the web_static directory within the release directory
        run("rm -rf /data/web_static/releases/{}/web_static".format(name))

        # Remove the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link pointing to the latest release
        run("ln -sfn /data/web_static/releases/{}/ /data/web_static/current".format(name))

        # Deployment successful
        return True

    except Exception as e:
        warn(f"An error occurred during deployment: {e}")
        return False
