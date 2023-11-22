from transformers import BartForConditionalGeneration, BartTokenizer

# كود الملخص
file_path = "/content/Recording3.txt"  # تعيين مسار الملف النصي الذي تريد استخراج النص منه

# تحميل التوكنايزر والنموذج
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

# استخراج النص من الملف
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()  # قراءة الملف النصي بأكمله وتخزين النص في متغير text

    # تحويل النص إلى الترميز المناسب لـ BART وطباعة النص
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs.input_ids, max_length=150, num_beams=4, length_penalty=2.0, early_stopping=True)
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print("الملخص:")
    print(output)

except FileNotFoundError:
    print(f"لم يتم العثور على الملف في المسار: {file_path}")
except Exception as e:
    print(f"حدث خطأ أثناء معالجة الملف: {e}")