import os

# Base dataset folder
base_path = "dataset/augmented"

folders = ["dementia", "no_dementia"]

for folder in folders:
    folder_path = os.path.join(base_path, folder)

    files = sorted(os.listdir(folder_path))

    count = 1
    for file in files:
        old_path = os.path.join(folder_path, file)

        # Get file extension (.wav, .mp3 etc)
        ext = os.path.splitext(file)[1]

        new_name = f"voice_{count}{ext}"
        new_path = os.path.join(folder_path, new_name)

        os.rename(old_path, new_path)

        count += 1

print("Renaming completed successfully.")