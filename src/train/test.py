from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments
import evaluate
import numpy as np
from sklearn.metrics import classification_report
from datasets import load_from_disk

model_path = "./model/best_model_bert_chinese"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

dataset = load_from_disk("./data/clean/ch_poems")


def preprocess_function(examples):
    result = tokenizer(
        examples["Content"],
        truncation=True,
        padding="max_length",
        max_length=512,
        )
    result["labels"] = examples['lable']
    return result


tokenized_data = dataset.map(preprocess_function, batched=True)
test_dataset = tokenized_data["test"]


def compute_metrics(eval_pred):
    accuracy = evaluate.load("accuracy")
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)


test_args = TrainingArguments(
    output_dir="./results",
    per_device_eval_batch_size=16,
    do_train=False,
    do_eval=False,
    do_predict=True,
    use_cpu=True,
)

trainer = Trainer(
    model=model,
    args=test_args,
    compute_metrics=compute_metrics,
)

print("Evaluating the model on test dataset...")
results = trainer.predict(test_dataset)

print(f"Result: {results.metrics}")

predictions = np.argmax(results.predictions, axis=1)

id2label = {
    0: 'WeiJin',
    1: 'NanBei',
    2: 'Tang',
    3: 'Song',
    4: 'Yuan',
    5: 'Ming',
    6: 'Qing'
}

class_correct = {i: 0 for i in range(7)}
class_total = {i: 0 for i in range(7)}

for i, pred in enumerate(predictions):
    true_label = test_dataset[i]['labels']
    class_total[true_label] += 1
    if pred == true_label:
        class_correct[true_label] += 1

print("\nAccuracy for each Dynasty:")
for class_id, class_name in id2label.items():
    if class_total[class_id] > 0:
        accuracy = class_correct[class_id] / class_total[class_id] * 100
        print(f"{class_name}:{accuracy:.2f}%", end=' ')
        print(f"({class_correct[class_id]}/{class_total[class_id]})")

true_labels = [test_dataset[i]['labels'] for i in range(len(test_dataset))]
print("\nReport of classification:")
report = classification_report(
    true_labels,
    predictions,
    target_names=[id2label[i] for i in range(7)],
    digits=4)
print(report)
