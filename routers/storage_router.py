import io
from fastapi import APIRouter, UploadFile, File
from config.minio_config import minio_client

router = APIRouter(
    prefix='/storage',
    tags=['Storage']
)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_content = await file.read()

        minio_client.put_object("img", file.filename, io.BytesIO(file_content), len(file_content), file.content_type)

        file_url = f"http://localhost:9000/img/{file.filename}"
        return {
            "status": 200,
            "file_url": file_url
        }
    except Exception as err:
        return {"error": str(err)}
