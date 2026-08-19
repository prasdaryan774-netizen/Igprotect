FROM php:8.3-cli

WORKDIR /app

COPY index.php .

CMD ["sh", "-c", "php -S 0.0.0.0:${PORT:-10000} -t /app"]
