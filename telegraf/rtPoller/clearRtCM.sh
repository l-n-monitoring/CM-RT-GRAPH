#!/bin/bash

set -e

tmpFilesFind=$(find /etc/telegraf/telegraf.d/tmp* -mmin +5)

if [[ ! -z "$tmpFilesFind" ]]; then
	find /etc/telegraf/telegraf.d/tmp* -mmin +5 -exec rm {} \;
	systemctl reload telegraf.service
else
	echo "No files to delete!"
fi

