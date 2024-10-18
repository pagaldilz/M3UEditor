import os
import datetime
from collections import defaultdict

def load_m3u(filepath):
    """Load and return the list of tracks from an extended m3u file, grouped by 'group-title'."""
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    groups = defaultdict(list)
    metadata = None

    for line in lines:
        line = line.strip()
        if line.startswith('#EXTINF'):
            metadata = line
        elif not line.startswith('#') and metadata:
            group_title = extract_group_title(metadata)
            groups[group_title].append((metadata, line))
            metadata = None
    
    return groups

def save_m3u(filepath, groups):
    """Save the list of tracks and metadata to an extended m3u file, sorted by group-title."""
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write("#EXTM3U\n")  # Write the M3U header
        
        # Sort the groups by group-title and write to the file
        for group in sorted(groups):
            for metadata, url in groups[group]:
                file.write(f"{metadata}\n{url}\n")

def extract_group_title(metadata):
    """Extract the group-title from the EXTINF metadata string."""
    start = metadata.find('group-title="') + len('group-title="')
    end = metadata.find('"', start)
    return metadata[start:end]

def export_unique_group_titles(groups, m3u_filepath):
    """Export unique group-titles to GroupTitles.txt in the same directory as the M3U file."""
    unique_group_titles = set()
    
    for group in groups.keys():
        unique_group_titles.add(group)

    directory = os.path.dirname(m3u_filepath)
    output_filepath = os.path.join(directory, 'GroupTitles.txt')
    
    export_unique_values(unique_group_titles, output_filepath, "group-title")
    
    print("\nReminder: You can now go ahead and modify 'GroupTitles.txt' with the group titles you want to keep.")

def export_unique_values(unique_values, output_filepath, value_type):
    """Export the unique values to a text file."""
    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.write(f"Unique {value_type.capitalize()} List\n")
        file.write("=" * 40 + "\n")
        
        for value in sorted(unique_values):
            file.write(f"{value}\n")

    print(f"Exported {value_type}s to {output_filepath}")

def read_group_titles_file(filepath):
    """Read the GroupTitles.txt file and return a set of allowed group titles."""
    allowed_groups = set()
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            group_title = line.strip()
            if group_title:
                allowed_groups.add(group_title)
    return allowed_groups

def filter_groups_by_titles(groups, allowed_groups):
    """Filter the M3U groups by only keeping those in the allowed group titles set."""
    filtered_groups = {group: entries for group, entries in groups.items() if group in allowed_groups}
    return filtered_groups

def save_filtered_m3u(filepath, groups):
    """Save a new M3U file with the allowed groups and a timestamp in the filename."""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    directory = os.path.dirname(filepath)
    base_filename = os.path.basename(filepath).replace('.m3u', '')
    new_filename = f"{base_filename}_filtered_{timestamp}.m3u"
    new_filepath = os.path.join(directory, new_filename)

    save_m3u(new_filepath, groups)
    print(f"Filtered playlist saved as {new_filepath}")

def main():
    filepath = input("Enter the path to your extended m3u file: ")
    groups = load_m3u(filepath)

    # Export unique group titles to GroupTitles.txt
    export_unique_group_titles(groups, filepath)

    print("\nWould you like to filter the M3U file by the GroupTitles.txt file?")
    filter_choice = input("Type 'yes' to proceed, or 'no' to skip: ")

    if filter_choice.lower() == 'yes':
        directory = os.path.dirname(filepath)
        group_titles_filepath = os.path.join(directory, 'GroupTitles.txt')

        if not os.path.exists(group_titles_filepath):
            print(f"GroupTitles.txt not found in {directory}.")
            return

        # Ask if the user has modified GroupTitles.txt
        already_modified = input("Have you already modified 'GroupTitles.txt'? (yes/no): ").lower()
        if already_modified == 'no':
            print("Please go ahead and modify 'GroupTitles.txt' with the group titles you want to keep.")
            input("Press Enter when you're ready to proceed...")

        allowed_groups = read_group_titles_file(group_titles_filepath)
        print(f"Loaded {len(allowed_groups)} allowed group titles from {group_titles_filepath}.")

        filtered_groups = filter_groups_by_titles(groups, allowed_groups)

        save_filtered_m3u(filepath, filtered_groups)

if __name__ == "__main__":
    main()
