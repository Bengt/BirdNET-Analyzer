import audio
import config as cfg
import model
import utils


import os


def _load_training_data():
    """Loads the data for training.
    Reads all subdirectories of "config.TRAIN_DATA_PATH" and uses their names as new labels.
    These directories should contain all the training data for each label.
    """
    # Get list of subfolders as labels
    labels = list(sorted(utils.list_subdirectories(cfg.TRAIN_DATA_PATH)))

    # Load training data
    x_train = []
    y_train = []

    for i, label in enumerate(labels):
        # Get label vector
        label_vector = np.zeros((len(labels),), dtype="float32")
        if not label.lower() in ["noise", "other", "background", "silence"]:
            label_vector[i] = 1

        # Get list of files
        # Filter files that start with '.' because macOS seems to them for temp files.
        files = filter(
            os.path.isfile,
            (
                os.path.join(cfg.TRAIN_DATA_PATH, label, f)
                for f in sorted(os.listdir(os.path.join(cfg.TRAIN_DATA_PATH, label)))
                if not f.startswith(".") and f.rsplit(".", 1)[-1].lower() in cfg.ALLOWED_FILETYPES
            ),
        )

        # Load files
        for f in files:
            # Load audio
            sig, rate = audio.open_audio_file(f)

            # Crop center segment
            sig = audio.crop_center(sig, rate, cfg.SIG_LENGTH)

            # Get feature embeddings
            embeddings = model.extract_embeddings([sig])[0]

            # Add to training data
            x_train.append(embeddings)
            y_train.append(label_vector)

    # Convert to numpy arrays
    x_train = np.array(x_train, dtype="float32")
    y_train = np.array(y_train, dtype="float32")

    return x_train, y_train, labels
