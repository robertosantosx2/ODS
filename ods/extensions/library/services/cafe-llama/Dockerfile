# Optional cafe-llama.cpp runtime image (scaffold).
# Prefers downloading a prebuilt llama-server from upstream releases when
# CAFE_LLAMA_RELEASE_URL is provided at build time; otherwise expects the
# binary to be supplied by a follow-up image layer or bind mount.
FROM ubuntu:24.04

RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/cafe-llama

ARG CAFE_LLAMA_RELEASE_URL=""
RUN if [ -n "$CAFE_LLAMA_RELEASE_URL" ]; then \
      curl -fsSL "$CAFE_LLAMA_RELEASE_URL" -o /tmp/cafe.tgz \
      && tar -xzf /tmp/cafe.tgz -C /opt/cafe-llama \
      && rm -f /tmp/cafe.tgz \
      && (test -x /opt/cafe-llama/llama-server || find /opt/cafe-llama -type f -name llama-server -exec cp {} /usr/local/bin/llama-server \;); \
    fi

COPY entrypoint.sh /usr/local/bin/cafe-llama-entrypoint.sh
RUN chmod +x /usr/local/bin/cafe-llama-entrypoint.sh

EXPOSE 8081
ENTRYPOINT ["/usr/local/bin/cafe-llama-entrypoint.sh"]
