#!/bin/bash
for ip in `cat /home/jack/Documents/list_of_new_install`; do
    ssh-copy-id -i ~/.ssh/id_rsa.pub jack@$ip
done