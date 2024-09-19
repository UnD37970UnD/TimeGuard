> [!CAUTION]
> Work in progress

# TimeGuard

TimeGuard is a parental control application built with Python and Tkinter. It allows parents to manage screen time and control access to user accounts on a Windows PC. The application features a modular interface with an admin panel for configuration and a user panel for regular use.

## Features

- **Admin Panel**: Configure settings and manage user accounts.
- **User Panel**: Access for regular users with restrictions based on admin settings.
- **System Tray Integration**: Minimize the application to the system tray for easy access.
- **Password Protection**: Admin actions are secured with a password.


## Configuration

On the first run, the application will prompt you to set an admin password. This password is required to access the admin panel.
Usage

    Switch Between Frames:
        Use the switch button at the bottom to toggle between the User and Admin panels.

    Admin Panel:
        Enter the admin password to access the configuration settings.

    User Panel:
        Regular users interact with the system as configured by the admin.

    System Tray:
        Minimize the application to the system tray. Right-click on the tray icon to restore or quit the application.

## File Structure

    main.py: Main application file that initializes the Tkinter window and manages frame switching.
    config_screen.py: Frame for configuring settings and setting the admin password.
    admin_frame.py: Frame for entering the admin password and accessing the admin panel.
    user_frame.py: Frame for the regular user interface.
    admin_panel.py: Admin panel with tabs for managing user settings and time limits.
    system_tray.py: Manages system tray icon and interactions.
    database.py: Handles database setup and operations.

## Known issues

    - The password field remains populated when switching from the User frame to the Admin frame if the Submit button has not been pressed.



## License

This project is licensed under the MIT License. See the LICENSE file for more details.
## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.
## Contact

For any questions or issues, please contact [iustin@notiustin.com](mailto:iustin@notiustin.com)
