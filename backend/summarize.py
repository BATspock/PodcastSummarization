# summarize long text by breaking them into smaller chunks of size 1024 or less, then perform an extractive summarization on each chunk and then combine the results.
# after the result is coupled perfom an abstractive summarization on the result.

# Input data from main.py

import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
model_name = 'tuner007/pegasus_summarizer'
#torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to('cpu')

def get_response(input_text):
  batch = tokenizer([input_text],truncation=True,padding='longest',max_length=1024, return_tensors="pt").to('cpu')
  gen_out = model.generate(**batch,max_length=128,num_beams=5, num_return_sequences=1, temperature=1.5)
  output_text = tokenizer.batch_decode(gen_out, skip_special_tokens=True)
  return output_text

# break it in chunks of 1024 words or less, stop at the last full stop before 512 words and continue from there
def split_text(text, n=1024):
    words = text.split()
    return [' '.join(words[i:i+n]) for i in range(0, len(words), n)]
    
# summarize each chunk and combine the results

def summarize_text(text):
    summary = get_response(text)
    return summary

# summarize each chunk and combine the results
def summarize_chunks(chunks):
    summary = []
    for chunk in chunks:
        summary.append(summarize_text(chunk))
    return summary

# summarize the text
def summarize(text):
    chunks = split_text(text)
    summary = summarize_chunks(chunks)
    return summary

with open("transcription.txt", "r") as f:
    text = f.read()

summary = summarize(text)
print(summary)