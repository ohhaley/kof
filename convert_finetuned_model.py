from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base_model_path = "path/to/your/base_model"
lora_adapter_path = "path/to/your/fine_tuned_checkpoint"
output_hf_dir = "path/to/save/merged_model"

base_model = AutoModelForCausalLM.from_pretrained(base_model_path, device_map="cpu", torch_dtype="auto")
model = PeftModel.from_pretrained(base_model, lora_adapter_path)
model = model.merge_and_unload()

tokenizer = AutoTokenizer.from_pretrained(base_model_path)
model.save_pretrained(output_hf_dir)
tokenizer.save_pretrained(output_hf_dir)
