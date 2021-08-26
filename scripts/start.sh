#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

exec uvicorn "core.main:app"