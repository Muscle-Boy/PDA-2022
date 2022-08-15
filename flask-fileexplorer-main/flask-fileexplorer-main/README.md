A file explorer that works over local area network using Flask server. You can explore a computer's complete directory and download any file. Moreover, it also lets you stream videos or audio files if your browser supports it.

**Description**

Server works on,
- Windows
It is written in Python and tested it on Mac and Windows.

**Frameworks**
- Flask (Server)
- Bootstrap 4 

Flask has been used to run the server and serve up the html pages. Meanwhile, Bootstrap has been used to show the Folders and the Files. To open any folder, just click on it. To download any file, enter the path and click download.

**How to Run**

Make sure you have flask installed. You can use the following command to install flask,

    pip install -r requirements.txt
    
Now, open terminal/command prompt in the flask-fileexplorer directory and run the setup.py file by using the following command,

    python setup.py

You will have to configure the [config.json](config.json) file with your paths,

Example for Mac,

    "Favorites":    ["Users/boon_/Downloads","Users/boon_/Documents"],

Example for Windows,

    "Favorites":    ["C://Users//boon_//Documents","C://Users//boon_//Downloads"],


This should start the Flask Server in your terminal window. By default, it is run on port 80. You can access it by going to,
- **localhost** (on your server's browser)
- **(IP Address of your Server)** (from any other browser on the same network)

For additional features,

- **Password Protection**: Set a password in the config.json file.
- **Hiding Folders**: Add paths of folders to hide in the config.json file as a list.
- **Favorite Folders**: Add paths to add as favorites in the config.json file as a list.
- **Share only Specific Folder**: Give a path to the Root Directory or leave it as default '/' to share the complete computer directory.
