import config as cfg
import model
from birdnet.train._load_training_data import _load_training_data


def train_model(on_epoch_end=None):
    """Trains a custom classifier.
    Args:
        on_epoch_end: A callback function that takes two arguments `epoch`, `logs`.
    Returns:
        A keras `History` object, whose `history` property contains all the metrics.
    """
    # Load training data
    print("Loading training data...", flush=True)
    x_train, y_train, labels = _load_training_data()
    print(f"...Done. Loaded {x_train.shape[0]} training samples and {y_train.shape[1]} labels.", flush=True)

    # Build model
    print("Building model...", flush=True)
    classifier = model.build_linear_classifier(y_train.shape[1], x_train.shape[1], cfg.TRAIN_HIDDEN_UNITS)
    print("...Done.", flush=True)

    # Train model
    print("Training model...", flush=True)
    classifier, history = model.train_linear_classifier(
        classifier,
        x_train,
        y_train,
        epochs=cfg.TRAIN_EPOCHS,
        batch_size=cfg.TRAIN_BATCH_SIZE,
        learning_rate=cfg.TRAIN_LEARNING_RATE,
        on_epoch_end=on_epoch_end,
    )

    # Best validation precision (at minimum validation loss)
    best_val_prec = history.history["val_prec"][np.argmin(history.history["val_loss"])]

    model.save_linear_classifier(classifier, cfg.CUSTOM_CLASSIFIER, labels)
    print(f"...Done. Best top-1 precision: {best_val_prec}", flush=True)

    return history