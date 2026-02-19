import os
import shutil

DATASET_PATH = r"C:\Dementia_ml\dementia-ai-backend\dataset\audio"

for class_folder in ["dementia", "no_dementia_1", "no_dementia_2"]:
    folder_path = os.path.join(DATASET_PATH, class_folder)

    print(f"\nProcessing: {folder_path}")

    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        if os.path.isdir(subfolder_path):
            for file in os.listdir(subfolder_path):
                if file.endswith(".wav"):
                    src = os.path.join(subfolder_path, file)
                    dst = os.path.join(folder_path, file)

                    print(f"Moving {file}")
                    shutil.move(src, dst)

            # optional: remove empty person folder
            if not os.listdir(subfolder_path):
                os.rmdir(subfolder_path)
