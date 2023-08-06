# Multiclipboard

Saves and loads pices of text to the clipboard, via a database in a .db file

## Install

``` bash
$ pip install multiclipboard
```

## How to use

``` bash
# Import pakage
from multiclipboard import multiclipboard

# Folder to save the .db file
bd_file = "c:\\user\\my_files"

# Make an intance reading the clipboard
my_multiclipboard = multiclipboard.Multiclipboard(bd_file)


# Save text from clipboard to the database, and associate this text with a keyword
my_multiclipboard.save_text ("key4")

# Save specific text  clipboard to the database, and associate this text with a keyword
my_multiclipboard.save_text ("key2", text="Example text to save")

# Return specific text with keyword
text = my_multiclipboard.get_text ("key2")
print (text)

# Copy to clipboard specific text with keyword
my_multiclipboard.copy_text ("key4")

# Delete specific keywords and the keyword text
my_multiclipboard.delete_keyword (1)

# Delete all keywords from the file
my_multiclipboard.delete_all()

# Print all keywords from the file
my_multiclipboard.list_keywords()

```

