#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=.
python -m pytest apps/api/blackletter_api/tests -q
