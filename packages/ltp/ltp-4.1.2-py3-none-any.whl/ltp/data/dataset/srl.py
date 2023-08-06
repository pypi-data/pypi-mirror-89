import logging

import datasets
from os.path import join
from dataclasses import dataclass
from ltp.data.utils import iter_blocks

_TRAINING_FILE = "train.txt"
_DEV_FILE = "dev.txt"
_TEST_FILE = "test.txt"


def create_feature(file=None):
    if file:
        return datasets.ClassLabel(names_file=file)
    return datasets.Value('string')


@dataclass
class SrlConfig(datasets.BuilderConfig):
    """BuilderConfig for Conll2003"""

    predicate: str = None
    labels: str = None


# ["word", "bio"]
class Srl(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = SrlConfig

    def _info(self):
        return datasets.DatasetInfo(
            features=datasets.Features(
                {
                    "words": datasets.Sequence(datasets.Value("string")),
                    "predicate": datasets.Sequence(create_feature(self.config.predicate)),
                    "roles": datasets.Sequence(
                        datasets.Sequence(create_feature(self.config.labels))
                    ),
                }
            ),
            supervised_keys=None,
        )

    def _split_generators(self, dl_manager):
        data_files = {
            "train": join(self.config.data_dir, _TRAINING_FILE),
            "dev": join(self.config.data_dir, _DEV_FILE),
            "test": join(self.config.data_dir, _TEST_FILE),
        }
        data_files = dl_manager.download_and_extract(data_files)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": data_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": data_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": data_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logging.info("⏳ Generating examples from = %s", filepath)
        for line_num, block in iter_blocks(filename=filepath):
            # last example
            words, predicate, *roles = [list(value) for value in zip(*block)]

            yield line_num, {
                "words": words, "predicate": predicate, "roles": roles
            }
