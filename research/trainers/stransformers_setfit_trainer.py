# Utility imports
import os
import argparse
from typing import Optional
import pandas as pd
import random
import numpy as np
import json

# Preprocessing imports
from stransformers_data_preprocessing import preprocess_dataset, limit_dataset
from sklearn.preprocessing import LabelEncoder

# Transformers imports
import torch
from setfit import SetFitModel, Trainer, TrainingArguments
from setfit.losses import SupConLoss
from sentence_transformers.losses import CosineSimilarityLoss, OnlineContrastiveLoss
from transformers import EarlyStoppingCallback

# Define available losses for body training
body_training_losses = {
    "cosine": CosineSimilarityLoss,
    "setfit-contrastive": SupConLoss,
    "online-contrastive": OnlineContrastiveLoss,
}


def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def load_dataset(file_path):
    file_extension = file_path[file_path.rfind(".") :].lower()
    file_loaders = {".xlsx": pd.read_excel, ".csv": pd.read_csv}
    if file_extension in file_loaders:
        return file_loaders[file_extension](file_path)
    else:
        raise ValueError("Unsupported file format. Please use .csv or .xlsx files.")


def main(args):
    set_seed(args.seed)

    exp_directory = os.path.join(os.getcwd(), args.exp_name)
    os.makedirs(exp_directory, exist_ok=True)

    # Load datasets
    train_dataset = load_dataset(args.train_dataset_path)
    eval_dataset = load_dataset(args.eval_dataset_path)
    test_dataset = load_dataset(args.test_dataset_path)

    # Encoding labels
    le = LabelEncoder()
    train_dataset["label"] = le.fit_transform(train_dataset["label"])
    eval_dataset["label"] = le.transform(eval_dataset["label"])
    test_dataset["label"] = le.transform(test_dataset["label"])

    train_dataset = limit_dataset(train_dataset, max_samples=500)
    eval_dataset = limit_dataset(eval_dataset, max_samples=150)
    test_dataset = limit_dataset(test_dataset, max_samples=150)

    # Load Model
    model = SetFitModel.from_pretrained(
        args.model,
        use_differentiable_head=True,
        head_params={"out_features": len(le.classes_)},
    ).to("cuda")

    tokenizer = model.model_body.tokenizer
    max_seq_len = model.model_body.max_seq_length

    train_dataset = preprocess_dataset(
        train_dataset,
        tokenizer,
        max_length=max_seq_len,
        stride=max_seq_len,
        shuffle_seed=args.seed,
    )
    eval_dataset = preprocess_dataset(
        eval_dataset,
        tokenizer,
        max_length=max_seq_len,
        stride=max_seq_len,
        shuffle_seed=args.seed,
    )
    test_dataset = preprocess_dataset(
        test_dataset,
        tokenizer,
        max_length=max_seq_len,
        stride=max_seq_len,
        shuffle_seed=args.seed,
    )

    # Instantiate TrainingArguments
    training_args = TrainingArguments(
        output_dir=exp_directory,
        batch_size=(args.body_batch_size, args.classif_batch_size),
        num_epochs=(args.body_epochs, args.classif_epochs),
        body_learning_rate=(args.body_learning_rate, args.classif_learning_rate),
        num_iterations=args.num_pairs_generation,
        end_to_end=args.e2e,
        sampling_strategy=args.sampling_strategy,
        report_to="tensorboard",
        logging_dir=os.path.join(exp_directory, "logs"),
        logging_strategy="steps",
        logging_steps=args.logging_steps,
        show_progress_bar=True,
        evaluation_strategy="steps",
        eval_steps=args.eval_steps,
        save_strategy="steps",
        save_steps=args.save_steps,
        load_best_model_at_end=True,
        warmup_proportion=0.1,
        l2_weight=args.l2_weight,
    )

    metric_average_arg = None
    if args.metric_type is not None:
        metric_average_arg = {"average": args.metric_type}

    # Instantiate Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        metric=args.metric,
        metric_kwargs=metric_average_arg,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=10)],
        # ... [add other relevant parameters for Trainer]
    )

    # Training
    trainer.train()

    # Evaluate on the evaluation dataset
    eval_metrics = trainer.evaluate(eval_dataset)
    print("Evaluation Metrics:", eval_metrics)

    # Evaluate on the test dataset
    test_metrics = trainer.evaluate(test_dataset)
    print("Test Metrics:", test_metrics)

    model.save_pretrained(exp_directory)
    model.push_to_hub(args.exp_name)

    # Save results to JSON file
    results = {args.exp_name: {"evaluation": eval_metrics, "test": test_metrics}}
    results_save_path = os.path.join(exp_directory, "results.json")
    with open(results_save_path, "w") as json_file:
        json.dump(results, json_file, indent=4)

    print(f"Results saved to {results_save_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a Sentence Transformer model using SetFit."
    )

    parser.add_argument(
        "--exp-name",
        type=str,
        default="setfit-experiment",
        help="Name of the experiment.",
    )

    # Arguments for dataset paths and model
    parser.add_argument(
        "--train-dataset-path",
        type=str,
        required=True,
        help="Path to the training dataset file (Excel or CSV).",
    )
    parser.add_argument(
        "--eval-dataset-path",
        type=str,
        required=True,
        help="Path to the evaluation dataset file (Excel or CSV).",
    )
    parser.add_argument(
        "--test-dataset-path",
        type=str,
        required=True,
        help="Path to the test dataset file (Excel or CSV).",
    )
    parser.add_argument(
        "--model", type=str, required=True, help="Model name to be used for training."
    )

    # Arguments for body training
    parser.add_argument(
        "--body-training-strategy",
        type=str,
        default="cosine",
        choices=list(body_training_losses.keys()),
        help="Training strategy to be used for body training.",
    )
    parser.add_argument(
        "--body-batch-size", type=int, default=16, help="Batch size for body training."
    )
    parser.add_argument(
        "--body-epochs", type=int, default=3, help="Number of epochs for body training."
    )
    parser.add_argument(
        "--body-learning-rate",
        type=float,
        default=2e-5,
        help="Learning rate for body training.",
    )
    parser.add_argument(
        "--num-pairs-generation",
        type=Optional[int],
        default=None,
        help="Number of pairs to generate for training (Deprecated).",
    )

    # Arguments for classification training
    parser.add_argument(
        "--e2e", type=bool, default=False, help="Whether to train the model end-to-end."
    )
    parser.add_argument(
        "--classif-batch-size",
        type=int,
        default=16,
        help="Batch size for classification training.",
    )
    parser.add_argument(
        "--classif-epochs",
        type=int,
        default=25,
        help="Number of epochs for classification training.",
    )
    parser.add_argument(
        "--classif-learning-rate",
        type=float,
        default=1e-2,
        help="Learning rate for classification training.",
    )

    # Additional arguments
    parser.add_argument(
        "--l2-weight", type=float, default=0.01, help="L2 weight decay for training."
    )

    parser.add_argument(
        "--sampling-strategy",
        type=str,
        default="oversampling",
        help="Sampling strategy for training: 'oversampling', 'undersampling', or 'unique'.",
    )

    parser.add_argument(
        "--seed", type=int, default=42, help="Seed for random number generators."
    )
    parser.add_argument(
        "--metric",
        type=str,
        required=True,
        help="Evaluation metric to be used for training.",
    )
    parser.add_argument(
        "--metric-type",
        type=Optional[str],
        default=None,
        required=False,
        help="Type of metric: macro , micro or weighted.",
    )

    parser.add_argument(
        "--save-steps",
        type=int,
        default=1000,
        help="Number of save steps.",
    )

    parser.add_argument(
        "--eval-steps",
        type=int,
        default=1000,
        help="Number of eval steps.",
    )

    parser.add_argument(
        "--logging-steps",
        type=int,
        default=500,
        help="Number of logging steps.",
    )

    args = parser.parse_args()
    main(args)
