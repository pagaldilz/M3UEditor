# M3U Playlist Editor
Python script to edit m3u files using the group tag
This script is generated using ChatGPT

Key Features:
GroupTitles.txt Export: The script automatically exports the unique group titles from the M3U file into a GroupTitles.txt file in the same directory as the M3U file.

Modification Check for GroupTitles.txt: Before filtering, the script asks the user if they have modified the GroupTitles.txt file to include the groups they want to keep.

Filtering M3U by GroupTitles: The user is asked if they want to proceed with filtering the M3U file using GroupTitles.txt. If they do, the M3U file is filtered, and a new filtered M3U file is saved with a timestamp in its filename.

Automatic Sorting: The M3U file is saved with the groups sorted alphabetically by group-title.

Usage:
Run the script and enter the path to your M3U file.
The script will export the GroupTitles.txt file and prompt you to modify it if needed.
After modifying the file, the script filters the M3U file to keep only the groups listed in GroupTitles.txt.
The filtered M3U file is saved with a timestamp to indicate the changes.
