import gdown

# Set the Google Drive video URL
video_url =  'sample gdrive public url'

# Extract the file ID from the URL
file_id = video_url.split('/')[-2]

# Construct the download URL
download_url = f'https://drive.google.com/uc?id={file_id}'

# Set the output file path
output_path = 'sample output.mp4'

# Download the video
gdown.download(download_url, output_path, quiet=False)

print('Video downloaded successfully.')
