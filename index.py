from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_audio():
    url = request.form['url']
    
    # Configure yt-dlp to download audio and convert to mp3
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s', # Save to a 'downloads' folder
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        # Create downloads directory if it doesn't exist
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Change extension to .mp3 because of post-processing
            mp3_filename = filename.rsplit('.', 1)[0] + '.mp3'
            
        return send_file(mp3_filename, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
