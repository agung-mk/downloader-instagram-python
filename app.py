from flask import Flask, render_template, request, send_file, jsonify  
import yt_dlp  
import os  
  
app = Flask(__name__)  
  
# Pastikan folder downloads tersedia  
os.makedirs('downloads', exist_ok=True)  
  
def download_facebook_video(url):  
    """Mengunduh video dari Facebook menggunakan yt-dlp"""  
    ydl_opts = {  
        'format': 'best',  
        'outtmpl': 'downloads/%(title)s.%(ext)s',  
    }  
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  
        info = ydl.extract_info(url, download=True)  
        filename = ydl.prepare_filename(info)  
    return filename  
  
@app.route('/', methods=['GET', 'POST'])  
def index():  
    """Tampilan halaman utama"""  
    if request.method == 'POST':  
        url = request.form.get('url')  
        if url:  
            video_path = download_facebook_video(url)  
            return send_file(video_path, as_attachment=True)  
    return render_template('index.html')  
  
@app.route('/api/download', methods=['POST'])  
def api_download():  
    """  
    API Endpoint untuk mengunduh video Facebook.  
  
    Request:  
    - POST JSON: { "url": "https://www.facebook.com/video-url" }  
  
    Response:  
    - Jika berhasil: { "status": "success", "download_url": "http://server.com/downloads/video.mp4" }  
    - Jika gagal: { "status": "error", "message": "Video tidak ditemukan" }  
    """  
    try:  
        data = request.get_json()  
        url = data.get('url')  
  
        if not url:  
            return jsonify({"status": "error", "message": "URL tidak ditemukan"}), 400  
  
        video_path = download_facebook_video(url)  
        video_filename = os.path.basename(video_path)  
        download_url = f"{request.host_url}downloads/{video_filename}"  
  
        return jsonify({"status": "success", "download_url": download_url})  
  
    except Exception as e:  
        return jsonify({"status": "error", "message": str(e)}), 500  
  
@app.route('/downloads/<filename>')  
def serve_video(filename):  
    """Mengakses video yang telah diunduh"""  
    return send_file(f"downloads/{filename}", as_attachment=True)  
  
if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000, debug=True)
