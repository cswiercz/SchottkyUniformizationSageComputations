###############################################################################
# This file should hold all of the stuff to do the forward problem, i.e. from
# group data construct branch places and hence the algebraic curve.
#
# It requires: delta, q (group data)
###############################################################################
#import signal #For breaking up a function call if it is too slow
from sage.all import *
from plot_uniformization import *
from prime_function import build_prime_function, test_prime_function
from slitmap import *

# NOT WORKING Right now for some reason?
#def handler(signum, frame): #handler for signal
#	print "Calculation of the prime function taking too long. Consider \
#					lowering product_threshold or increasing max_time"
#	raise Exception("Exiting from build_prime_function")


def forward_problem(delta, q, prime_function_tests=False,
slitmap_tests=False, slitmap_full=False, plot_circles=False, plot_F=False, 
plot_branch_pts=False, product_threshold=12, max_time=200):
	# input:	
	# 	delta = list of centers of circles
	# 	q = list of radii of circles
	# 	max_time = max time for prime function computation before timeout
	# 	prime_function_tests = Check to see if the prime function passes some
	# 							tests
	# 	slitmap_tests = Check to see if the slitmap passes some tests
	# 	slitmap_full = Plot each component of the slitmap, for diagnostic
	# 					reasons
	# 	plot_circles = circle plot, unit circle and the Cj excised
	# 	plot_F = Plots the whole fundamental domain, F, with shading
	# 	plot_branch_pts = Plots the branch points with red xs
	# 	product_threshold = determines the max number of terms in the prime \
	# 							function product
	#
	# output:
	# 	none
	
	z = var('z') # complex variable
	gamma = var('gamma') #base point for 'abelmap' or prime function

	genus = len(q)

	# Plot some stuff about the region if we want.
	if plot_circles: circle_plots(delta,q) #returns plot
	if plot_F: F_plot(delta,q) #returns plot
	
	# Build the prime function, but make sure it doesn't take too long
#	signal.signal(signal.SIGALRM,handler)
#	signal.alarm(max_time) #Let it take max_time seconds at most!
#	try:
	omega = build_prime_function(delta, q, product_threshold)
#	except Exception, exc: #stop if it takes too long.
#		print exc

	# Build the slitmap
	slitmap = build_slitmap(omega)
	
	# Test the slit map
	if slitmap_tests: test_slitmap(slitmap)

	# Build the slitmap piece by piece for diagnostic purposes.
	if slitmap_full: build_slitmap_detailed(omega, delta, q)
	# this thing can output some stuff for use, but for now it just plots. 
	

	# Define the points of intersection of the Cj with the real axis. The image
	# of these points under the slitmap (5.19) are the branch points of the
	# curve.
	# For the hyperelliptic case this is easy, we know what the circles look
	# like so this is where they intersect. For the nonhyperelliptic case we
	# need to do something else maybe. For example, evaluate Cj(t=0)?
	pre_branch_pts = [ delta[j]-q[j] for j in xrange(genus) ]
	pre_branch_pts += [ delta[j]+q[j] for j in xrange(genus) ]

	# Branch points are the image of pre_branch_pts
	branch_pts = [slitmap(z = bp) for bp in pre_branch_pts]

	# Simple plot of branch points if interested. Shows location.
	if plot_branch_pts: plot_branch_pts(branch_pts)

	return None
