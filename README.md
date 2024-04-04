# zsh-bench-hist
This application processes the output of `zsh-bench --raw` to visualize it as ASCII histograms.

# Usage
```sh
zsh-bench --raw --iters 100 | python3 zsh-bench-hist.py --bin-count 10
```

**Note:** As benchmark with many iterations might take a while, it may be useful to send the output of `zsh-bench --raw` to a file and process it later if you want to experiment with the `--bin-count` option:
```sh
zsh-bench --raw --iters 100 > zsh-bench-1.log
cat zsh-bench-1.log | python3 zsh-bench-hist.py --bin-count 10
```


# Example Output
```
Settings
creates_tty             = 0
has_compsys             = 1
has_syntax_highlighting = 1
has_autosuggestions     = 1
has_git_prompt          = 1

Benchmark                               min_value,            median_value,               max_value
first_prompt_lag_ms     =                  11.678,                  13.438,                  22.217
first_command_lag_ms    =                 115.986,                 120.724,                 158.821
command_lag_ms          =                  11.206,                  15.480,                  18.518
input_lag_ms            =                  12.002,                  12.424,                  13.451
exit_time_ms            =                   9.855,                  11.861,                  16.469

Histogram for first_prompt_lag_ms
[   11.678,    12.732): ******************
[   12.732,    13.786): *****************************************
[   13.786,    14.840): **************************
[   14.840,    15.894): *****
[   15.894,    16.947): ***
[   16.947,    18.001): **
[   18.001,    19.055): ***
[   19.055,    20.109): 
[   20.109,    21.163): *
[   21.163,    22.217]: *

Histogram for first_command_lag_ms
[  115.986,   120.270): ******************************************
[  120.270,   124.553): *******************************
[  124.553,   128.837): *********
[  128.837,   133.120): ****
[  133.120,   137.404): *******
[  137.404,   141.687): **
[  141.687,   145.970): **
[  145.970,   150.254): *
[  150.254,   154.537): *
[  154.537,   158.821]: *

Histogram for command_lag_ms
[   11.206,    11.937): *
[   11.937,    12.668): 
[   12.668,    13.400): 
[   13.400,    14.131): *
[   14.131,    14.862): ***********
[   14.862,    15.593): *********************************************
[   15.593,    16.324): *************************
[   16.324,    17.056): *********
[   17.056,    17.787): *****
[   17.787,    18.518]: ***

Histogram for input_lag_ms
[   12.002,    12.147): ***********
[   12.147,    12.292): *****************
[   12.292,    12.437): ************************
[   12.437,    12.582): *********************
[   12.582,    12.727): ******************
[   12.727,    12.871): ******
[   12.871,    13.016): 
[   13.016,    13.161): *
[   13.161,    13.306): 
[   13.306,    13.451]: **

Histogram for exit_time_ms
[    9.855,    10.516): ***************
[   10.516,    11.178): **********************
[   11.178,    11.839): *************
[   11.839,    12.501): *******************
[   12.501,    13.162): *****************
[   13.162,    13.823): *****
[   13.823,    14.485): ****
[   14.485,    15.146): **
[   15.146,    15.808): *
[   15.808,    16.469]: **
```
