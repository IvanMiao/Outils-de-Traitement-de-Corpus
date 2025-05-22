from datasets import load_dataset, DatasetDict


train_file = "./data/clean/train.csv"
validation_file = "./data/clean/validation.csv"
test_file = "./data/clean/test.csv"

train_dataset = load_dataset("csv", data_files=train_file, split="train")
validation_dataset = load_dataset("csv", data_files=validation_file, split="train")
test_dataset = load_dataset("csv", data_files=test_file, split="train")

dataset = DatasetDict({
	"train": train_dataset, 
	"validation": validation_dataset,
	"test": test_dataset
	})

dataset.save_to_disk("./data/clean/ch_poems")