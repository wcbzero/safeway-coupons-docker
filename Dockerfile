FROM python:3-alpine
RUN apk add tini
RUN pip install safeway-coupons
ENTRYPOINT ["/sbin/tini", "--"]
RUN mkdir /etc/cron.d \
    && ( \
        echo "10 10 * * * safeway-coupons -c /config/accounts >/proc/1/fd/1 2>/proc/1/fd/2" \
        ) >> /var/spool/cron/crontabs/root
ADD sendmail-pushover.py /
RUN chmod +x /sendmail-pushover.py && ln -sf /sendmail-pushover.py /usr/bin/sendmail && ln -sf /sendmail-pushover.py /usr/sbin/sendmail

CMD ["crond", "-f", "-d", "8"]