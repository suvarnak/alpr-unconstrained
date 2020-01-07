#!/bin/bash

check_file() 
{
	if [ ! -f "$1" ]
	then
		return 0
	else
		return 1
	fi
}

check_dir() 
{
	if [ ! -d "$1" ]
	then
		return 0
	else
		return 1
	fi
}


# Check if Darknet is compiled
check_file "darknet/libdarknet.so"
retval=$?
if [ $retval -eq 0 ]
then
	echo "Darknet is not compiled! Go to 'darknet' directory and 'make'!"
	exit 1
fi

lp_model="data/lp-detector/wpod-net_update1.h5"
input_dir='samples/videos/'
output_dir='output'
csv_file='output/video_results.csv'


# Check # of arguments
usage() {
	echo ""
	echo " Usage:"
	echo ""
	echo "   bash $0 -i input/dir -o output/dir -c csv_file.csv [-h] [-l path/to/model]:"
	echo ""
	echo "   -i   Input dir path (containing JPG or PNG images)"
	echo "   -o   Output dir path"
	echo "   -c   Output CSV file path"
	echo "   -l   Path to Keras LP detector model (default = $lp_model)"
	echo "   -h   Print this help information"
	echo ""
	exit 1
}

while getopts 'i:o:c:l:h' OPTION; do
	case $OPTION in
		i) input_dir=$OPTARG;;
		o) output_dir=$OPTARG;;
		c) csv_file=$OPTARG;;
		l) lp_model=$OPTARG;;
		h) usage;;
	esac
done

if [ -z "$input_dir"  ]; then echo "Input dir not set."; usage; exit 1; fi
if [ -z "$output_dir" ]; then echo "Ouput dir not set."; usage; exit 1; fi
if [ -z "$csv_file"   ]; then echo "CSV file not set." ; usage; exit 1; fi

# Check if input dir exists
check_dir $input_dir
retval=$?
if [ $retval -eq 0 ]
then
	echo "Input directory ($input_dir) does not exist"
	exit 1
fi

# Check if output dir exists, if not, create it
check_dir $output_dir
retval=$?
if [ $retval -eq 0 ]
then
	mkdir -p $output_dir
fi

# End if any error occur
set -e
# process video and store frames in input_dir
python process-vertical-video.py $input_dir output

# Detect vehicles
python vehicle-detection.py output/frames output/detection
# Detect license plates
python license-plate-detection.py output/detection $lp_model

# OCR
python license-plate-ocr.py output/detection

# Draw output and generate list
python gen-outputs.py output/frames output/detection > $csv_file

# write the video from output-dir and generate list
python gen-output-video.py output/detection output/videos


# Clean files and draw output
#rm $output_dir/*_lp.png
#rm $output_dir/*car.png
#rm $output_dir/*_cars.txt
#rm $output_dir/*_lp.txt
#rm $output_dir/*_str.txt