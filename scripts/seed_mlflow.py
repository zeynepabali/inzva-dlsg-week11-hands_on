"""
Seed MLflow with demo experiment runs for teaching.

Usage:
    python seed_mlflow.py                          # defaults to http://localhost:5000
    python seed_mlflow.py http://mlflow:5000       # inside Docker network

Creates two experiments:
  1. "inzva-ai-telemetry"  — 20 inference runs (simulating /chat endpoint)
  2. "inzva-model-training" — 8 training runs with per-epoch loss/accuracy curves
"""

import math
import os
import sys
import random

import mlflow

# ─── Config ───
TRACKING_URI = sys.argv[1] if len(sys.argv) > 1 else os.getenv(
    "MLFLOW_TRACKING_URI", "http://localhost:5000"
)

# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIMENT 1: Inference Telemetry
# ═══════════════════════════════════════════════════════════════════════════════

TELEMETRY_EXPERIMENT = "inzva-ai-telemetry"

PROMPTS = [
    "What is gradient descent?",
    "Explain backpropagation briefly.",
    "How does a hash map work?",
    "What is a binary search tree?",
    "Explain Docker containers in simple terms.",
    "What is the difference between CNN and RNN?",
    "How does attention work in transformers?",
    "What is quantization in deep learning?",
    "Explain the bias-variance tradeoff.",
    "What is transfer learning?",
    "How does batch normalization help training?",
    "What are the advantages of using uv over pip?",
    "Explain the concept of overfitting.",
    "What is a learning rate scheduler?",
    "How does dropout regularization work?",
    "What is the purpose of an activation function?",
    "Explain the difference between L1 and L2 regularization.",
    "What is a REST API?",
    "How does FastAPI differ from Flask?",
    "What are the benefits of containerization?",
]

INFERENCE_MODELS = [
    ("qwen2.5:0.5b", 0.7),
    ("qwen2.5:1.5b", 0.2),
    ("qwen2.5:3b", 0.1),
]


def pick_inference_model():
    r = random.random()
    cumulative = 0
    for model, weight in INFERENCE_MODELS:
        cumulative += weight
        if r <= cumulative:
            return model
    return INFERENCE_MODELS[0][0]


def simulate_latency(model: str) -> float:
    base = {
        "qwen2.5:0.5b": random.gauss(1200, 400),
        "qwen2.5:1.5b": random.gauss(2800, 600),
        "qwen2.5:3b": random.gauss(5500, 1200),
    }
    return max(200, base.get(model, 1500))


def simulate_response_length(model: str) -> int:
    base = {
        "qwen2.5:0.5b": random.randint(80, 350),
        "qwen2.5:1.5b": random.randint(150, 600),
        "qwen2.5:3b": random.randint(250, 900),
    }
    return base.get(model, 200)


