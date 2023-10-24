import torch 

import datetime 

from PIL import Image
from diffusers import AutoPipelineForImage2Image
from diffusers import AutoPipelineForText2Image
def negative():
    # negative_prompt= [
    #     "text"," signature"," watermark"," username"," artist name"," stamp"," title"," subtitle"," date"," footer"," header ",
    #     "bad hands","bad finger","bad face","bad Facial Structure","bad Mouth","bad nose","bad Arm structure","extra legs","extra arms",
    #     "worst quality","Deformation","Distortion","Skin Exposure",
    #     "malformed_face","malformed_hands","malformed_eye","Worst image quality"," out of focus","heavy ",
    #     "Make it look ugly with bad anatomy",
    #     " make it irrelevant to the topic","low quality",
    #     "Noise", "mosaic"
    #     ]
    # negative = ""
    # for textdata in negative_prompt:
    #     negative+=textdata
    # negative_prompt = negative
    negative_prompt=""
    return negative_prompt
model_paths = {"normal":"xyn-ai/anything-v4.0","Anime_style":"CompVis/stable-diffusion-v1-4","real":"emilianJR/chilloutmix_NiPrunedFp32Fix"}

def main2(prompt,MODEL_ID="",init_img=None):
    
    STEP = 20
    if MODEL_ID=="normal":
        MODEL_ID = model_paths["normal"]
    elif MODEL_ID == "Anime_style":
        MODEL_ID = model_paths["Anime_style"]
    elif MODEL_ID == "real":
        MODEL_ID = model_paths["real"]
    else:
        MODEL_ID = model_paths["normal"]
    
    pipe_t2i = AutoPipelineForText2Image.from_pretrained(
        MODEL_ID, torch_dtype=torch.float16
    ).to("cuda")
    # 作成済みの「pipe_t2i」を利用して作成すれば追加メモリ不要
    pipe_i2i = AutoPipelineForImage2Image.from_pipe(pipe_t2i)  
    init_image = Image.open(init_img)

    # img2img実行
    # prompt = "beautiful landscape with animals"
    strength=0.8
    image = pipe_i2i(prompt=prompt,negative_prompt=negative(), image=init_image, strength=strength ,num_inference_steps=STEP).images[0]
    dt_now = datetime.datetime.now() 
    print(dt_now)
    now = dt_now.strftime("%Y%m%d%H%M%S") 
    print(str(now))
    file_path = "./static/images/create/"+   str(now) +"ReCreate"+ ".png"
    image.save(file_path)
    return file_path
if __name__ == "__main__":
    prompt = input("プロンプト:")
    file_path=input("(static/images/create)の中のパスを指定: ")
    file_path="static/images/create/"+file_path
    # main2("beautiful landscape with animals",init_img="./static/images/create/512_20230914102037.png")
    print(main2(prompt=prompt,init_img=file_path))
    
