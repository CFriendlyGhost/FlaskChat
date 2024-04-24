from app import create_app
from app.events import socketio
from azure.storage.blob import BlobServiceClient, ContentSettings
import mimetypes




if __name__ == "__main__":
    app = create_app()
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
    # blob_client = container_client.get_blob_client("photo.png")

    # Upload the file to Azure Blob Storage
    # with open(photo_path, "rb") as data:
    #     blob_client.upload_blob(data, overwrite=True, content_settings=ContentSettings(content_type=content_type))
    #
    # print(blob_client.url)



