BOT_TOKEN = "7875103347:AAHl-aCPeQ-AmvobMzfyriYBtc_yF5Pl1XA"


API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJzaGVycmlkYW4iLCJVc2VyTmFtZSI6InNoZXJyaWRhbiIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxOTI1NDY3MTM3MDY1ODgyNTg0IiwiUGhvbmUiOiIiLCJHcm91cElEIjoiMTkyNTQ2NzEzNzA2MTY4Nzc2NyIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6InR5dXJpbmdlb3JnZTIwMDVAZ21haWwuY29tIiwiQ3JlYXRlVGltZSI6IjIwMjUtMDUtMjQgMTc6MjA6MjkiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.NgxA-riqBwB33176Fln7MuO3NaAZXbYFNjqRmeUezPmjeRlkMxmgl7Iy9r06ycZaEi_a6RNAnnINcUWyNsd6344wLOXM4Xr4KNZ5Kcr8qATyl9URtUnLaJ3h3cBoNcRz1xaYHzGIs6OYW6XvoJ7HuaplSt57zB46KXpsmKXjxaMT1mUXeJLLtzpBnQCh0iW5VasMX-pszUSirx4r_LmIp84kxVbl7snucuWm2o9mQ1RrK7EOPUmSzvO6WNqyvYRFEbmnoIFDptWdav-l8a63jkiDnN6iv9d13S9uvN58pBmEAajCF8Ieo26ZDGF1Rsp0yWws1qqd5-7MNhodOrk4WA"
group_id = "1925467137061687767"


storage_path = "./storage/"

new_topic_message = "*Новое Видео\\!*\n\nПридумай тему для нового Видеоролика\\. _\\(Можно написать с деталями\\)_"


system_video_prompt = """Ты профессиональный продюсер коротких видео. Пиши только сюжет видео на английском языке на заданную тему промпта, на основе описание изображения, учитывай детали пожелания. Сюжет должен быть подробно расписан. Видео будет основано на изображени по описанию.

Сюжет видео является промптом для другой нейросети, которая делает видео. Описание сюжета должно быть менее 1000 символов. Отвечай только промптом (сюжет видео), никаких пожеланий и вступительных текстов. В видео не должно быть текста. Название видео писать тоже не надо."""

system_description_prompt = """Ты профессиональный художник. Пиши только подробное описание на английском языке на заданную тему промпта, учитывай детали пожелания.

Описание является промптом для другой нейросети, которая делает изображения. Отвечай только промптом (описание изображения), никаких пожеланий и вступительных текстов. Описание менее 1000 символов.

На изображение могут быть персонажи, предметы или что-то другое - твоя задача помимо изображения описать персонажей или предметы."""