FROM python:3-alpine
RUN apk add tini
RUN pip install safeway-coupons
ENTRYPOINT ["/sbin/tini", "--"]
COPY safeway-accounts-file /
RUN mkdir /etc/cron.d \
    && ( \
        echo "10 10 * * * safeway-coupons -c /safeway-accounts-file >/proc/1/fd/1 2>/proc/1/fd/2" \
        ) >> /var/spool/cron/crontabs/root
CMD ["crond", "-f", "-d", "8"]