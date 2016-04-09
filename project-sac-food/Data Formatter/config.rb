require 'rubygems'
require 'bundler/setup'
require 'csv'

INPUT_DIR = "../PDF-to-Text/Processed/"
OUTPUT_DIR = "./Processed/"

# Get all inspection report files
ALL_TXT_REPORTS = Dir.entries(File.expand_path INPUT_DIR).select { |filename| filename.end_with? ".txt"}

COLUMN_HEADERS = [
"report_id",
"facility_name",
"permit_holder",
"address",
"city",
"zip_code",
"violation"
]

# record[COLUMN_ORDER[:column_name]] = datum
COLUMN_ORDER = COLUMN_HEADERS.map.with_index { |elem, i| [elem.to_sym, i] }.to_h
# output:
#   `{ :column_name1 => 1, :column_name2 => 2, ... }`



