# Stage 1: init
FROM python:3.11 as init

# Pass `--build-arg API_URL=http://app.example.com:8000` during build
ARG API_URL

# Copy local context to `/app` inside container (see .dockerignore)
WORKDIR /app
COPY . .

# Create virtualenv which will be copied into final container
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3.11 -m venv $VIRTUAL_ENV

# Install app requirements and nextpy inside virtualenv
RUN pip install -r requirements.txt

# Deploy templates and prepare app
RUN nextpy init

# Export static copy of frontend to /app/.web/_static
RUN nextpy export --frontend-only --no-zip

# Copy static files out of /app to save space in backend image
RUN mv .web/_static /tmp/_static
RUN rm -rf .web && mkdir .web
RUN mv /tmp/_static .web/_static

# Stage 2: copy artifacts into slim image 
FROM python:3.11-slim
ARG API_URL
WORKDIR /app
RUN adduser --disabled-password --home /app nextpy
COPY --chown=nextpy --from=init /app /app
USER nextpy
ENV PATH="/app/.venv/bin:$PATH" API_URL=$API_URL

CMD nextpy db migrate && nextpy run --env prod --backend-only
