#!/usr/bin/env bash
# Probe the data hosts the adhi-climate pipelines download from, and report
# which are reachable from this machine. Read-only: one tiny ranged request
# per host. Exit code 0 if every REQUIRED host answered, 1 otherwise.
#
# Usage: tools/check-data-access.sh
#
# In a Claude Code remote session, BLOCKED means the environment's network
# policy refused the connection at the gateway. The fix is a one-time change
# to the environment's network access settings; the domain table lives in
# bushfire-weather/EXECUTION_PROMPT.md.
set -u

fails=0

probe() {
  local req="$1" name="$2" url="$3" code
  code=$(curl -sS -o /dev/null -m 25 -L --range 0-400 -w '%{http_code}' \
    -A "adhi-climate access probe (github.com/lumbalumbaputih/adhi-climate)" \
    "$url" 2>/dev/null)
  case "$code" in
    2*|3*) printf 'ok       %-9s %-34s HTTP %s\n' "$req" "$name" "$code" ;;
    000)   printf 'BLOCKED  %-9s %-34s no connection (gateway/policy)\n' "$req" "$name"
           [ "$req" = "required" ] && fails=1 ;;
    *)     printf 'DENIED   %-9s %-34s HTTP %s\n' "$req" "$name" "$code"
           [ "$req" = "required" ] && fails=1 ;;
  esac
}

echo "Probing data hosts (one tiny request each)..."
echo

# Required by bushfire-weather (project #11)
probe required "Open-Meteo ERA5 archive" \
  "https://archive-api.open-meteo.com/v1/archive?latitude=-31.95&longitude=115.86&start_date=2020-01-01&end_date=2020-01-02&daily=temperature_2m_max&timezone=auto"
probe required "NOAA NCEI data service (GHCN)" \
  "https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=ASN00009021&startDate=2020-01-01&endDate=2020-01-02&dataTypes=TMAX&format=csv"

# Required by high-water (project #12)
probe required "UHSLC tide gauges (hourly)" \
  "https://uhslc.soest.hawaii.edu/data/csv/rqds/indian/hourly/h175a.csv"

# Used by other projects' pipelines and re-runs
probe optional "NOAA PSL downloads (ERSSTv5)" \
  "https://downloads.psl.noaa.gov/Datasets/noaa.ersst.v5/"
probe optional "NOAA CoastWatch ERDDAP" \
  "https://coastwatch.pfeg.noaa.gov/erddap/index.html"
probe optional "PSMSL tide gauges" \
  "https://psmsl.org/data/"
probe optional "AEMO WEM data portal" \
  "https://data.wa.aemo.com.au/"
probe optional "Bureau of Meteorology" \
  "http://www.bom.gov.au/climate/data/"

echo
if [ "$fails" -eq 0 ]; then
  echo "Required hosts reachable: the self-fetch pipelines can run."
else
  echo "Required hosts unreachable: fix the environment network settings"
  echo "(see the project's EXECUTION_PROMPT.md) or stage files in dropzone/."
fi
exit "$fails"
