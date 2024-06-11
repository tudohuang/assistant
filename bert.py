import torch
from transformers import AutoTokenizer, AutoModel

model_name = "hfl/chinese-bert-wwm"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def embed_texts(texts, model, tokenizer, device):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=128)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).cpu().numpy()




browser_list = ["開啟瀏覽器", "啟動瀏覽器", "打開網頁", "開網頁", "開啟Chrome", "啟動Chrome", "打開Chrome", 
                "開啟Firefox", "打開Firefox", "啟動Firefox", "開啟Safari", "打開Safari", "啟動Safari", 
                "開啟Edge", "打開Edge", "啟動Edge", "開網頁程式", "打開網路瀏覽器", "開啟瀏覽程式", 
                "打開上網程式", "幫我開瀏覽器", "麻煩你開一下瀏覽器", "請打開瀏覽器", "能不能幫我開瀏覽器", 
                "我想用一下瀏覽器，幫我開一下"]
app_list = ["開啟{xx}應用程式", "啟動{xx}應用程式", "打開{xx}APP", "開啟{xx}APP", "啟動{xx}APP", 
            "打開{xx}程式", "開啟{xx}程式", "啟動{xx}程式", "打開{xx}軟體", "開啟{xx}軟體", 
            "啟動{xx}軟體", "開{xx}應用程式", "打開{xx}應用", "開啟{xx}應用", "啟動{xx}應用", 
            "打開{xx}工具", "開啟{xx}工具", "啟動{xx}工具", "進入{xx}", "開啟{xx}服務", 
            "幫我打開{xx}應用", "麻煩你開一下{xx}", "請幫我啟動{xx}程式", "能不能幫我開{xx}", 
            "我要用{xx}，請打開"]
leave_list = ["結束", "退出", "離開", "關閉", "停止", "終止", "關掉", "停用", "結束應用", "關閉程式", 
              "終止程式", "離開應用", "退出程式", "結束這個", "退出這個", "關閉這個", "結束運行", 
              "終止操作", "停止運行", "離開這裡", "我想退出", "幫我關掉", "能不能結束這個", "麻煩停止這個", "請關閉"]
video_list = ["YouTube搜尋{xx}", "YouTube查找{xx}", "YouTube搜索{xx}", "在YouTube找{xx}", "在YouTube搜{xx}", 
              "YouTube上搜尋{xx}", "YouTube查詢{xx}", "YouTube上找{xx}", "YouTube上搜索{xx}", "YouTube上查詢{xx}", 
              "在YouTube上找{xx}", "YouTube影片{xx}", "YouTube上查找{xx}", "YouTube查找影片{xx}", "YouTube搜尋影片{xx}", 
              "YouTube影片搜索{xx}", "在YouTube上搜尋{xx}", "YouTube上搜{xx}", "YouTube視頻{xx}", "YouTube視頻搜索{xx}", 
              "幫我在YouTube找{xx}", "麻煩你搜尋YouTube上的{xx}", "請在YouTube搜索{xx}", "我想看YouTube上的{xx}", 
              "能不能在YouTube查找{xx}", "我要{xx}的影片"]
google_list=["Google搜尋{xx}", "Google查找{xx}", "Google搜索{xx}", "在Google找{xx}", "在Google搜{xx}", 
             "Google上搜尋{xx}", "Google查詢{xx}", "Google上找{xx}", "Google上搜索{xx}", "Google上查詢{xx}", 
             "在Google上找{xx}", "Google查找資訊{xx}", "Google上查找{xx}", "Google查找資料{xx}", "Google搜尋資訊{xx}", 
             "在Google上搜尋{xx}", "Google上搜{xx}", "Google資訊{xx}", "Google上查資料{xx}", "Google查找{xx}", 
             "幫我在Google搜尋{xx}", "麻煩你查找Google上的{xx}", "請在Google搜索{xx}", "我想查Google上的{xx}", 
             "能不能在Google查找{xx}"]
