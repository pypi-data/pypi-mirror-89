from setuptools import setup

long_description1 = '''
# КРАТКАЯ ДОКУМЕНТАЦИЯ

Привет! эта библиотека создана для быстрого написания ботов в ВК. Сейчас я расскажу вам о ней!

(тест)


'''
setup(
name='LiteVkApi', 
version='0.4',
description='Библиотека для лекгого написания ботов ВК!', 
packages=['LiteVkApi'], 
author_email='ma_mush@mail.ru', 
zip_safe=False,
python_requires='>=3.6',
long_description=long_description1,
long_description_content_type="text/markdown"
)