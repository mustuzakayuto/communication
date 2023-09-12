import torch 
from diffusers import StableDiffusionPipeline 
from torch import autocast 
import datetime 
import json 
def main(PROMPT,ISanimation=False):
    if ISanimation:
        MODEL_ID = "xyn-ai/anything-v4.0"
    else:
        MODEL_ID = "CompVis/stable-diffusion-v1-4"
    
    DEVICE = "cuda"
    YOUR_TOKEN = "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"
    # PROMPT = "idol"
    SEED = 512
    STEP = 20
    SCALE = 7.5
    negative_prompt = "I want the image to have worst quality with low resolution, out of focus, , heavy jpeg artifacts. Make it look ugly with bad anatomy. Add a visible watermark, use inappropriate language in the text,  make it irrelevant to the topic. Ensure it doesn't match the story , feels unsettling with a gloomy tone ,worst quality,low quality, bad anatomy,Skin Exposure"
    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16, 
                                                use_auth_token=YOUR_TOKEN) 
    pipe.to(DEVICE) 
    
    # seed固定 
    generator = torch.Generator(device=DEVICE).manual_seed(SEED) 
    # list型に引数・呪文を格納→json文字列に変換 
    dic_info = {"prompt": PROMPT, "guidance_scale": SCALE, "seed": SEED, "num_inference_steps": STEP} 
    json_str = json.dumps(dic_info) 
    file_path=""
    with autocast(DEVICE): 
        image = pipe(PROMPT, guidance_scale=SCALE, num_inference_steps=STEP, generator=generator,negative_prompt=negative_prompt).images[0]
        # 現在時間 
        dt_now = datetime.datetime.now() 
        now = dt_now.strftime("%Y%m%d%H%M%S") 
        # ファイル名 
        file_path = "./static/images/create/"+str(SEED) + "_" + str(now) + ".png"
        # ファイル保存 
        image.save(file_path) 
        
    torch.cuda.empty_cache()
    return file_path    
if __name__ == "__main__":
    main("Beautiful idol")
