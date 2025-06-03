import requests
import json
import base64
from PIL import Image
from io import BytesIO
from time import sleep

from config import system_description_prompt, system_video_prompt



def clear_topics(message):
    message = message.replace("Описание Изображения:\n\n", "")
    message = message.replace("Сюжет для Видео:\n\n", "")
    message = message.replace("\n\nПосле Подтверждения будет Сгенерировано Изображение!", "")
    message = message.replace("\n\nГенерируем Видео?", "")

    return message


class VideoGenerator:
    def __init__(self, new_topic, storage_path):
        self.topic = new_topic
        self.character_description = None
        self.character_image = None
        self.video_plot = None

        self.storage_path = storage_path


    def new_character_description(self, description):
        self.character_description = description

    def new_character_image(self, image_path):
        self.character_image = image_path

    def new_video_plot(self, plot):
        self.video_plot = plot

    def debugger(self):
        for k, v in self.__dict__.items():
            print(f"{str(k)} = {str(v)}")



class MiniMaxAi:
    def __init__(self, api_key, group_id, storage_path):
        self.api_key = api_key
        self.group_id = ""

        self.storage_path = storage_path


    def generate_image(self, prompt):
        url = "https://api.minimaxi.chat/v1/image_generation"
        api_key = self.api_key

        payload = json.dumps({
            "model": "image-01",
            "prompt": prompt,
            "aspect_ratio": "9:16",
            "response_format": "base64",
            "n": 1,
            "prompt_optimizer": False
        })
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()

        # print(response)

        path_to_save = self.storage_path + response["id"] + ".jpeg"

        image_bytes = self.base64_to_image(response["data"]["image_base64"][0])
        img = self.create_image_from_bytes(image_bytes)
        img.save(path_to_save)

        return path_to_save

    def base64_to_image(self, base64_string):
        if "data:image" in base64_string:
            base64_string = base64_string.split(",")[1]

        image_bytes = base64.b64decode(base64_string)
        return image_bytes

    def create_image_from_bytes(self, image_bytes):
        image_stream = BytesIO(image_bytes)

        image = Image.open(image_stream)
        return image


    def generate_description(self, prompt):
        api_key = self.api_key

        url = f"https://api.minimaxi.chat/v1/text/chatcompletion_v2"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "DeepSeek-R1",
            "messages": [
                {
                    "content": system_description_prompt,
                    "role": "system",
                    "name": "MM Intelligent Assistant"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload).json()

        print(response)

        return response["choices"][0]["message"]["content"].replace("**Prompt:**", "")

    def generate_plot(self, video_topic, image_description):
        api_key = self.api_key

        url = f"https://api.minimaxi.chat/v1/text/chatcompletion_v2"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "DeepSeek-R1",
            "messages": [
                {
                    "content": system_video_prompt,
                    "role": "system",
                    "name": "MM Intelligent Assistant"
                },
                {
                    "role": "user",
                    "content": f"Video Topic: {video_topic}\n\nImage Description: {image_description}"
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload).json()

        print(response)

        return response["choices"][0]["message"]["content"]

    def generate_video(self, prompt, video_topic, image_path):
        url = "https://api.minimaxi.chat/v1/video_generation"
        api_key = self.api_key

        # base64
        with open(image_path, "rb") as image_file:
            data = base64.b64encode(image_file.read()).decode('utf-8')

        payload = json.dumps({
            "model": "I2V-01-Director",
            "prompt": f"Video Topic: {video_topic}\n\n{prompt}",
            "first_frame_image": f"data:image/jpeg;base64,{data}"
        })
        headers = {
            'authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()
        task_id = response["task_id"]

        print(response)

        url_status = f"http://api.minimaxi.chat/v1/query/video_generation?task_id={task_id}"

        payload = {}
        headers = {
            'authorization': f'Bearer {api_key}',
            'content-type': 'application/json',
        }

        while True:
            response_status = requests.request("GET", url_status, headers=headers, data=payload).json()

            print(response_status)

            if (response_status["status"] == "Success"):
                file_id = response_status["file_id"]

                url_video = f'https://api.minimaxi.chat/v1/files/retrieve?GroupId={self.group_id}&file_id={file_id}'
                headers = {
                    'authority': 'api.minimaxi.chat',
                    'content-type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                }

                video_response = requests.get(url_video, headers=headers).json()
                print(video_response)

                try:
                    file_name = self.download_video_from_url(file_id, video_response["file"]["download_url"])

                    return file_name

                except:
                    pass

            sleep(10)

    def download_video_from_url(self, file_id, url_download):
        filename = self.storage_path + file_id + ".mp4"

        try:
            response = requests.get(url_download, stream=True)
            response.raise_for_status()

            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            return filename

        except Exception as e:
            return None