1-网址
旧版（官方文档）
https://ai.google.dev/gemini-api/docs/text-generation?hl=zh-cn
新版
https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn

安装sdk
pip install -U -q "google-genai"

export GOOGLE_API_KEY="YOUR_API_KEY"

1-get api key
https://ai.google.dev/gemini-api/docs/libraries

语言	新库（推荐）	旧库
Python	google-genai	google-generativeai

2- set api key--mac os
sudo open ~/.zshrc

export GEMINI_API_KEY=AIzaSyCY0pgtmhJbisYENnNgWzd0m_u5vKdiB8U

source ~/.zshrc
3-test the api key

  curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[{"text": "Write a story about a magic backpack."}]
        }]
       }'

# 将 API 密钥设置为环境变量
如果您设置了环境变量 GEMINI_API_KEY 或 GOOGLE_API_KEY，
则客户端在使用某个 Gemini API 库时会自动提取 API 密钥。建议您仅设置其中一个变量，
但如果同时设置这两个变量，则 GOOGLE_API_KEY 具有优先权。


3.1--if reply this success

{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "Leo wasn't known for being prepared. He was the kid who forgot his homework, his lunch, even his shoes on occasion. So, when he stumbled upon a dusty, leather backpack tucked away in his grandfather's attic, his initial reaction was mild curiosity, not excitement. It was old, plain, and smelled faintly of mothballs and something indefinably…ancient.\n\nHe almost left it there. Almost. But something about the worn leather and the tarnished silver buckle snagged his attention. He unbuckled it, and the musty attic air filled with the scent of cinnamon and old books. Peeking inside, he found only a single, smooth river stone. He shrugged, tucked the stone in his pocket, and hauled the backpack downstairs.\n\nThe next day at school, during a particularly gruesome geometry lesson, Leo realized he'd forgotten his protractor. Again. Sighing, he mumbled, \"I wish I had a protractor,\" and subconsciously patted the backpack hanging on the back of his chair.\n\nHe reached in. And pulled out a brand new, gleaming protractor.\n\nLeo stared. It hadn't been there before. He rummaged deeper, convinced he was hallucinating. The backpack was still empty. He cautiously put the protractor back in, pulled it out again. Same result.\n\nOver the next few days, Leo experimented. He wished for a pen when his ran out of ink. Poof, a pen. He longed for a snack during a particularly long science lesson. Presto, a perfectly ripe apple. The backpack manifested whatever he genuinely needed, right when he needed it.\n\nAt first, it was amazing. No more forgetting things! Perfect grades! He was the most prepared student in the school. He even started using it to help others. A forgotten calculator? Bam, calculator. A needed bandage? Here you go! He was a hero, albeit a secret one.\n\nBut then, the magic started to…shift. He was walking home in a downpour, wishing for an umbrella, when the backpack produced a giant, rusty oil drum. He wished for a comforting hug after a particularly bad day, and it coughed up a thorny cactus.\n\nHe realized the backpack wasn't granting his wants, but his *true* needs, as perceived by something…else. He needed an umbrella to protect him, but the world, according to the backpack, needed more recycled materials (hence the oil drum). He needed comfort, but perhaps a little pain and resilience to go with it (cactus).\n\nThe backpack was starting to change him, too. He became more aware of the bigger picture, the needs of the world beyond his own. He started volunteering at the local food bank, collecting discarded materials for recycling projects, and even attempted to hug the cactus (with thick gloves, of course).\n\nOne day, his friend Maya was distraught. Her grandmother was sick, and the doctors weren't sure what was wrong. Leo, instinctively reaching for the backpack, wished for a cure.\n\nThe backpack remained stubbornly empty.\n\nHe wished harder. Still nothing. He understood then. The backpack wasn't a genie; it was a mirror, reflecting the true needs of the world. And sometimes, the hardest needs were the ones he couldn't solve with a magically conjured object.\n\nInstead, he sat with Maya, listening to her worries and offering what comfort he could. He realized that sometimes, the greatest need wasn't a miraculous cure, but a listening ear and a comforting presence.\n\nLeo still carried the backpack, but he used it less now. He relied on his own resourcefulness, his own empathy. He learned that true preparedness wasn't about having everything you wanted at your fingertips, but about being ready to face the world, needs and all, with an open heart and a willingness to help.\n\nHe reached into the backpack one last time, not needing anything, but just to feel the worn leather beneath his fingers. He pulled out the river stone he'd found inside. It was warm, smooth, and a constant reminder that even the smallest, most unassuming thing could hold a world of lessons, if you were just willing to look. And sometimes, the greatest magic wasn't in the backpack, but within yourself.\n"
          }
        ],
        "role": "model"
      },
      "finishReason": "STOP",
      "avgLogprobs": -0.68146030017618164
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 8,
    "candidatesTokenCount": 878,
    "totalTokenCount": 886,
    "promptTokensDetails": [
      {
        "modality": "TEXT",
        "tokenCount": 8
      }
    ],
    "candidatesTokensDetails": [
      {
        "modality": "TEXT",
        "tokenCount": 878
      }
    ]
  },
  "modelVersion": "gemini-2.0-flash"
}

