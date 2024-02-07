#!/bin/bash

# Set the path to the source files
SRC_DIR="src"

# Set the destination directory for installation
DEST_DIR="/usr/bin"

# Copy the main.py file to the destination directory
if cp "$SRC_DIR/main.py" "$DEST_DIR/Youtube-Downloader"; then
    echo "Main script copied successfully to $DEST_DIR/Youtube-Downloader"
else
    echo "Error: Failed to copy main script to $DEST_DIR/Youtube-Downloader" >&2
    exit 1
fi

# Set executable permissions for the main.py file
if chmod +x "$DEST_DIR/Youtube-Downloader"; then
    echo "Executable permissions set for $DEST_DIR/Youtube-Downloader"
else
    echo "Error: Failed to set executable permissions for $DEST_DIR/Youtube-Downloader" >&2
    exit 1
fi

# Install Python dependencies from requirements.txt
if pip3 install -r "$SRC_DIR/requirements.txt"; then
    echo "Python dependencies installed successfully"
else
    echo "Error: Failed to install Python dependencies" >&2
    exit 1
fi

# Copy the icon file to a suitable location
ICON_DEST_DIR="/usr/share/icons"
ICON_SRC="$SRC_DIR/logo.ico"

# Create the directory if it doesn't exist
mkdir -p "$ICON_DEST_DIR"

# Copy the icon file
if cp "$ICON_SRC" "$ICON_DEST_DIR/logo.ico"; then
    echo "Icon file copied successfully to $ICON_DEST_DIR/logo.ico"
else
    echo "Error: Failed to copy icon file to $ICON_DEST_DIR/logo.ico" >&2
    exit 1
fi

# Output success message
echo "YourApp has been installed successfully!"
