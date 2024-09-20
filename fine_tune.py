# fine_tune.py (optimized for faster runs)

import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments, DataCollatorForSeq2Seq
import torch

def load_and_prepare_dataset(csv_path):
    """ Load and prepare the dataset from the provided CSV file. """
    try:
        import chardet
        with open(csv_path, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']

        data = pd.read_csv(csv_path, encoding=encoding, engine='python')

        if 'question' not in data.columns or 'answer' not in data.columns:
            raise ValueError("CSV must contain 'question' and 'answer' columns.")

        data = data.dropna(subset=['question', 'answer'])

        data['question'] = data['question'].astype(str)
        data['answer'] = data['answer'].astype(str)

        dataset = Dataset.from_pandas(data)
        return dataset
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def tokenize_function(example, tokenizer):
    """ Tokenize the dataset for training. """
    model_inputs = tokenizer(example['question'], max_length=128, truncation=True, padding='max_length')
    labels = tokenizer(example['answer'], max_length=128, truncation=True, padding='max_length')
    model_inputs['labels'] = labels['input_ids']
    return model_inputs

class CustomTrainer(Trainer):
    """ Custom trainer with an improved save_model function. """
    def save_model(self, output_dir=None, _internal_call=False):
        # Ensure all tensors are contiguous before saving
        for name, param in self.model.named_parameters():
            if not param.is_contiguous():
                param.data = param.data.contiguous()

        # Now save the model
        super().save_model(output_dir, _internal_call)

def main():
    csv_path = r'C:\Users\91744\Downloads\AI-Dataset.csv'  # Update path accordingly

    # Load dataset
    dataset = load_and_prepare_dataset(csv_path)
    if dataset is None:
        print("Failed to load dataset.")
        return

    # Split dataset into train and eval
    split_datasets = dataset.train_test_split(test_size=0.1)
    train_dataset = split_datasets['train']
    eval_dataset = split_datasets['test']

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('google/t5-v1_1-small')  # Smaller model for fast training
    model = AutoModelForSeq2SeqLM.from_pretrained('google/t5-v1_1-small')

    def tokenize_examples(example):
        return tokenize_function(example, tokenizer)

    # Tokenize the datasets
    tokenized_train = train_dataset.map(tokenize_examples, batched=True)
    tokenized_eval = eval_dataset.map(tokenize_examples, batched=True)

    # Data collator for Seq2Seq models
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    # Set up training arguments for faster training
    training_args = TrainingArguments(
        output_dir='./results',
        eval_strategy='epoch',
        learning_rate=2e-5,
        per_device_train_batch_size=2,  # Reduced batch size for limited memory usage
        per_device_eval_batch_size=2,
        num_train_epochs=1,  # Fewer epochs for faster testing
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=1000,  # Less frequent logging
        fp16=True,  # Mixed precision training for faster computation
        gradient_accumulation_steps=4,  # Accumulate gradients for memory efficiency
    )

    # Custom trainer for handling model saves
    trainer = CustomTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_eval,
        data_collator=data_collator
    )

    # Start training
    trainer.train()

    # Save the fine-tuned model
    model.save_pretrained('./fine_tuned_model')
    tokenizer.save_pretrained('./fine_tuned_model')

if __name__ == "__main__":
    main()
