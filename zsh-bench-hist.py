#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This application processes the output of `zsh-bench --raw` to visualize it as ASCII histograms."""

import argparse
import math
import re
import sys
import statistics


def extract_timings(output):
    """Tested to be compatible with `zsh-bench --raw` as of 2024.04.04 
    (https://github.com/romkatv/zsh-bench/commit/3b4896c4840c64bea8e79b8392a93dfdc5a0a096)"""
    timings = {}
    pattern = r'(\w+)\s*=\(\s*([\d. ]+)\)'
    matches = re.findall(pattern, output)
    for match in matches:
        name = match[0]
        values = [float(value) for value in match[1].split()]
        timings[name] = values
    return timings


def print_metric_info(metric: str, min_value: float, median_value: float, max_value: float,
                      width: int = 9, precision: int = 3):
    float_format = f'{width}.{precision}f'
    print(f'{metric:{width}} = {min_value:{float_format}}, {median_value:{float_format}}, {max_value:{float_format}}')


def print_constant_info(metric: str, value: int, width=20):
    print(f'{metric:{width}} = {value}')


def generate_histogram(data: tuple, bin_count: int, min_value: float, bin_width: float) -> list[int]:
    """Generate a list containing the count of hits for the bin."""
    assert bin_count >= 1
    histogram = [0] * bin_count

    for item in data:
        bin_index = int((item - min_value) // bin_width)
        bin_index = min(bin_index, bin_count - 1)  # The last bin's upper limit is inclusive
        histogram[bin_index] += 1

    return histogram


def display_histogram(histogram: list, bin_width: float, min_value: float = 0.0, float_format: str = '9.3f',
                      bar_symbol: str = '*'):
    """Display a histogram in textual form."""
    last_bin_index = len(histogram) - 1
    for bin_index, value in enumerate(histogram):
        bin_start = min_value + bin_width * bin_index
        bin_end = min_value + bin_width * (bin_index + 1)
        bar = bar_symbol * value
        interval_closing_brace = ']' if bin_index == last_bin_index else ')'
        print(f'[{bin_start:{float_format}}, {bin_end:{float_format}}{interval_closing_brace}:', bar)


def display_timing_histograms(timings: dict, bin_count: int, logarithmic: bool):
    """Visualize the timings as textual histogram each."""
    for name, values in timings.items():
        print(f'Histogram for {name}')
        min_value = min(values)
        max_value = max(values)
        bin_width = (max_value - min_value) / bin_count

        histogram = generate_histogram(data=values, bin_count=bin_count, min_value=min_value, bin_width=bin_width)

        if logarithmic:
            histogram = [math.ceil(math.log(x+1, 2)) for x in histogram]

        display_histogram(histogram, min_value=min_value, bin_width=bin_width)
        print()


def display_timings(timings: dict, bin_count: int, logarithmic: bool = False):
    """Display the settings and visualize the timings as textual histogram each."""
    constants = ['creates_tty', 'has_compsys', 'has_syntax_highlighting', 'has_autosuggestions', 'has_git_prompt']
    table_width = max(map(len, timings.keys()))  # calculate width for formatting the table

    print('Settings')
    for constant in constants:
        values = timings[constant]
        assert min(values) == max(values), f'Value of {constant!r} apparently changed during benchmark. Run it again.'
        value = values[0]
        value = int(value) if int(value) == value else value
        print_constant_info(metric=constant, value=value, width=table_width)
        timings.pop(constant)
    print()

    print(f'{"Benchmark":{table_width}}  ',
          f'{"min_value":>{table_width}}, {"median_value":>{table_width}}, {"max_value":>{table_width}}')
    for metric, values in timings.items():
        min_value = min(values)
        median_value = statistics.median(values)
        max_value = max(values)
        print_metric_info(metric, min_value, median_value, max_value, width=table_width)
    print()

    display_timing_histograms(timings, bin_count=bin_count, logarithmic=logarithmic)


def main():
    """Parse zsh-bench data from stdin, Display the settings, and Visualize the timings as textual histogram each."""
    parser = argparse.ArgumentParser(description='Visualizer of zsh-bench --raw output')
    parser.add_argument('--bin-count', type=int, default=10, help='Histogram bin count (default: 10, minimum: 1).')
    parser.add_argument('--logarithmic', action='store_true', help='Use logarithmic histogram mode.')


    args = parser.parse_args()
    command_output = sys.stdin.read()
    timings = extract_timings(command_output)
    display_timings(timings=timings, bin_count=args.bin_count, logarithmic=args.logarithmic)


if __name__ == '__main__':
    main()
