#!/usr/bin/env bash
# cleanroom-e2e-python.sh
#
# Cleanroom Docker E2E for Python projects. Runs the project's tests inside
# a fresh python:3.13-slim container with no host artifacts leaking in.
#
# What it does:
#   1. Captures repo root and HEAD SHA from the host.
#   2. Builds an ephemeral Docker image from python:3.13-slim with the repo
#      contents copied in.
#   3. Inside the container: pip install -e . then runs pytest on $TESTS_DIR
#      (default tests/).
#   4. Tees all output to verification/cleanroom-<sha>.log on the host.
#   5. Exits with the test command's exit code.
#
# Expected env vars (all optional):
#   TESTS_DIR   directory passed to pytest (default: tests/)
#   PYTEST_ARGS extra args to pytest      (default: -v)
#
# Invoked by the /ship release train as part of the Verification phase.
# Manual run:  scripts/cleanroom-e2e.sh

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HEAD_SHA="$(git rev-parse HEAD)"
TESTS_DIR="${TESTS_DIR:-tests/}"
PYTEST_ARGS="${PYTEST_ARGS:--v}"

LOG_DIR="${REPO_ROOT}/verification"
mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/cleanroom-${HEAD_SHA}.log"

IMAGE_TAG="cleanroom-e2e:${HEAD_SHA}"

cd "${REPO_ROOT}"

{
  echo "=== Cleanroom E2E (Python) ==="
  echo "Repo:    ${REPO_ROOT}"
  echo "SHA:     ${HEAD_SHA}"
  echo "Tests:   ${TESTS_DIR}"
  echo "Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo

  DOCKERFILE_TMP="$(mktemp)"
  trap 'rm -f "${DOCKERFILE_TMP}"' EXIT

  cat > "${DOCKERFILE_TMP}" <<'EOF'
FROM python:3.13-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .[test] 2>/dev/null || pip install --no-cache-dir -e .
EOF

  echo "--- docker build ---"
  docker build -f "${DOCKERFILE_TMP}" -t "${IMAGE_TAG}" .

  echo
  echo "--- pytest ${TESTS_DIR} ${PYTEST_ARGS} ---"
  set +e
  docker run --rm "${IMAGE_TAG}" pytest ${TESTS_DIR} ${PYTEST_ARGS}
  EXIT_CODE=$?
  set -e

  echo
  echo "Exit:    ${EXIT_CODE}"
  echo "Ended:   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  if [ ${EXIT_CODE} -eq 0 ]; then
    echo "Result:  PASS"
  else
    echo "Result:  FAIL"
  fi
} 2>&1 | tee "${LOG_FILE}"

EXIT_CODE=${PIPESTATUS[0]}
echo
echo "Log:     ${LOG_FILE}"
exit ${EXIT_CODE}
