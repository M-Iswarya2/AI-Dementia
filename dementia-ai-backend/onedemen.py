import os
import shutil

BASE_PATH = r"C:\Dementia_ml\dementia-ai-backend\dataset\audio"

src_folders = ["no_dementia_1", "no_dementia_2"]
target_folder = os.path.join(BASE_PATH, "no_dementia")

os.makedirs(target_folder, exist_ok=True)

for folder in src_folders:
    folder_path = os.path.join(BASE_PATH, folder)

    for file in os.listdir(folder_path):
        if file.endswith(".wav"):
            shutil.move(
                os.path.join(folder_path, file),
                os.path.join(target_folder, file)
            )

print("✅ no_dementia_1 and no_dementia_2 merged into no_dementia")