remind_list = ["提醒我{x}分鐘後去{xx}", "{x}分鐘後提醒我去{xx}", "在{x}分鐘後提醒我去{xx}", "請在{x}分鐘後提醒我去{xx}", 
               "{x}分鐘後通知我去{xx}", "提醒我去{xx}，{x}分鐘後", "在{x}分鐘後提醒我做{xx}", "{x}分鐘後叫我去{xx}", 
               "請在{x}分鐘後通知我去{xx}", "{x}分鐘後提醒我做{xx}", "在{x}分鐘後叫我去{xx}", "提醒我{xx}，{x}分鐘後", 
               "{x}分鐘後提醒我辦{xx}", "提醒我{x}分鐘之後去{xx}", "在{x}分鐘後提醒我做{xx}事", "請提醒我{x}分鐘後去{xx}", 
               "{x}分鐘後提醒我去辦{xx}", "在{x}分鐘後提醒我去{xx}", "提醒我做{xx}，{x}分鐘後", "{x}分鐘後提醒我去做{xx}", 
               "幫我設一個提醒，{x}分鐘後去{xx}", "麻煩在{x}分鐘後提醒我去{xx}", "請在{x}分鐘後通知我辦{xx}", 
               "我需要一個提醒，{x}分鐘後去{xx}", "設定一個提醒，{x}分鐘後去{xx}"]
weather_list = ["{city}的天氣", "查詢{city}天氣", "{city}天氣如何", "{city}的天氣如何", "{city}的天氣情況", 
                "{city}天氣怎樣", "查{city}的天氣", "搜尋{city}天氣", "查詢{city}的天氣", "{city}今天天氣", 
                "{city}的天氣狀況", "{city}的天氣預報", "{city}天氣怎麼樣", "{city}的天氣怎麼樣", "搜索{city}天氣", 
                "{city}的天氣情況怎樣", "{city}天氣預報", "{city}的氣象", "{city}現在的天氣", "查{city}天氣", 
                "幫我查{city}的天氣", "麻煩你查詢{city}的天氣", "請問{city}的天氣如何", "{city}現在的天氣怎麼樣", 
                "能不能告訴我{city}的天氣"]

calculate = [
    '計算', '算一下', '幫我算', '計算一下', '求', '求一下', '算出來', '算一下結果', '計算結果', '幫我計算'
]

# 時間查詢功能相似詞列表
time = [
    '時間', '現在幾點', '幾點了', '報告時間', '說一下時間', '告訴我時間', '現在的時間', '時間是多少', '時間是什麼', '當前時間'
]

# 日期查詢功能相似詞列表
date = [
    '日期', '今天幾號', '今天的日期', '現在的日期', '報告日期', '告訴我今天的日期', '今天是什麼日子', '日期是多少', '今天是幾號', '今天是哪一天'
]



# 翻譯功能相似詞列表
translate = [
    '翻譯', '翻譯一下', '幫我翻譯', '翻譯成', '翻譯到', '翻譯這句話', '翻譯這段', '請翻譯', '翻譯這個', '幫我翻譯一下'
]

note = [
    '筆記', "備忘錄", 'note', '筆記本'
]
templates = {
    "browser": browser_list,
    "app": app_list,
    "leave": leave_list,
    "video": video_list,
    "google": google_list,
    "remind": remind_list,
    "weather": weather_list,
    "calculate": calculate,
    "date":date,
    "translate": translate,
    "time": time,
    "note":note,
}

template_embeddings = {}
for category, texts in templates.items():
    template_embeddings[category] = embed_texts(texts, model, tokenizer, device)



import numpy as np

def cosine_similarity_manual(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def find_best_match(input_text, template_embeddings=template_embeddings, model=model, tokenizer=tokenizer, device=device):
    input_embedding = embed_texts([input_text], model, tokenizer, device)[0]
    best_match = None
    best_similarity = -1
    best_category = None

    for category, embeddings in template_embeddings.items():
        for i, template_embedding in enumerate(embeddings):
            similarity = cosine_similarity_manual(input_embedding, template_embedding)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = templates[category][i]
                best_category = category
    
    return best_category, best_match, best_similarity

# 測試
'''
input_text = "我要看YouTube上的xx"
best_category, best_match, similarity = find_best_match(input_text, template_embeddings, model, tokenizer, device)
print(f"Best match: {best_match} in category {best_category} with similarity: {similarity}")
'''
