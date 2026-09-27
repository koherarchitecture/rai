# rai's keyed inference (rai/serve.py) for CapRover: CPU only, the current reader baked in, nothing logged.
# The key is never in the image: set RAI_API_KEY in the app's environment in CapRover.
FROM python:3.12-slim
RUN pip install --no-cache-dir torch==2.14.0 --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir transformers==5.17.0 pyyaml
WORKDIR /app
COPY rai/ rai/
COPY runs/ runs/
EXPOSE 8080
CMD ["python", "-m", "rai.serve", "8080"]
