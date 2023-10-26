import requests
import io
import base64
from PIL import Image
import re
from github import Github
import os

# 输入您的 GitHub 个人访问令牌
token = "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"
# 创建 GitHub 客户端
g = Github(token)
# 指定仓库的用户名和仓库名
username = "ssnsja"
repo_name = "testoutputimage"
# 获取指定的仓库
repo = g.get_user(username).get_repo(repo_name)
prompts = "<lora:April-01:1.1>,a beautiful girl,a beautiful white blouse,a blue skirt, masterpiece, best quality,indoor,wooden house"
nagetive_prompts="lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, negative_hand-neg";
PaintsNumber = r"../output/PaintsNumber.txt";
PaintsNumber_file_path = "paintingsNumber.txt"

def getPaintsNumber():
        try:
            with open(PaintsNumber, "r", encoding="utf-8") as file:
                paintsnumbercontent = file.read()
                print("文件内容：")
                print(paintsnumbercontent)
        except FileNotFoundError:
            print("文件 'paintsnumber.txt' 不存在")
        except Exception as e:
            print(f"发生错误: {str(e)}")
        return paintsnumbercontent

image_counter = int(getPaintsNumber());
# 指定文件路径
file_path = r"../output/sessionlog.txt";
last_position = 0;
num = 0;
import os  # 导入os模块
# 定义目标文件夹路径
output_folder = r"../output/png"

def set_initialization(file_path):
    with open(file_path, 'w') as file:
        file.write('')
    
def set_last_position(file_path):
    global last_position
    with open(file_path,'a+') as file:
        last_position= file.tell()
        
def read_quoted_contents(file_path, position):
    # 以读取模式打开文件
    with open(file_path, 'r+') as file:
        # 读取文件内容
        file.seek(position,0)
        print(position)
        contents = file.read()
    # 使用正则表达式查找所有被双引号括起来的内容
    quoted_contents = re.findall(r'"([^"]*)"', contents)
    #通过生成器函数返回被引号括起来的内容
    #for content in quoted_contents:
    #   yield content
    #返回列表中第一个元素
    return quoted_contents[0]
# 创建一个生成器对象
#gen = read_quoted_contents(r"D:\LearnDeepLearning\DigitalLife\Betav0.3\ChaGPT-API-Call-main(1)\ChaGPT-API-Call-main\sessionlog.txt",3)#这个要在函数外部 
#print(gen)

def setPaintsNumber(number):
    with open(PaintsNumber,"w+") as file:
        try:
                with open(PaintsNumber, "w+", encoding="utf-8") as file:
                    file.write(str(number));
                    print("修改后文件内容：");
                    print(str(number))
        except FileNotFoundError:
                print("文件 'paintsnumber.txt' 不存在")
        except Exception as e:
                print(f"发生错误: {str(e)}")
   
def setGithubPaintsNumber(PaintsNumber):
    file_content = str(PaintsNumber)
     # 获取文件
    file = repo.get_contents(PaintsNumber_file_path)
    # 更新文件内容
    repo.update_file(PaintsNumber_file_path, "Update PaintsNumber",file_content, file.sha)
    print(f"成功将 {PaintsNumber_file_path} 内容更新为 {file_content}")
     

def DrawPainting():  
    global image_counter;
    print("good1")
    # 每次运行函数时，调用next(gen)来读取下一个被引号括起来的内容    
    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''
    #content =next(gen)
    url = "http://127.0.0.1:7860"
    content = read_quoted_contents(file_path,last_position)
    payload = {
        "prompt": content+prompts, # 正面提示词
        "negative_prompt": nagetive_prompts, # 负面提示词
        "steps": 20 , # 步数        
    }
    print("\033[36m图片提示词\n"+content)
    
    
    headers = {
        "Authorization": "Basic RGlnaXRhbExpZmU6RGlnaXRhbExpZmU="
    }
    print("drawing")
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload, headers=headers)
    r = response.json()
   
    image_counter += 1   
    print(image_counter)
    setPaintsNumber(image_counter)
    setGithubPaintsNumber(image_counter)

    # 得到图像对象后，将其保存到目标文件夹中
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
        image_filename = f"output{image_counter}.png"
        image_path = os.path.join(output_folder, image_filename)  # 构建完整的文件路径
        print(f"Saving image to: {image_path}")
        image.save(image_path)  # 保存图像到目标文件夹

    # 上传图片到仓库
    with open(image_path, "rb") as file:
        contents = file.read()
        repo.create_file(image_filename, "Commit message", contents)
        print("Image uploaded successfully.")
    
    # 删除本地图片
    os.remove(image_path);
    print("Local image deleted.");
    print("draw successfully");
   

