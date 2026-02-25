import modal
from modal import Image
from transformers import BitsAndBytesConfig

app = modal.App("pricer-service")
image = Image.debian_slim().pip_install(
    "torch",
    "transformers",
    "bitsandbytes",
    "accelerate",
    "peft",
)
secret = [modal.Secret.from_name("huggingface-secret")]


#constants
GPU ="T4"
BASE_MODEL = "meta-llama/Llama-3.2-3B"
PROJECT_NAME = "price"
HF_USER = "kanyaraasi"
RUN_NAME = "2026-02-22_03.22.44"
REVISION = "f7acf0541bb98f0d944a3d70645840aeb946592f"
PROJECT_RUN_NAME=f"{PROJECT_NAME}-{RUN_NAME}"
FINETUNED_MODEL_NAME=f"{HF_USER}/{PROJECT_RUN_NAME}"

@app.function(image=image,secrets=secret,gpu=GPU,timeout=1800)
def price(description:str) -> str:
    import torch
    import re
    from transformers import AutoTokenizer,AutoModelForCausalLM,set_seed
    from peft import PeftModel

    PREFIX = "Price is $"
    QUESTION = "What does this cost to the nearest dollar?"

    prompt = f"{QUESTION}\n\n{description}\n\n{PREFIX}"

    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL,quantization_config=quant_config,device_map="auto")

    model = PeftModel.from_pretrained(base_model,FINETUNED_MODEL_NAME,revision=REVISION)

    set_seed(42)

    input = tokenizer.encode(prompt,return_tensors="pt").to("cuda")
    with torch.no_grad():
        output = model.generate(input,max_new_tokens=5)
    result = tokenizer.decode(output[0])
    contents = result.split("Price is $")[1]
    contents = contents.replace(",", "")
    match = re.search(r"[-+]?\d*\.\d+|\d+", contents)
    return float(match.group()) if match else 0