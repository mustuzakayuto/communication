import torch 
from diffusers import StableDiffusionPipeline 
from torch import autocast 
import datetime 
import json 
import os

model_paths = {"normal":"xyn-ai/anything-v4.0","Anime_style":"CompVis/stable-diffusion-v1-4","real":"emilianJR/chilloutmix_NiPrunedFp32Fix"}

def main(PROMPT,MODEL_ID="",init_img=None):
    
    if not os.path.isdir("./static/images/create"):
        os.mkdir("./static/images/create")
    
    
    if MODEL_ID=="normal":
        MODEL_ID = model_paths["normal"]
    elif MODEL_ID == "Anime_style":
        MODEL_ID = model_paths["Anime_style"]
    elif MODEL_ID == "real":
        MODEL_ID = model_paths["real"]
    else:
        MODEL_ID = model_paths["normal"]
    print(MODEL_ID)
    
    
    if os.path.isfile("../config.json"):
        tag=".."
    else:
        tag="."
    # GPU設定
    DEVICE = "cuda"
    # CPU設定
    # DEVICE = "cpu"
    
    # config.jsonファイルをroad
    json_open = open(tag+"/config.json","r")
    json_load = json.load(json_open)
    # config.jsonファイルの中に入っているtokenでYOUR_TOKENを設定
    YOUR_TOKEN = json_load["create_image"]["token"]
    SEED = 512
    STEP = 20
    SCALE = 7.5
    # ネガティブプロンプトリスト型で設定
    negative_prompt= [
        "text"," signature"," watermark"," username"," artist name"," stamp"," title"," subtitle"," date"," footer"," header ",
        "bad hands","bad finger","bad face","bad Facial Structure","bad Mouth","bad nose","bad Arm structure","extra legs","extra arms",
        "worst quality","Deformation","Distortion","Skin Exposure",
        "malformed_face","malformed_hands","malformed_eye","Worst image quality"," out of focus","heavy ",
        "Make it look ugly with bad anatomy",
        " make it irrelevant to the topic","low quality",
        "Noise", "mosaic"
        ]
    
    negative = ""
    for textdata in negative_prompt:
        negative+=textdata
    negative_prompt = negative
    print(negative_prompt)
    
    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16, 
                                                use_auth_token=YOUR_TOKEN) 
    pipe.to(DEVICE) 
    
    # seed固定 
    generator = torch.Generator(device=DEVICE).manual_seed(SEED) 
    
    file_path=""
    with autocast(DEVICE): 
        
        image = pipe(
            # プロンプト
            PROMPT, 
            # ネガティブプロンプト
            negative_prompt=negative_prompt,
            # 画像生成プロセスが入力されたプロンプト（呪文）にどれくらい忠実に描画を行うかを制御するためのパラメータ
            guidance_scale=SCALE, 
            # 推論ステップ数
            num_inference_steps=STEP,
            # デバイス設定(GPU,CPU)
            generator=generator,
            
            ).images[0]
        # 現在の時刻
        dt_now = datetime.datetime.now() 
        now = dt_now.strftime("%Y%m%d%H%M%S") 
        # ファイル名 
        file_path = "./static/images/create/"+str(SEED) + "_" + str(now) + ".png"
        # ファイル保存 
        image.save(file_path) 
        
    torch.cuda.empty_cache()
    return file_path    


    
    
if __name__ == "__main__":

    # main2("Beautiful idol",init_img="./static/images/create/512_20230914102037.png")
    main("dog and rabbit")
