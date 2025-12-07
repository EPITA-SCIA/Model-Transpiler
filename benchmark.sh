#!/usr/bin/env bash
exec 2>/dev/null # Suppress all stderr output (warnings)

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODELS_DIR="$ROOT/models"
OUTPUTS_DIR="$ROOT/outputs"

models=("$MODELS_DIR"/*.joblib "$MODELS_DIR"/*.pt "$MODELS_DIR"/*.pth)

for model in "${models[@]}"; do
	stem="$(basename "$model")"
	stem_no_ext="${stem%.*}"
	echo -e "====================MODEL: $stem===================="

	python "$ROOT/main.py" --path "$model" --c --v

	c_source="$OUTPUTS_DIR/${stem_no_ext}.c"
	v_source="$OUTPUTS_DIR/${stem_no_ext}.v"
	c_bin="$OUTPUTS_DIR/${stem_no_ext}_c.out"
	v_bin="$OUTPUTS_DIR/${stem_no_ext}_v.out"

	if [ ! -f "$c_source" ] || [ ! -f "$v_source" ]; then
		echo "Missing generated sources for $stem" >&2
		continue
	fi

	gcc -std=c99 -O2 -lm "$c_source" -o "$c_bin"
	iverilog -o "$v_bin" "$v_source"

	input_args="1 2 3"

	hyperfine --runs 1 "python $ROOT/time_inference.py --path $model --inputs $input_args"

	echo "Benchmarking $stem_no_ext (C vs Verilog)"
	hyperfine \
		"\"$c_bin\" $input_args" \
		"\"$v_bin\" $input_args"
done
