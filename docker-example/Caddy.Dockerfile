FROM library/caddy

COPY --from=local/nextpy-app /app/.web/_static /srv
ADD Caddyfile /etc/caddy/Caddyfile