#!/usr/bin/env bash
set -o errexit

set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

main() {
    yum update -y
    yum -y install httpd php
    chkconfig httpd on
    service httpd start
    echo "--- Provisioning Complete ---"
}

main "$@"