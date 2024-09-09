---
language: 
  - en
tags:
- Named Entity Recognition
- SciBERT
- Adverse Effect
- Drug
- Medical
datasets:
- ade_corpus_v2
widget:
- text: "Abortion, miscarriage or uterine hemorrhage associated with misoprostol (Cytotec), a labor-inducing drug."
  example_title: "Abortion, miscarriage, ..."
- text: "Addiction to many sedatives and analgesics, such as diazepam, morphine, etc."
  example_title: "Addiction to many..."
- text: "Birth defects associated with thalidomide"
  example_title: "Birth defects associated..."
- text: "Bleeding of the intestine associated with aspirin therapy"
  example_title: "Bleeding of the intestine..."
- text: "Cardiovascular disease associated with COX-2 inhibitors (i.e. Vioxx)"
  example_title: "Cardiovascular disease..."

---

This is a SciBERT-based model fine-tuned to perform Named Entity Recognition for drug names and adverse drug effects. 
![model image](https://raw.githubusercontent.com/jsylee/personal-projects/master/Hugging%20Face%20ADR%20Fine-Tuning/hf_adr.png)

This model classifies input tokens into one of five classes:

- `B-DRUG`: beginning of a drug entity
- `I-DRUG`: within a drug entity
- `B-EFFECT`: beginning of an AE entity
- `I-EFFECT`: within an AE entity
- `O`: outside either of the above entities 

To get started using this model for inference, simply set up an NER `pipeline` like below: 

```python
from transformers import (AutoModelForTokenClassification, 
                          AutoTokenizer, 
                          pipeline,
                          )

model_checkpoint = "jsylee/scibert_scivocab_uncased-finetuned-ner"
model = AutoModelForTokenClassification.from_pretrained(model_checkpoint, num_labels=5,
                                                        id2label={0: 'O', 1: 'B-DRUG', 2: 'I-DRUG', 3: 'B-EFFECT', 4: 'I-EFFECT'} 
                                                        )                                                        
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

model_pipeline = pipeline(task="ner", model=model, tokenizer=tokenizer)

print( model_pipeline ("Abortion, miscarriage or uterine hemorrhage associated with misoprostol (Cytotec), a labor-inducing drug."))
``` 

SciBERT: https://huggingface.co/allenai/scibert_scivocab_uncased

Dataset: https://huggingface.co/datasets/ade_corpus_v2
