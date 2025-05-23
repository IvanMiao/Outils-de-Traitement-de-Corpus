from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import numpy as np
from datasets import load_from_disk
import evaluate


dataset = load_from_disk("./data/clean/ch_poems")

# model:
# option 1. distilled-bert-multilingual
# option 2. bert-case-chinese
# option 3. guwenbert
model_checkpoint = "ethanyt/guwenbert-base"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

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


accuracy = evaluate.load("accuracy")
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)

id2label = {
    0: 'WeiJin',
    1: 'NanBei',
    2: 'Tang',
    3: 'Song',
    4: 'Yuan',
    5: 'Ming',
    6: 'Qing'
}
label2id = {
    'WeiJin': 0,
    'NanBei': 1,
    'Tang': 2,
    'Song': 3,
    'Yuan': 4,
    'Ming': 5,
    'Qing': 6
    }

model = AutoModelForSequenceClassification.from_pretrained(
    model_checkpoint,
    num_labels=7,
    id2label=id2label,
    label2id=label2id
)

training_args = TrainingArguments(
    output_dir="./model/ch_poem_classifier_guwenbert",
    learning_rate=2e-5,
    per_device_train_batch_size=6,
    per_device_eval_batch_size=6,
    num_train_epochs=2,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    push_to_hub=False,
    fp16=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data["train"],
    eval_dataset=tokenized_data["validation"],
    processing_class=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()
trainer.save_model("./model/best_model_guwenbert")