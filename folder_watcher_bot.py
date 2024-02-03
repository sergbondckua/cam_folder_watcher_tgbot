import asyncio
import logging
import os
import shutil

from aiogram import Bot
from aiogram.types import FSInputFile


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class FileManager:
    """
    A class responsible for file-related operations.
    """

    def __init__(self, folder_path: str):
        self.folder_path = folder_path

    def find_file_path(self) -> str:
        """
        Finds the path of a file within the specified folder.

        Returns:
        - The full path to the first file found within the folder.
        - If no files are found, an empty string is returned.
        """
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                return os.path.join(root, file)
        return ""


class FolderMonitor:
    """
    Monitors a specified folder for file uploads, sends the file as a photo,
    and deletes the file and its containing folder.
    """

    def __init__(self, folder_path: str, chat_id: int, telegram_bot: Bot):
        self.logger = logging.getLogger(__name__)
        self.folder_path = folder_path
        self.chat_id = chat_id
        self.telegram_bot = telegram_bot

    async def send_photo_and_delete(
        self, file_path: str, sub_folder: str
    ) -> None:
        """
        Sends the file as a photo to the specified chat ID and deletes the file and its folder.

        Args:
        - file_path: Path to the file to be sent.
        - sub_folder: Sub folder containing the file to be deleted.

        Raises:
        - Exception: If an error occurs during file sending or deletion.
        """
        photo = FSInputFile(str(file_path))
        folder_to_delete = os.path.join(self.folder_path, sub_folder)

        try:
            # Send the file as an image
            await self.telegram_bot.send_photo(
                chat_id=self.chat_id,
                photo=photo,
                caption=f"📂 <code>{file_path}</code>",
            )
            self.logger.info("File sent successfully.")

            # Clearing the folder
            shutil.rmtree(folder_to_delete)
            self.logger.info("File deleted: %s", file_path)
        except Exception as e:
            self.logger.error(
                "Error sending or deleting file %s: %s", sub_folder, e
            )

            if os.path.exists(folder_to_delete):
                shutil.rmtree(folder_to_delete)
                self.logger.warning(
                    "Folder deleted in the finally block: %s", folder_to_delete
                )

    async def monitor_folder(self) -> None:
        """
        Monitors the specified folder continuously, sending and deleting files when available.

        The method iterates indefinitely, checking for new files in the specified folder.
        If a file is found, it is sent as a photo to the specified Telegram chat,
        and both the file and its containing folder are deleted.

        The process repeats in a loop with a sleep interval of 1 second between iterations.
        """
        try:
            while True:
                contents = os.listdir(self.folder_path)
                if contents:
                    self.logger.info(
                        "The folder is not empty! File is being uploaded and deleted..."
                    )
                    sub_folder = contents[0]
                    file_path = FileManager(self.folder_path).find_file_path()
                    await self.send_photo_and_delete(file_path, sub_folder)

                await asyncio.sleep(1)
        except asyncio.CancelledError:
            # Catch CancelledError to allow graceful shutdown
            pass
        finally:
            await self.telegram_bot.session.close()
