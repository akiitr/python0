#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from numpy import histogram,percentile,array
import argparse
from math import floor

# Constants
CHARS={'full_top':'┃', 'half_top':'╻', 'fill':'┃'}

def draw_hist(normed_hist_list,shape,args):
    """ takes a list of histogram bin counts and shape(min,max) of input """
    
    # TODO make the offset configurable
    y_offset = '       '
    y_label  = ' prop. '

    print ("")
    # Build plot from top level
    for depth in range(args.height-1,-1,-1):

        # Draw Y axis
        if depth == args.height/2:
            sys.stdout.write(y_label+'│')
        else:
            sys.stdout.write(y_offset+'│')

        # Draw bars
        for item in normed_hist_list:
            floored_item = floor(item)
            if floored_item >= depth:
                if floored_item == depth and item % 1 < 0.75 and item%1 >0.25:
                    sys.stdout.write( CHARS['half_top'] )
                elif floored_item == depth and item % 1 > 0.75 :
                    sys.stdout.write( CHARS['full_top'] )
                elif floored_item > depth:
                    sys.stdout.write( CHARS['fill'] )
                else:
                    sys.stdout.write(' ')
                continue
            else:
                sys.stdout.write(' ')
        print ("")

    # Draw X axis 
    print (y_offset + '└'+ "─"*(args.bins+2))
    print (y_offset + str(shape[0]) + ' '*(args.bins-3) + str(shape[1]))


def parse_args():
    parser = argparse.ArgumentParser(description='draw a histogram from stdin', add_help=False)
    parser.add_argument('-b', '--bins', type=int, help='the number of bins (default=60)', default=60)
    parser.add_argument('-h', '--height', type=int, help='the height of the plot (default=10)', default=10)
    parser.add_argument('-w', '--width', type=int, help='the width of the bins (default=0)', default=0)
    parser.add_argument('-rmin', '--range_min', type=int, help='the min range of the series (default=0)', default=0)
    parser.add_argument('-rmax', '--range_max', type=int, help='the max range of the series (default=0)', default=0)
    parser.add_argument('-?', '--help', action='help', help='show this help and exit')
    return parser.parse_args(sys.argv[1:])


def main():

    args = parse_args()
    input_data = sys.stdin.read().strip('\n')
    input_list = input_data.split('\n')
    
    temp = []
    
    # Convert input to floats
    try:
	# map returns an iterable in pyhton3 to be converted to list to work other than print statement
        input_list = list(map(float,input_list))
    except:
      #raise SystemError("Failed to convert input to float")
    
      # AK: a way to remove the text from column but slow
      for i in input_list:
        try:
          temp.append(float(i))
        except:
          continue
      input_list = temp
	# AK: Done

# AK: clipping the list based on given range
    if (args.range_max == 0):
	    input_max = max(input_list)
    else:
	    input_max = args.range_max

    if (args.range_min == 0):
	    input_min = min(input_list)
    else:
	    input_min = args.range_min

# AK: list comprehensiong for clipping the list
    input_list = [i for i in input_list if (i <= input_max) and (i >= input_min)]

    if (args.width > 0):
	    hist_list,bin_edges = histogram(input_list,bins=range(int(min(input_list)), int(max(input_list)) + args.width, args.width))
    else:
	    hist_list,bin_edges = histogram(input_list,bins=args.bins)

    max_count = max(hist_list)
    shape = ( min(input_list), max(input_list) )
    normed_hist_list = [ float(x)*args.height/max_count for x in hist_list ]
    
    # Draw the histogram
    draw_hist(normed_hist_list,shape,args)
    # Printing histogram
    #print ("Vlaue from: {0} to: {1}\n".format(min(input_list),max(input_list)))
    print ("Bins		Count		ASCII_plot\n")
    for (x,n) in zip(range(len(bin_edges)),hist_list):
	    bar = '#'*int(n*50.0/max_count)
	    x1 = '{0: <7.5g}'.format(bin_edges[x]).ljust(5)
	    x2 = '{0: <7.5g}'.format(bin_edges[x+1]).ljust(5)
	    count = 'count: {0: <7.10g}'.format(int(n)).ljust(5)
	    print ("{0} - {1} {2}| {3}".format(x1,x2,count,bar))
    # Calculate stats on data
    print ('\nSamples	:',len(input_list))
    print ('Mean	:',array(input_list).mean())
    print ('Var	:',array(input_list).var())
    print ('Std_dev	:',array(input_list).std())

    for perc in [25,50,75]:
        print ("{0}th perc. :".format(perc), percentile(input_list,perc))
    

if __name__ == '__main__':
    main()
