# Task Manager

A native Linux desktop application for managing your tasks and to-do lists.

## Features

- Add, edit, and delete tasks
- Set due dates with calendar picker
- Track task progress
- Set priority levels (Low, Medium, High)
- Track task status (Not Started, In Progress, Completed)
- Local SQLite database storage
- Native Linux GUI with PyQt6
- Clean and modern interface

## Installation

### System Requirements
- Linux (Ubuntu/Debian-based distributions)
- Python 3.12 or higher
- PyQt6
- SQLite3

### Install Dependencies

```bash
sudo apt-get update
sudo apt-get install python3-pyqt6
```

### Install Task Manager

1. Clone the repository:
```bash
git clone https://github.com/yourusername/task-manager.git
cd task-manager
```

2. Build and install the application:
```bash
sudo ./install.sh
```

### Launch the Application

1. From Applications Menu:
   - Search for "Task Manager" in your applications menu

2. From Terminal:
```bash
/usr/local/bin/TaskManager/TaskManager
```

## Usage

1. Launch the application from your applications menu
2. Click "Add Task" to create a new task
3. Fill in the task details:
   - Title (required)
   - Description
   - Due Date
   - Status (Not Started, In Progress, Completed)
   - Priority (Low, Medium, High)
   - Progress (0-100%)
4. Click "Save" to add the task
5. Edit or delete tasks using the action buttons in the task list

## Development

To run the application in development mode:

```bash
python3 desktop_app.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
