from flask import Flask, request, send_file
import whisper
import os
from deep_translator import GoogleTranslator

app = Flask(__name__)
model = whisper.load_model("tiny") # Server-la fast-ah run aaga tiny best

@app.route("/process", methods=["POST"])
def process_video():
    file = request.files['video']
    lang = request.form.get('lang')
    
    video_path = "temp_video.mp4"
    file.save(video_path)
    
    # AI Transcription
    result = model.transcribe(video_path, task="translate")
    
    # Subtitle Formatting Logic
    translator = GoogleTranslator(source='auto', target='ta')
    srt_content = ""
    for i, seg in enumerate(result["segments"]):
        txt = seg["text"].strip()
        if lang == "tamil":
            final = translator.translate(txt)
        elif lang == "both":
            final = f"{txt}\n{translator.translate(txt)}"
        else:
            final = txt
        srt_content += f"{i+1}\n00:00:00,000 --> 00:00:10,000\n{final}\n\n"
    
    with open("output.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)
        
    return send_file("output.srt", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))