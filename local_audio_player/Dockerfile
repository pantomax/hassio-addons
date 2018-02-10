ARG BUILD_FROM
FROM $BUILD_FROM

# Add env
ENV LANG C.UTF-8

# Setup base, install sox package
RUN apk add --no-cache jq sox

# Copy data
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ] 
