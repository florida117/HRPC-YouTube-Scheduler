#!/bin/bash

# Get current year
year=$(date +%Y)

# Get Easter Sunday from ncal - using sed to clean up the output
easter_info=$(ncal -e $year | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

# Split the date components
easter_day=$(echo $easter_info | cut -d' ' -f1)
easter_month_name=$(echo $easter_info | cut -d' ' -f2 | tr '[:upper:]' '[:lower:]')

# Convert month name to number (using tr for case conversion instead of ,,)
case "$easter_month_name" in
    "january")   month_num="01" ;;
    "february")  month_num="02" ;;
    "march")     month_num="03" ;;
    "april")     month_num="04" ;;
    "may")       month_num="05" ;;
    "june")      month_num="06" ;;
    "july")      month_num="07" ;;
    "august")    month_num="08" ;;
    "september") month_num="09" ;;
    "october")   month_num="10" ;;
    "november")  month_num="11" ;;
    "december")  month_num="12" ;;
esac

# Pad the day with leading zero if needed
easter_day=$(printf "%02d" $easter_day)

# Create Easter date string with numeric month
easter_date="${year}-${month_num}-${easter_day}"

# Calculate Good Friday (2 days before Easter)
good_friday=$(date -v-2d -j -f "%Y-%m-%d" "$easter_date" "+%Y-%m-%d")

# Extract month and day for crontab
gf_month=$(date -j -f "%Y-%m-%d" "$good_friday" "+%-m")
gf_day=$(date -j -f "%Y-%m-%d" "$good_friday" "+%-d")

# Extract month and day for crontab
# gf_month=$(date -j -f "%Y-%m-%d" "$good_friday" "+%-m")
# gf_day=$(date -j -f "%Y-%m-%d" "$good_friday" "+%-d")

# # Create temporary file with existing crontab
# crontab -l > temp_crontab 2>/dev/null || touch temp_crontab

# # Add new cron job for Good Friday
# echo "0 0 $gf_day $gf_month * /path/to/your/script.sh" >> temp_crontab

# # Install new crontab
# crontab temp_crontab

# # Clean up
# rm temp_crontab

echo "Crontab updated. Your script will run on Good Friday ($good_friday)"