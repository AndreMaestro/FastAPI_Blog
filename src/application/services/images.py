import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from typing import List
from core.config import settings

class ImageService:
    @staticmethod
    async def save_images(
            files: List[UploadFile],
            content_type: str,
            object_id: int
    ) -> List[str]:
        if not files: return []
        saved_paths = []
        upload_dir = Path(settings.IMAGE_DIR) / f"{content_type}s" / str(object_id)
        upload_dir.mkdir(parents=True, exist_ok=True)

        for order, file in enumerate(files):
            content = await file.read()
            if len(content) > settings.MAX_IMAGE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Файл слишком большой. Максимальный размер {settings.MAX_IMAGE_SIZE // (1024*1024)} MB"
                )

            ext = file.filename.split(".")[-1].lower()
            if ext not in ["jpeg", "jpg", "png"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Неподдерживаемый формат. Разрешены: jpeg, jpg, png"
                )

            unique_name: str = f"{uuid.uuid4()}.{ext}"
            file_path = upload_dir / unique_name

            with open(file_path, "wb") as buffer:
                buffer.write(content)

            saved_paths.append(f"{settings.IMAGE_DIR}/{content_type}s/{object_id}/{unique_name}")

        return saved_paths


    @staticmethod
    async def delete_images(image_paths: List[str]):
        for path in image_paths:
            p = Path(path)
            if p.exists():
                p.unlink()

    @staticmethod
    async def delete_image(image_path: str):
        path = Path(image_path)
        if path.exists():
            path.unlink()