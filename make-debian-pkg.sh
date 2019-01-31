#!/usr/bin/env bash

echo '[INFO] Make sure the root folder is named pobkup-<VERSION>'
dpkg-buildpackage -uc -us
