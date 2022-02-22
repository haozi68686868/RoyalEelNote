#!/bin/bash
##
# Copyright (C) 2020 - 2021 by SenseTime Group Limited. All rights reserved.
# Liuxinhao <liuxinhao@senseauto.com>
##
ROOT_DIR=$(dirname $0)
project=$1
if [[ x$project = x ]]; then
    project=notes
fi
python ${ROOT_DIR}/tools/summary-generator.py ${ROOT_DIR}/${project}
gitbook pdf ${ROOT_DIR}/${project} ${ROOT_DIR}/${project}.pdf
