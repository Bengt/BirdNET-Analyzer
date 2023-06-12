import os
from typing import List

from birdnet.configuration import config
from birdnet.configuration import config
from birdnet.configuration import config


def save_labels_file(labels: List[str], locale: str):
    """Saves localized labels to a file.

    Saves the given labels into a file with the format:
    "{config.LABELSFILE}_{locale}.txt"

    Args:
        labels: List of labels.
        locale: Two character string of a language.
    """
    # Create folder
    os.makedirs(config.TRANSLATED_LABELS_PATH, exist_ok=True)

    # Save labels file
    fpath = os.path.join(
        config.TRANSLATED_LABELS_PATH, "{}_{}.txt".format(os.path.basename(config.LABELS_FILE).rsplit(".", 1)[0], locale)
    )
    with open(fpath, "w", encoding="utf-8") as f:
        for l in labels:
            f.write(l + "\n")