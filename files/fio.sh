#!/bin/bash
set -e

base_dir=$(dirname $0)

rm -rf results
mkdir results
cp "$base_dir/fio.job" results/ # for reference

run_fio() {
  echo fio "$@" >fio-cmdline
  fio "$@"
}

for iodepth in 1 2 4 8 16 32 64 128; do
  results_dir=results/iodepth/$iodepth
  mkdir -p "$results_dir"
  cd "$results_dir"
  run_fio --output-format=json \
          --output=fio-output.json \
          --iodepth $iodepth \
	  "$base_dir/fio.job"
  cd -
done
