import os
from moviepy.editor import VideoFileClip

def browse_folder(start_path="."):
    """Allows user to navigate folders and select a video file"""
    current_path = os.path.abspath(start_path)
    
    while True:
        print(f"\nCurrent folder: {current_path}")
        items = os.listdir(current_path)
        
        # Separate folders and files
        folders = [f for f in items if os.path.isdir(os.path.join(current_path, f))]
        files = [f for f in items if os.path.isfile(os.path.join(current_path, f))]
        
        # Show folders
        print("\nFolders:")
        for i, folder in enumerate(folders):
            print(f"{i+1}. [D] {folder}")
        
        # Show video files only
        video_files = [f for f in files if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))]
        print("\nVideo files:")
        for i, file in enumerate(video_files):
            print(f"{i+1}. [F] {file}")
        
        print("\nCommands: cd <folder_number>, up, select <file_number>, exit")
        cmd = input("Enter command: ").strip()
        
        if cmd.startswith("cd "):
            idx = int(cmd.split()[1]) - 1
            if 0 <= idx < len(folders):
                current_path = os.path.join(current_path, folders[idx])
            else:
                print("Invalid folder number.")
        elif cmd == "up":
            current_path = os.path.dirname(current_path)
        elif cmd.startswith("select "):
            idx = int(cmd.split()[1]) - 1
            if 0 <= idx < len(video_files):
                return os.path.join(current_path, video_files[idx])
            else:
                print("Invalid file number.")
        elif cmd == "exit":
            exit()
        else:
            print("Unknown command.")

# Step 1: Browse and select video
input_video = browse_folder()

# Step 2: Ask for output file name
output_video = input("Enter output video filename (e.g., output.mp4): ").strip()

# Step 3: Ask for start and end times
start_time = float(input("Enter start time in seconds: "))
end_time = float(input("Enter end time in seconds: "))

# Step 4: Load and trim video
clip = VideoFileClip(input_video)
trimmed_clip = clip.subclip(start_time, end_time)
trimmed_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")

clip.close()
trimmed_clip.close()
print("Video trimmed successfully!")