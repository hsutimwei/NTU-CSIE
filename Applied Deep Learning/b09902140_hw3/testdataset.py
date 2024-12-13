import datasets
import json
class Mydataset(datasets.GeneratorBasedBuilder):
   #cited:https://blog.csdn.net/qq_42388742/article/details/114293746
    def _info(self):
       return datasets.DatasetInfo(
            features=datasets.Features(
                {
                    'id': datasets.Value("string"),
                    'text': datasets.Value("string"),
                }
            ),supervised_keys=None
        )

    def _split_generators(self, filepath):

        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": self.config.data_files['test']}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath[0]) as file:
            for line in file:
                row = json.loads(line)
                text = row['maintext'].strip().replace('\n', '').replace('\r', '')
                id = row['id']
                yield id,{
                "id": id,
                "text": text,
                }
        