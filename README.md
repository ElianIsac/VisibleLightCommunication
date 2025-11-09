# VisibleLightCommunication

start: 2cm

run1:2 X
run2:5 X
run3:8 X
run4:11 X
run5:14 X
run6:17 X
run7:20 X

0
3
6
9
12
15
18

end: ~20cm


❯ python analyze_logs.py
🧪 run1: payload=100B → img/run1/100B

📊 Stats for 100B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]    96.51  0.22    96.44    96.57
1        Delay [ms]  1026.01  9.27  1023.32  1028.71
🧪 run1: payload=180B → img/run1/180B

📊 Stats for 180B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]   106.46  0.20   106.40   106.51
1        Delay [ms]  1678.98  8.31  1676.57  1681.39
🧪 run1: payload=1B → img/run1/1B

📊 Stats for 1B:
             metric    mean   std  ci_low  ci_high
0  Throughput [B/s]    4.38  0.05    4.36     4.39
1        Delay [ms]  217.03  7.78  214.82   219.24
✅ Finished run1, saved in img/run1/
🧪 run2: payload=100B → img/run2/100B

📊 Stats for 100B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]    96.29  0.23    96.22    96.36
1        Delay [ms]  1026.00  7.49  1023.82  1028.17
🧪 run2: payload=180B → img/run2/180B

📊 Stats for 180B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]   106.43  0.06   106.41   106.45
1        Delay [ms]  1678.89  6.59  1676.97  1680.80
🧪 run2: payload=1B → img/run2/1B

📊 Stats for 1B:
             metric    mean   std  ci_low  ci_high
0  Throughput [B/s]    4.40  0.08    4.38     4.42
1        Delay [ms]  216.73  8.16  214.41   219.05
✅ Finished run2, saved in img/run2/
🧪 run3: payload=100B → img/run3/100B

📊 Stats for 100B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]    96.32  0.40    96.20    96.43
1        Delay [ms]  1027.16  9.32  1024.45  1029.86
🧪 run3: payload=180B → img/run3/180B

📊 Stats for 180B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]   106.29  0.08   106.27   106.31
1        Delay [ms]  1681.62  6.83  1679.64  1683.61
🧪 run3: payload=1B → img/run3/1B

📊 Stats for 1B:
             metric    mean   std  ci_low  ci_high
0  Throughput [B/s]    4.35  0.03    4.34     4.36
1        Delay [ms]  217.33  8.72  214.85   219.81
✅ Finished run3, saved in img/run3/
🧪 run4: payload=100B → img/run4/100B

📊 Stats for 100B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]    96.27  0.12    96.23    96.30
1        Delay [ms]  1025.75  7.68  1023.52  1027.98
🧪 run4: payload=180B → img/run4/180B

📊 Stats for 180B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]   106.47  0.13   106.44   106.51
1        Delay [ms]  1679.57  7.98  1677.25  1681.88
🧪 run4: payload=1B → img/run4/1B

📊 Stats for 1B:
             metric    mean    std  ci_low  ci_high
0  Throughput [B/s]    4.36   0.07    4.34     4.38
1        Delay [ms]  219.99  13.87  216.05   223.94
✅ Finished run4, saved in img/run4/
🧪 run5: payload=100B → img/run5/100B

📊 Stats for 100B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]    96.28  0.13    96.24    96.31
1        Delay [ms]  1025.54  6.26  1023.72  1027.36
🧪 run5: payload=180B → img/run5/180B

📊 Stats for 180B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]   106.44  0.08   106.41   106.46
1        Delay [ms]  1679.49  7.80  1677.23  1681.75
🧪 run5: payload=1B → img/run5/1B

📊 Stats for 1B:
             metric    mean   std  ci_low  ci_high
0  Throughput [B/s]    4.38  0.05    4.37     4.40
1        Delay [ms]  216.95  9.04  214.38   219.52
✅ Finished run5, saved in img/run5/
🧪 run6: payload=100B → img/run6/100B

📊 Stats for 100B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]    96.50  0.20    96.44    96.55
1        Delay [ms]  1025.57  7.08  1023.51  1027.62
🧪 run6: payload=180B → img/run6/180B

📊 Stats for 180B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]   106.51  0.25   106.43   106.58
1        Delay [ms]  1679.92  7.42  1677.76  1682.07
🧪 run6: payload=1B → img/run6/1B

📊 Stats for 1B:
             metric    mean   std  ci_low  ci_high
0  Throughput [B/s]    4.38  0.05    4.36     4.39
1        Delay [ms]  216.39  6.57  214.53   218.26
✅ Finished run6, saved in img/run6/
🧪 run7: payload=100B → img/run7/100B

📊 Stats for 100B:
             metric     mean     std   ci_low  ci_high
0  Throughput [B/s]    72.19   10.72    69.08    75.30
1        Delay [ms]  1480.31  957.12  1202.39  1758.23
🧪 run7: payload=180B → img/run7/180B

📊 Stats for 180B:
             metric     mean      std   ci_low  ci_high
0  Throughput [B/s]    77.68     8.72    75.17    80.18
1        Delay [ms]  2391.98  1493.67  1962.95  2821.01
🧪 run7: payload=1B → img/run7/1B

📊 Stats for 1B:
             metric    mean     std  ci_low  ci_high
