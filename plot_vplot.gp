# Draws the V-plot from vplot_wide.txt and saves it as vplot.png
set terminal pngcairo size 1000,800
set output "vplot.png"

set title "V-plot"
set xlabel "Offset from site centre (bp)"
set ylabel "Fragment length (bp)"
set xrange [-500:499]
set yrange [50:400]

# Skip column 0 (the length), then turn column number -> offset and row number -> length
plot "vplot_wide.txt" matrix every ::1 using ($1-501):($2+50):3 with image notitle