--------------------
use api key

1-pip install google-genai

Veo is Google's most capable video generation model to date. It generates videos in a wide range of cinematic and visual styles, capturing prompt nuance to render intricate details consistently across frames.

To learn more and see example output, check out the Google DeepMind Veo overview.
Veo是谷歌迄今为止最强大的视频生成模型。它生成各种电影和视觉风格的视频，捕捉即时的细微差别，在帧间一致地呈现复杂的细节。
要了解更多信息并查看示例输出，请查看Google DeepMind Veo概述。
Specifications
Modalities	
Text-to-video generation
Image-to-video generation
Request latency	
Min: 11 seconds
Max: 6 minutes (during peak hours)
Variable length generation	5-8 seconds
Resolution	720p
Frame rate	24fps
Aspect ratio	
16:9 - landscape
9:16 - portrait
Input languages (text-to-video)	English
规格
方式
文本到视频生成
图像到视频生成
请求延迟
最短：11秒
最长：6分钟（高峰时段）
可变长度生成5-8秒
分辨率720p
帧率24fps
纵横比
16:9-景观
9:16-肖像
输入语言（文本到视频）英语

Videos created by Veo are watermarked using SynthID, our tool for watermarking and identifying AI-generated content, and are passed through safety filters and memorization checking processes that help mitigate privacy, copyright and bias risks.

Before you begin
Before calling the Gemini API, ensure you have your SDK of choice installed, and a Gemini API key configured and ready to use.

To use Veo with the Google Gen AI SDKs, ensure that you have one of the following versions installed:

Python v1.10.0 or later
TypeScript and JavaScript v0.8.0 or later
Go v1.0.0 or later
Veo创建的视频使用SynthID进行水印处理，SynthID是我们用于水印和识别AI生成内容的工具，并通过安全过滤器和记忆检查过程，有助于降低隐私、版权和偏见风险。

开始之前
在调用Gemini API之前，请确保安装了您选择的SDK，并配置了Gemini API密钥并准备好使用。

要将Veo与Google Gen AI SDK一起使用，请确保您安装了以下版本之一：

Python v1.10.0或更高版本
TypeScript和JavaScript v0.8.0或更高版本
转到v1.0.0或更高版本

Generate videos
This section provides code examples for generating videos using text prompts and using images.

Generate from text
You can use the following code to generate videos with Veo:
生成视频
本节提供了使用文本提示和图像生成视频的代码示例。

从文本生成
您可以使用以下代码使用Veo生成视频：



---------
[//]: # (ssss)
这张照片是一位年轻的亚洲女性的特写工作室肖像，她拥有美丽清澈的皮肤。该图像具有干净、极简主义的美学，是典型的美容或时尚摄影。
**详细信息：**
***模特：**这位女士有深色头发和浅色皮肤。她的五官精致，传统上很有魅力。
***头发：**她的头发又长又直，又黑又有光泽。几缕头发垂在她的脸上。
***妆容：**她化着自然的妆，突出了自己的五官，嘴唇光滑。
***珠宝：**她有一个小巧精致的耳环。
***灯光：**灯光柔和均匀，营造出光滑无瑕的外观。
***背景：**背景为中性浅灰色/白色，有助于将注意力集中在模型上，避免分心。
**风格和目的：**
*这张照片给人一种现代而精致的感觉。
*重点是模特的美丽和皮肤质量。
总之，这是一幅精心制作的美容肖像画，注重自然美和无瑕肌肤。

------------
========Generate video using Veo============
The Gemini API provides access to Veo 2, Google's state-of-the-art video generation model. Veo is designed to help you build next-generation AI applications that transform user prompts and images into high quality video assets.

This guide will help you get started with Veo using the Gemini API.
Gemini API提供了对Veo 2的访问，Veo 2是谷歌最先进的视频生成模型。Veo旨在帮助您构建下一代人工智能应用程序，将用户提示和图像转换为高质量的视频资产。

本指南将帮助您使用Gemini API开始使用Veo。

About Veo
Note: Veo is a paid feature and will not run in the Free tier. Visit the Pricing page for more details.
Veo is Google's most capable video generation model to date. It generates videos in a wide range of cinematic and visual styles, capturing prompt nuance to render intricate details consistently across frames.

To learn more and see example output, check out the Google DeepMind Veo overview.

关于Veo
注意：Veo是付费功能，不会在免费级别运行。有关更多详细信息，请访问定价页面。
Veo是谷歌迄今为止最强大的视频生成模型。它生成各种电影和视觉风格的视频，捕捉即时的细微差别，在帧间一致地呈现复杂的细节。

要了解更多信息并查看示例输出，请查看Google DeepMind Veo概述。


Veo 2
Try the API

Our state-of-the-art video generation model, available to developers on the paid tier of the Gemini API.

Free Tier	Paid Tier, per second in USD
Video price	Not available	$0.35
Used to improve our products	Yes	No
Veo 2
尝试API

我们最先进的视频生成模型，可供Gemini API付费层的开发人员使用。

免费付费等级，每秒美元
视频价格不可用$0.35
用于改进我们的产品是否
