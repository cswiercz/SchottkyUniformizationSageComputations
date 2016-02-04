###############################################################################
# Plots the fundamential region, F.
# 
# Requires: t, delta, q, genus defined before called
###############################################################################

# Define the C0, Cj, Cjp
C0 = exp(I*t)
Cj = lambda j: delta[j] + q[j]*exp(I*t)
Cjp = lambda j: 1/(Cj(j).conjugate())

# Define circles for filling regions D_zeta and D_zeta'
C0_fill = abs(zeta)^2-1
Cj_fill = lambda j: abs(zeta-delta[j])^2 - q[j]^2
Cjp_fill = lambda j: abs(1/zeta.conjugate()-delta[j])^2 - q[j]^2

# Colors for plotting
colors = [(0.6*random(),random(),random()) for k in range(genus)] #For plotting,
                          #multiply the first one by 0.6 so nothing is TOO red

# Find a better way to do this. 
#xplot_range = 4.5 #to plot for x \in [-xplot_range,xplot_range]
#yplot_range = 2 #to plot for y \in [-yplot_range,yplot_range]


# Plot the circles, identifying edges with like colors.
## First plot C_0
D_zeta = line( [CC(C0(t=v)) for v in srange(0,2*pi+0.2,0.1)], linestyle='--',
rgbcolor=(1,0,0), thickness=3, legend_label='C_0' )
## Plot the C_j
D_zeta += sum( [line( [CC(Cj(j)(t=v)) for v in srange(0,2*pi+0.2,0.1)],
rgbcolor=colors[j], thickness=3, legend_label='C_'+str(j+1) ) for j in
range(genus)] )
## Plot the C_j'
D_zeta += sum( [line( [CC(Cjp(j)(t=v)) for v in srange(0,2*pi+0.2,0.1)],
rgbcolor=colors[j], thickness=3 ) for j in range(genus)] )
## Fill the two regions, D_\zeta and D_zeta'
D_zeta += region_plot( [real_part(C0_fill)<0]+[real_part(Cj_fill(k))>0 for k in
range(0,genus)], (x,-xplot_range,xplot_range), (y,-yplot_range,yplot_range),
incol='red', borderwidth=0, alpha=0.2 )
D_zeta += region_plot([real_part(C0_fill)>0]+[real_part(Cjp_fill(k))>0 for k in
range(0,genus)], (x,-xplot_range,xplot_range), (y,-yplot_range,yplot_range),
incol='blue', borderwidth=0, alpha=0.2 )
## Show the graphic
D_zeta.show(axes = True, title='D_zeta')
