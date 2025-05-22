from datasets import load_dataset, concatenate_datasets
import pandas as pd


raw_dir = "./data/raw"
output_dir = "./data/clean"
dynasties = ["WeiJin", "NanBei", "Tang", "Song", "Yuan", "Ming", "Qing"]

dynasty_to_label = {
    'WeiJin': 0,
    'NanBei': 1,
    'Tang': 2,
    'Song': 3,
    'Yuan': 4,
    'Ming': 5,
    'Qing': 6
}

combined_train = []
combined_validation = []
combined_test = []

for dynasty in dynasties:
    dataset = []
    raw_file = f"{raw_dir}/{dynasty}_poems.csv"
    df = pd.read_csv(raw_file)

    filtered_df = df[~df["Content"].str.contains("□|①", na=False)]
    filtered_df['lable'] = df['Dynasty'].map(dynasty_to_label)
    temp_file = f"{raw_dir}/temp_{dynasty}_poems.csv"
    filtered_df.to_csv(temp_file, index=False)

    dataset = load_dataset("csv", data_files=temp_file)["train"]

    split_dataset = dataset.train_test_split(test_size=0.3)
    test_valid = split_dataset["test"].train_test_split(test_size=0.5)

    combined_train.append(split_dataset["train"])
    combined_validation.append(test_valid["train"])
    combined_test.append(test_valid["test"])

final_train = concatenate_datasets(combined_train).shuffle(seed=42)
final_train.to_csv(f"{output_dir}/train.csv", index=False)

final_validation = concatenate_datasets(combined_validation).shuffle(seed=42)
final_validation.to_csv(f"{output_dir}/validation.csv", index=False)

final_test = concatenate_datasets(combined_test).shuffle(seed=42)
final_test.to_csv(f"{output_dir}/test.csv", index=False)
