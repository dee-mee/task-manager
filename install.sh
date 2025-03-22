#!/bin/bash

# Create directories
sudo mkdir -p /usr/local/bin/TaskManager
sudo mkdir -p /usr/local/share/icons
sudo mkdir -p /usr/local/share/applications

# Copy application files
sudo cp -r dist/TaskManager/* /usr/local/bin/TaskManager/

# Convert and copy icon
sudo convert todo_app.svg -resize 256x256 /usr/local/share/icons/taskmanager.png

# Create desktop entry
cat << EOF | sudo tee /usr/local/share/applications/taskmanager.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=Task Manager
Comment=Personal Task Management Application
Exec=/usr/local/bin/TaskManager/TaskManager
Icon=/usr/local/share/icons/taskmanager.png
Terminal=false
Categories=Utility;Office;
EOF

# Set permissions
sudo chmod +x /usr/local/bin/TaskManager/TaskManager
sudo chmod 644 /usr/local/share/applications/taskmanager.desktop
sudo chmod 644 /usr/local/share/icons/taskmanager.png

# Update desktop database
sudo update-desktop-database /usr/local/share/applications/

echo "Installation complete! You can now find Task Manager in your applications menu."
