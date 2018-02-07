ARG BUILD_FROM
FROM $BUILD_FROM

# Add env
ENV LAN# Setup
RUN apk add --no-cache python3 python3-dev gcc linux-headers musl-dev tcpdump \
    && pip3 install --no-cache --upgrade pipG C.UTF-8

# Setup base, install sox package
RUN apk add --no-cache jq sox

# Copy  data
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ] 
