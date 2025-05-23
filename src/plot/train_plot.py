import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# 1. Loss data from terminal
#    distilbert-multilingual
distilbert_train_loss = [
    1.8123, 1.7152, 1.6424, 1.5912, 1.5733, 1.5433, 1.5054, 1.4983,
    1.4555, 1.3828, 1.3546, 1.3518, 1.3743, 1.3443, 1.3323, 1.3166, 1.3417,
    1.2372, 1.1696, 1.1505, 1.1057, 1.1649, 1.1158, 1.1649, 1.1338, 1.1227
]
distilbert_eval_loss = [1.4935, 1.4148, 1.4760]
distilbert_eval_accuracy = [0.3774, 0.4187, 0.4222]
distilbert_epochs = np.linspace(0.11, 2.99, len(distilbert_train_loss))
distilbert_eval_epochs = [1.0, 2.0, 3.0]

#    bert-base-chinese
bert_chinese_train_loss = [
    1.7852, 1.6555, 1.6018, 1.5566, 1.5164, 1.4426,
    1.3377, 1.3184, 1.3148, 1.2707, 1.2533
]
bert_chinese_eval_loss = [1.4911, 1.4106]
bert_chinese_eval_accuracy = [0.3681, 0.4241]
bert_chinese_epochs = np.linspace(0.17, 1.89, len(bert_chinese_train_loss))
bert_chinese_eval_epochs = [1.0, 2.0]

#    guwenbert-base
guwenbert_train_loss = [
    1.677, 1.5626, 1.4769, 1.4279, 1.3749, 1.3334,
    1.2207, 1.2089, 1.2195, 1.1771, 1.1501
]
guwenbert_eval_loss = [1.3528, 1.2604]
guwenbert_eval_accuracy = [0.4380, 0.4790]
guwenbert_epochs = np.linspace(0.17, 1.89, len(guwenbert_train_loss))
guwenbert_eval_epochs = [1.0, 2.0]

# result from validation subsets
test_results = {
    'DistilBERT': 0.4222,
    'BERT-Chinese': 0.4241,
    'GuwenBERT': 0.4790
}

# Accuracy for classification
dynasties = ['WeiJin', 'NanBei', 'Tang', 'Song', 'Yuan', 'Ming', 'Qing']
distilbert_dynasty_acc = [
    0.8248, 0.5397, 0.3680, 0.1211, 0.5115, 0.3632, 0.4509
]
bert_chinese_dynasty_acc = [
    0.7350, 0.6032, 0.5898, 0.1413, 0.5322, 0.4003, 0.2754
]
guwenbert_dynasty_acc = [
    0.8376, 0.6413, 0.5546, 0.2287, 0.6877, 0.4361, 0.2018
]

# number of samples
samples = [234, 315, 568, 446, 823, 782, 570]

# 2. Figure 1. Training Analysis
fig, axes1 = plt.subplots(1, 2, figsize=(16, 8))
fig.suptitle('Model Training Analysis', fontsize=18)

# 2.1 curve of Loss/Epoch
ax = axes1[0]
ax.plot(distilbert_epochs, distilbert_train_loss,
        'b-', label='train loss: DistilBERT')
ax.plot(distilbert_eval_epochs, distilbert_eval_loss,
        'bo--', label='validation loss: DistilBERT')
ax.plot(bert_chinese_epochs, bert_chinese_train_loss,
        'r-', label='train loss: BERT-Chinese')
ax.plot(bert_chinese_eval_epochs, bert_chinese_eval_loss,
        'ro--', label='validation loss: BERT-Chinese')
ax.plot(guwenbert_epochs, guwenbert_train_loss,
        'g-', label='train loss: GuwenBERT')
ax.plot(guwenbert_eval_epochs, guwenbert_eval_loss,
        'go--', label='validation loss: GuwenBERT')
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
ax.set_title('Training and Validation Loss')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

# 2.2 Comparaison of accuracies
ax = axes1[1]
models = list(test_results.keys())
accuracies = list(test_results.values())
ax.bar(models, accuracies, color=['blue', 'red'])
ax.set_xlabel('Model')
ax.set_ylabel('Accuracy')
ax.set_title('Accuracy Comparison in Validation Subset')
for i, v in enumerate(accuracies):
    ax.text(i, v + 0.01, f'{v:.4f}', ha='center')
ax.set_ylim(0, 0.6)
ax.grid(True, linestyle='--', alpha=0.7, axis='y')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('./figures/training_analysis.png', dpi=300, bbox_inches='tight')

# 3 Figure 2: Test Result Analysis

fig2, axes2 = plt.subplots(1, 2, figsize=(16, 8))
fig2.suptitle('Evaluation Analysis', fontsize=18)

# 2.1 Accuracy of classification
ax = axes2[0]
x = np.arange(len(dynasties))
width = 0.25
ax.bar(x - width, distilbert_dynasty_acc, width, label='DistilBERT')
ax.bar(x, bert_chinese_dynasty_acc, width, label='BERT-Chinese')
ax.bar(x + width, guwenbert_dynasty_acc, width, label='GuwenBERT')
ax.set_xlabel('Dynasty')
ax.set_ylabel('Accuracy')
ax.set_title('Accuracy by Dynasty')
ax.set_xticks(x)
ax.set_xticklabels(dynasties)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7, axis='y')

# 2.4 Relation bewtween samples and accuracy
total_accuracy = (distilbert_dynasty_acc +
                  bert_chinese_dynasty_acc + guwenbert_dynasty_acc)
ax = axes2[1]
scatter_df = pd.DataFrame({
    'samples': samples * 3,
    'accuracy': total_accuracy,
    'model': ['DistilBERT'] * 7 + ['BERT-Chinese'] * 7 + ['GuwenBERT'] * 7,
    'dynasty': dynasties * 3
})
sns.scatterplot(data=scatter_df, x='samples', y='accuracy', hue='model',
                style='dynasty', s=100, ax=ax)
ax.set_title('Relation: Sample Size & Accuracy')
ax.grid(True, linestyle='--', alpha=0.7)

# add dynasty label
for i, row in scatter_df.iterrows():
    ax.annotate(row['dynasty'],
                (row['samples'], row['accuracy']),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('./figures/evaluate_analysis.png', dpi=300, bbox_inches='tight')