0  Throughput [B/s]    2.72    0.46    2.59     2.85
1        Delay [ms]  375.59  262.41  301.02   450.17
✅ Finished run7, saved in img/run7/
🧪 run1: payload=100B → img/run1/100B

📊 Stats for 100B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]    96.51  0.22    96.44    96.57
1        Delay [ms]  1026.01  9.27  1023.32  1028.71
🧪 run1: payload=180B → img/run1/180B

📊 Stats for 180B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]   106.46  0.20   106.40   106.51
1        Delay [ms]  1678.98  8.31  1676.57  1681.39
🧪 run1: payload=1B → img/run1/1B

📊 Stats for 1B:
             metric    mean   std  ci_low  ci_high
0  Throughput [B/s]    4.38  0.05    4.36     4.39
1        Delay [ms]  217.03  7.78  214.82   219.24
✅ Finished run1, saved in img/run1/
🧪 run2: payload=100B → img/run2/100B

📊 Stats for 100B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]    96.29  0.23    96.22    96.36
1        Delay [ms]  1026.00  7.49  1023.82  1028.17
🧪 run2: payload=180B → img/run2/180B

📊 Stats for 180B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]   106.43  0.06   106.41   106.45
1        Delay [ms]  1678.89  6.59  1676.97  1680.80
🧪 run2: payload=1B → img/run2/1B

📊 Stats for 1B:
             metric    mean   std  ci_low  ci_high
0  Throughput [B/s]    4.40  0.08    4.38     4.42
1        Delay [ms]  216.73  8.16  214.41   219.05
✅ Finished run2, saved in img/run2/
🧪 run3: payload=100B → img/run3/100B

📊 Stats for 100B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]    96.32  0.40    96.20    96.43
1        Delay [ms]  1027.16  9.32  1024.45  1029.86
🧪 run3: payload=180B → img/run3/180B

📊 Stats for 180B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]   106.29  0.08   106.27   106.31
1        Delay [ms]  1681.62  6.83  1679.64  1683.61
🧪 run3: payload=1B → img/run3/1B

📊 Stats for 1B:
             metric    mean   std  ci_low  ci_high
0  Throughput [B/s]    4.35  0.03    4.34     4.36
1        Delay [ms]  217.33  8.72  214.85   219.81
✅ Finished run3, saved in img/run3/
🧪 run4: payload=100B → img/run4/100B

📊 Stats for 100B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]    96.27  0.12    96.23    96.30
1        Delay [ms]  1025.75  7.68  1023.52  1027.98
🧪 run4: payload=180B → img/run4/180B

📊 Stats for 180B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]   106.47  0.13   106.44   106.51
1        Delay [ms]  1679.57  7.98  1677.25  1681.88
🧪 run4: payload=1B → img/run4/1B

📊 Stats for 1B:
             metric    mean    std  ci_low  ci_high
0  Throughput [B/s]    4.36   0.07    4.34     4.38
1        Delay [ms]  219.99  13.87  216.05   223.94
✅ Finished run4, saved in img/run4/
🧪 run5: payload=100B → img/run5/100B

📊 Stats for 100B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]    96.28  0.13    96.24    96.31
1        Delay [ms]  1025.54  6.26  1023.72  1027.36
🧪 run5: payload=180B → img/run5/180B

📊 Stats for 180B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]   106.44  0.08   106.41   106.46
1        Delay [ms]  1679.49  7.80  1677.23  1681.75
🧪 run5: payload=1B → img/run5/1B

📊 Stats for 1B:
             metric    mean   std  ci_low  ci_high
0  Throughput [B/s]    4.38  0.05    4.37     4.40
1        Delay [ms]  216.95  9.04  214.38   219.52
✅ Finished run5, saved in img/run5/
🧪 run6: payload=100B → img/run6/100B

📊 Stats for 100B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]    96.50  0.20    96.44    96.55
1        Delay [ms]  1025.57  7.08  1023.51  1027.62
🧪 run6: payload=180B → img/run6/180B

📊 Stats for 180B:
             metric     mean   std   ci_low  ci_high
0  Throughput [B/s]   106.51  0.25   106.43   106.58
1        Delay [ms]  1679.92  7.42  1677.76  1682.07
🧪 run6: payload=1B → img/run6/1B

📊 Stats for 1B:
             metric    mean   std  ci_low  ci_high
0  Throughput [B/s]    4.38  0.05    4.36     4.39
1        Delay [ms]  216.39  6.57  214.53   218.26
✅ Finished run6, saved in img/run6/
🧪 run7: payload=100B → img/run7/100B

📊 Stats for 100B:
             metric     mean     std   ci_low  ci_high
0  Throughput [B/s]    72.19   10.72    69.08    75.30
1        Delay [ms]  1480.31  957.12  1202.39  1758.23
🧪 run7: payload=180B → img/run7/180B

📊 Stats for 180B:
             metric     mean      std   ci_low  ci_high
0  Throughput [B/s]    77.68     8.72    75.17    80.18
1        Delay [ms]  2391.98  1493.67  1962.95  2821.01
🧪 run7: payload=1B → img/run7/1B

📊 Stats for 1B:
             metric    mean     std  ci_low  ci_high
0  Throughput [B/s]    2.72    0.46    2.59     2.85
1        Delay [ms]  375.59  262.41  301.02   450.17
✅ Finished run7, saved in img/run7/
