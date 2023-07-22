import datasets
import json

class Mydataset(datasets.GeneratorBasedBuilder):
   #cite:https://blog.csdn.net/qq_42388742/article/details/114293746
    def _info(self):
       return datasets.DatasetInfo(
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {"text": datasets.Value("string"),"answer_start": datasets.Value("int32")}
                    ),
                }
            ),supervised_keys=None
        )

    def _split_generators(self, filepath):
        
        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": self.config.data_files['test']}),
        ]

    def _generate_examples(self, filepath):
        data_path = open(filepath[0] , encoding = "utf-8")
        context = open(filepath[1] , encoding = "utf-8")
        relevant=open("./data/pred.json" , encoding = "utf-8")
        all_data = json.load(data_path)
        context_data = json.load(context)
        choice=json.load(relevant)

        for data in all_data:
          id = data['id']
          question = data['question']
          context = context_data[choice[id]]
          answer_starts = []
          text = []

          yield id,{
            "id": id,
            "question": question,
            "context": context,
            "answers": {"answer_start": answer_starts,"text": text},
            }
        