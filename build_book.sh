#!/bin/bash
##
# Copyright (C) 2020 - 2021 by SenseTime Group Limited. All rights reserved.
# Liuxinhao <liuxinhao@senseauto.com>
##
ROOT_DIR=$(dirname $0)
python ${ROOT_DIR}/tools/summary-generator.py ${ROOT_DIR}/notes
gitbook build ${ROOT_DIR}/notes ${ROOT_DIR}/docs
