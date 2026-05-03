# База данных
DATABASE_URL=sqlite:///./db.sqlite3

# Секретный ключ для JWT
SECRET_AUTH_KEY=your_secret_str

# Настройки сервера
PORT=8000
HOST=127.0.0.1

# Настройки загрузки картинок
IMAGE_DIR=image
MAX_IMAGE_SIZE=5242880

# Логирование
LOG_LEVEL=ERROR
LOG_FILE=logs/app.log
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=5