def seed_telemetry():
    print(f"\n{'═'*60}")
    print(f"  📊 Experiment 1: {TELEMETRY_EXPERIMENT}")
    print(f"{'═'*60}")
    mlflow.set_experiment(TELEMETRY_EXPERIMENT)

    num_runs = len(PROMPTS)
    print(f"  Seeding {num_runs} inference runs...\n")

    for i, prompt in enumerate(PROMPTS, 1):
        model = pick_inference_model()
        latency = round(simulate_latency(model), 2)
        resp_len = simulate_response_length(model)

        with mlflow.start_run(run_name=f"chat-{i:03d}"):
            mlflow.log_param("model", model)
            mlflow.log_param("prompt", prompt[:200])
            mlflow.log_metric("latency_ms", latency)
            mlflow.log_metric("response_length", resp_len)

        bar = "█" * (i * 30 // num_runs) + "░" * (30 - i * 30 // num_runs)
        print(f"  [{bar}] {i}/{num_runs}  {model:<14}  {latency:>7.0f}ms  {prompt[:45]}")

    print(f"\n  ✅ {num_runs} inference runs logged.")


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIMENT 2: Model Training
# ═══════════════════════════════════════════════════════════════════════════════

TRAINING_EXPERIMENT = "inzva-model-training"

# Each training run: (name, architecture, optimizer, lr, batch_size, epochs, final_acc, converge_speed)
TRAINING_RUNS = [
    {
        "name": "resnet18-baseline",
        "architecture": "ResNet-18",
        "dataset": "CIFAR-10",
        "optimizer": "SGD",
        "lr": 0.01,
        "batch_size": 128,
        "epochs": 25,
        "dropout": 0.0,
        "final_acc": 0.912,
        "converge": 0.35,       # how fast loss drops (higher = faster)
        "noise": 0.015,         # epoch-to-epoch noise
        "tags": {"task": "image-classification", "framework": "PyTorch"},
    },
    {
        "name": "resnet18-augmented",
        "architecture": "ResNet-18",
        "dataset": "CIFAR-10",
        "optimizer": "SGD",
        "lr": 0.01,
        "batch_size": 128,
        "epochs": 25,
        "dropout": 0.2,
        "final_acc": 0.938,
        "converge": 0.28,
        "noise": 0.012,
        "tags": {"task": "image-classification", "framework": "PyTorch", "augmentation": "randaugment"},
    },
    {
        "name": "resnet50-cosine-lr",
        "architecture": "ResNet-50",
        "dataset": "CIFAR-10",
        "optimizer": "Adam",
        "lr": 0.001,
        "batch_size": 64,
        "epochs": 30,
        "dropout": 0.3,
        "final_acc": 0.951,
        "converge": 0.22,
        "noise": 0.008,
        "tags": {"task": "image-classification", "framework": "PyTorch", "scheduler": "cosine"},
    },
    {
        "name": "vit-tiny-scratch",
        "architecture": "ViT-Tiny",
        "dataset": "CIFAR-10",
        "optimizer": "AdamW",
        "lr": 0.0003,
        "batch_size": 256,
        "epochs": 30,
        "dropout": 0.1,
        "final_acc": 0.873,
        "converge": 0.15,
        "noise": 0.025,
        "tags": {"task": "image-classification", "framework": "PyTorch", "model_type": "transformer"},
    },
    {
        "name": "vit-small-pretrained",
        "architecture": "ViT-Small",
        "dataset": "CIFAR-10",
        "optimizer": "AdamW",
        "lr": 0.0001,
        "batch_size": 64,
        "epochs": 15,
        "dropout": 0.1,
        "final_acc": 0.968,
        "converge": 0.45,
        "noise": 0.006,
        "tags": {"task": "image-classification", "framework": "PyTorch", "pretrained": "ImageNet-21k"},
    },
    {
        "name": "bert-base-finetune",
        "architecture": "BERT-base",
        "dataset": "SST-2",
        "optimizer": "AdamW",
        "lr": 2e-5,
        "batch_size": 32,
        "epochs": 5,
        "dropout": 0.1,
        "final_acc": 0.927,
        "converge": 0.55,
        "noise": 0.008,
        "tags": {"task": "sentiment-analysis", "framework": "HuggingFace", "pretrained": "bert-base-uncased"},
    },
    {
        "name": "mlp-overfit-demo",
        "architecture": "MLP-3layer",
        "dataset": "CIFAR-10",
        "optimizer": "SGD",
        "lr": 0.1,
        "batch_size": 512,
        "epochs": 30,
        "dropout": 0.0,
        "final_acc": 0.52,
        "converge": 0.45,
        "noise": 0.03,
        "overfit": True,         # train acc keeps rising, val acc plateaus
        "tags": {"task": "image-classification", "framework": "PyTorch", "note": "overfitting-demo"},
    },
    {
        "name": "mlp-regularized",
        "architecture": "MLP-3layer",
        "dataset": "CIFAR-10",
        "optimizer": "Adam",
        "lr": 0.001,
        "batch_size": 128,
        "epochs": 30,
        "dropout": 0.5,
        "final_acc": 0.61,
        "converge": 0.20,
        "noise": 0.018,
        "tags": {"task": "image-classification", "framework": "PyTorch", "note": "regularized"},
    },
]


def generate_loss_curve(epochs, converge, noise, initial_loss=2.3):
    """Generate a realistic training loss curve with exponential decay + noise."""
    losses = []
    for e in range(epochs):
        # Exponential decay with noise
        base = initial_loss * math.exp(-converge * e)
        jitter = random.gauss(0, noise * initial_loss)
        losses.append(max(0.01, base + jitter))
    return losses


def generate_acc_curve(epochs, final_acc, converge, noise, overfit=False):
    """Generate realistic train/val accuracy curves."""
    train_accs = []
    val_accs = []
    for e in range(epochs):
        progress = 1 - math.exp(-converge * e)

        # Training accuracy — always rises
        train_target = min(0.999, final_acc + (0.05 if not overfit else 0.45))
        train_acc = 0.1 + progress * (train_target - 0.1) + random.gauss(0, noise)
        train_accs.append(min(0.999, max(0.05, train_acc)))

        # Validation accuracy
        if overfit and e > epochs * 0.35:
            # Plateau and slightly decline after peak
            peak = 0.1 + 0.35 * (final_acc + 0.05 - 0.1) / 0.35
            val_acc = peak + random.gauss(0, noise * 1.5) - 0.003 * (e - epochs * 0.35)
        else:
            val_acc = 0.1 + progress * (final_acc - 0.1) + random.gauss(0, noise * 1.2)

        val_accs.append(min(0.999, max(0.05, val_acc)))

    return train_accs, val_accs


def seed_training():
    print(f"\n{'═'*60}")
    print(f"  🧪 Experiment 2: {TRAINING_EXPERIMENT}")
    print(f"{'═'*60}")
    mlflow.set_experiment(TRAINING_EXPERIMENT)

    num_runs = len(TRAINING_RUNS)
    print(f"  Seeding {num_runs} training runs with per-epoch metrics...\n")

    for i, run_cfg in enumerate(TRAINING_RUNS, 1):
        epochs = run_cfg["epochs"]
        is_overfit = run_cfg.get("overfit", False)

        # Generate curves
        train_losses = generate_loss_curve(epochs, run_cfg["converge"], run_cfg["noise"])
        val_losses = generate_loss_curve(epochs, run_cfg["converge"] * 0.85, run_cfg["noise"] * 1.3)
        train_accs, val_accs = generate_acc_curve(
            epochs, run_cfg["final_acc"], run_cfg["converge"], run_cfg["noise"], is_overfit
        )

        with mlflow.start_run(run_name=run_cfg["name"]):
            # ── Hyperparameters ──
            mlflow.log_param("architecture", run_cfg["architecture"])
            mlflow.log_param("dataset", run_cfg["dataset"])
            mlflow.log_param("optimizer", run_cfg["optimizer"])
            mlflow.log_param("learning_rate", run_cfg["lr"])
            mlflow.log_param("batch_size", run_cfg["batch_size"])
            mlflow.log_param("epochs", epochs)
            mlflow.log_param("dropout", run_cfg["dropout"])

            # ── Per-epoch metrics (shows up as charts in MLflow) ──
            for e in range(epochs):
                mlflow.log_metric("train_loss", round(train_losses[e], 4), step=e + 1)
                mlflow.log_metric("val_loss", round(val_losses[e], 4), step=e + 1)
                mlflow.log_metric("train_acc", round(train_accs[e], 4), step=e + 1)
                mlflow.log_metric("val_acc", round(val_accs[e], 4), step=e + 1)

            # ── Final summary metrics ──
            mlflow.log_metric("best_val_acc", round(max(val_accs), 4))
            mlflow.log_metric("final_train_loss", round(train_losses[-1], 4))
            mlflow.log_metric("final_val_loss", round(val_losses[-1], 4))
            mlflow.log_metric("total_epochs", epochs)

            # ── Tags ──
            for k, v in run_cfg["tags"].items():
                mlflow.set_tag(k, v)

        status = "⚠️ overfit" if is_overfit else f"  acc={max(val_accs):.1%}"
        print(f"  [{i}/{num_runs}]  {run_cfg['name']:<24}  {run_cfg['architecture']:<12}  "
              f"{epochs:>2} epochs  {status}")

    print(f"\n  ✅ {num_runs} training runs logged with per-epoch curves.")


# ═══════════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    random.seed(42)  # Reproducible results

    print(f"🔗 Connecting to MLflow at: {TRACKING_URI}")
    mlflow.set_tracking_uri(TRACKING_URI)

    seed_telemetry()
    seed_training()

    print(f"\n{'═'*60}")
    print(f"  🎉 All done! Open {TRACKING_URI} to explore.")
    print(f"  Experiments created:")
    print(f"    1. {TELEMETRY_EXPERIMENT}  — 20 inference runs")
    print(f"    2. {TRAINING_EXPERIMENT} — 8 training runs with loss/accuracy charts")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    main()

