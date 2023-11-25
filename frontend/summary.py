from transformers import BartForConditionalGeneration, BartTokenizer


def get_summary(file_path):
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs.input_ids, max_length=150, num_beams=4, length_penalty=2.0, early_stopping=True)
        output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    except FileNotFoundError:
        print(f"file not found: {file_path}")
    except Exception as e:
        print(f"Error: {e}")

    return output

