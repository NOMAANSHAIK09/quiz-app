# from flask import Flask, json, render_template, request, jsonify, session, redirect, url_for



# import requests

# key="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"

# # quiz_topic = input("Enter the quiz topic: ")

# # difficulty = input("Enter the difficulty level (easy, medium, hard): ")
# app = Flask(__name__)
# @app.route("/")
# def home():
    
#     return render_template("index.html")

# @app.route("/start_quiz", methods=["GET", "POST"])
# def start_quiz():
#     outputs=0
#     result=0
#     if request.method == "POST":
        
#         quiz_topic = request.form.get("quiz_topic")
#         difficulty = request.form.get("difficulty")

#         system_prompt = f"""
#         Generate 5 quiz questions on '{quiz_topic}' with '{difficulty}' difficulty.
#         Return in JSON format like:
#         [
#           {{
#             "question": "...",
#             "options": ["A", "B", "C", "D"],
#             "answer": "..."
#           }}
#         ]
#         """
#         url="https://openrouter.ai/api/v1/chat/completions"

#         headers = {
#                 "Authorization":f"Bearer {key}",
#                 "Content-type":"application/json"
#             }

#         payload = {
#                 "model":"deepseek/deepseek-chat",
#                 "messages":[
#                     {"role":"system","content":system_prompt},
#                     {"role":"user","content":f'Analyze:"{quiz_topic}" and difficulty:"{difficulty}"'}
#                 ],
#                 "temperature":0.7,
#             }

#         response = requests.post(url, headers=headers, json=payload)
#         if response.status_code == 200:
#                     quiz_data = response.json()
#                     outputs = quiz_data['choices'][0]['message']['content']
                      
                    
#         else:
#                 print("error")
                
#         result = jsonify(outputs)
    
#     return render_template("start_quiz.html", outputs=result)
            
   
# if __name__ == "__main__":
#     app.run(debug=True)
    
