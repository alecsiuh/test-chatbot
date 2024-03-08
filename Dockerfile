FROM gcr.io/cloudsql-docker/gce-proxy:1.19.1

ENV CLOUD_SQL_CONNECTION = ${INSTANCE_CONNECTION_NAME}
ENV DB_USER = ${DB_USER}
ENV DB_PASS = ${DB_PASSWORD}
ENV DB_NAME = ${DB_NAME}

# Copy the service account key file into the container
COPY ./fan-analytic-chatbot-7f018b20fd46.json /config/keyfile.json

# Start the Cloud SQL Proxy
CMD ["/cloud_sql_proxy", "-instances=fan-analytic-chatbot:europe-west1:fan-analytic-chatbot=tcp:3306", "-credential_file=/config/keyfile.json"]
