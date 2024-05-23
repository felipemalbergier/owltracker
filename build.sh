pyinstaller main.py \
--onefile \
--hidden-import plyer.platforms.win.notification \
--exclude-module tkinter

# pyinstaller downloader_backend.py --distpath electron_ui\python_build --workpath %TEMP% --exclude-module tkinter --onefile --noconsole --hidden-import plyer.platforms.win.notification

# activate otification on windows
# https://support.microsoft.com/en-gb/windows/change-notification-settings-in-windows-8942c744-6198-fe56-4639-34320cf9444e#WindowsVersion=Windows_11