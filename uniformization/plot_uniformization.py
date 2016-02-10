###############################################################################
# Plotting associated with the Schottky uniformization is here. I.e. the region,
# calculated branch points, etc.
###############################################################################

from sage.all import *

# plot_circles plots ONLY the unit circle and the interior circle. No filling.
def circle_plots(delta, q, colors=[]):
    #
    # This module plots the circles from group data in the complex plane
    # input:
    #   delta = list of centers of circles
    #   q = radius of circles
    #   colors = list of len genus of RGBcolors for uniform plotting
    # 
    # output:
    #   D_zeta = plot data. To show this plot it is recommended to use 
    #       D_zeta.show(axes=True, title='$D_{\zeta}$', aspect_ratio=1)
    #
    
    # Define our parametric plotting variable
    t = var('t')
    assume(t,'real')
    genus = len(q)
    
    # Define the C0, Cj
    C0 = exp(I*t)
    Cj = lambda j: delta[j] + q[j]*exp(I*t)
    
    # Colors for plotting, if not already passed.
    if len(colors)==0:
        colors = [(0.6*random(),random(),random()) for k in range(genus)]
         #For plotting, multiply the first one by 0.6 so nothing is TOO red
    
    # Plot the circles, identifying edges with like colors.
    ## First plot C_0
    D_zeta = line( [CC(C0(t=v)) for v in srange(0,2*pi+0.2,0.1)], linestyle='--',
    rgbcolor=(1,0,0), thickness=3, legend_label='C_0' )
    ## Plot the C_j
    #D_zeta += sum( [line( [CC(Cj(j)(t=v)) for v in srange(0,2*pi+0.2,0.1)],
    #rgbcolor=colors[j], thickness=3, legend_label='C_'+str(j+1) ) for j in
    #range(genus)] )
    D_zeta += sum( [line( [CC(Cj(j)(t=v)) for v in srange(0,2*pi+0.2,0.1)],
    rgbcolor=colors[j], thickness=3, legend_label='C_'+str(j+1) ) for j in
    range(genus)] )

    return D_zeta
	

def F_plot(delta, q, colors=[]):
    #
    # This module  plots the fundamential region, F, including filling and Cjp
    #
    # input:
    #   delta = list of centers of circles
    #   q = radius of circles
    #   colors = list of len genus of RGBcolors for uniform plotting
    #
    # output:
    #   D_zeta = plot data

    # Define our parametric plotting variable
    t = var('t')
    assume(t,'real')
    genus = len(q)
    x,y = var('x,y', domain='real')
    zeta = x+I*y # For the fill plot.

    # Define the C0, Cj, Cjp
    C0 = exp(I*t)
    Cj = [ delta[j] + q[j]*exp(I*t) for j in range(genus) ]
    Cjp = [ 1/circle.conjugate() for circle in Cj ]
    
    # Define circles for filling regions D_zeta and D_zeta'
    C0_fill = norm(zeta)-1 # norm(zeta) = x^2+y^2, sage syntax
    Cj_fill = [ norm(zeta-delta[j]) - q[j]**2 for j in range(genus) ]
                                        # norm(z) = x^2+y^2, a sage syntax
    Cjp_fill = [ norm(1/zeta.conjugate()-delta[j]) - q[j]**2 for j in
                range(genus) ] # norm(z) = x^2+y^2, a sage syntax
    
    # Colors for plotting, if colors not already passed.
    if len(colors)==0:
        colors = [(0.6*random(),random(),random()) for k in range(genus)]
         #For plotting, multiply the first one by 0.6 so nothing is TOO red

	
    
    # Get the right viewing window. Calculate the maximum on the real axis
    xplot_range = [max( [ abs(circle.substitute(t=0)) for circle in Cjp ] )]
    xplot_range += [max( [ abs(circle.substitute(t=pi)) for circle in Cjp ]
        )]
    xplot_range = max( xplot_range+[1] ) # Add 1 to make sure we at least
                                         # get the unit circle
    yplot_range = [max( [ norm(CDF(circle.substitute(t=pi/2))) for circle in
        Cjp ] )]
    yplot_range += [max( [ norm(CDF(circle.substitute(t=-pi/2))) for circle
        in Cjp ] )]
    yplot_range = max( yplot_range+[1] ) # Add 1 to make sure we at least get
                                        # the unit circle
    
    # Plot the circles, identifying edges with like colors.
    ## First plot C_0
    D_zeta = line( [CC(C0(t=v)) for v in srange(0,2*pi+0.2,0.1)], linestyle='--',
        rgbcolor=(1,0,0), thickness=3, legend_label='C_0' )
    ## Plot the C_j
    D_zeta += sum( [line( [CC(Cj[j](t=v)) for v in srange(0,2*pi+0.2,0.1)],
        rgbcolor=colors[j], thickness=3, legend_label='C_'+str(j+1) )
            for j in range(genus)] )
    ## Plot the C_j'
    D_zeta += sum( [line( [CC(Cjp[j](t=v)) for v in srange(0,2*pi+0.2,0.1)],
        rgbcolor=colors[j], thickness=3 ) for j in range(genus)] )
    ## Fill the two regions, D_\zeta and D_zeta'
    D_zeta += region_plot( [real_part(C0_fill)<0]+[real_part(Cj_fill[k])>0
            for k in range(0,genus)], (x,-xplot_range,xplot_range),
            (y,-yplot_range,yplot_range), incol='red', borderwidth=0, alpha=0.2
            )
    D_zeta += region_plot([real_part(C0_fill)>0]+[real_part(Cjp_fill[k])>0
            for k in range(0,genus)], (x,-xplot_range,xplot_range),
            (y,-yplot_range,yplot_range), incol='blue', borderwidth=0, alpha=0.2
            )
	
    return D_zeta

def branch_point_plot(b_pts):
    #
    # This module plots the branch points on the line
    #
    # input:
    #	b_pts = branch points
    #
    # output:
    # 	branch_plot = plot data. Use  branch_plot.show(axes = True,
    # 	title='Branch Points') to plot for example

    
    branch_plot = sum( [point( CC(bp), marker='x', size=50,
            rgbcolor='red' ) for bp in b_pts] )
    return branch_plot

def circles_and_points_plot(
        delta, q, points, circle_colors=[], colors=[]
        ):
    #
    # This module plots circles and test points in the domain together.
    #
    # input:
    #   delta = list of centers of circles
    #   q = radius of circles
    #   points = test points in the domain
    #   circle_colors = RGBcolors for plotting the circles. This is passed in
    #   to uniformize across various plots
    #   colors = RGBcolors for plotting the lines and points. This is passed
    #   in to uniformize across various plots
    # 
    # output:
    #   D_zeta = plot data
    #

    if len(colors)==0:
        colors = [ (random(), random(), random()) for k in xrange(len(points)) ]
    if len(circle_colors)==0:
        circle_colors = [ (random(), random(), random()) for k in xrange(len(points)) ]

    D_zeta = circle_plots(delta, q, colors=circle_colors)
    D_zeta += sum( [ point( p, marker='x', size=50, rgbcolor=colors[itnum] ) for
        itnum, p in enumerate(points) ] )

    return D_zeta
