require "./config.rb"

def convert_to_csv(file_path)
  @filename, dot, ext = File.basename(file_path).rpartition(".")
  raise "Expected file extension 'txt' but saw '#{ext}' instead" unless ext == "txt"

  @original_file_path = File.expand_path(INPUT_DIR) + "/#{@filename}.#{ext}"
  @new_file_path = File.expand_path(OUTPUT_DIR) + "/#{@filename}.csv"
  @contents = File.readlines(@original_file_path)

  report_header = @contents.slice(0, 3).map { |line| line = [line.chomp] }
  report_header << [@filename]
  delimited_rows = report_header + [[""]] + parse_contents

  write_csv(delimited_rows, @new_file_path) unless delimited_rows.empty?
end

def write_csv(rows_array, filename="new.csv")
  raise "'#{filename}'' exists" if File.exist? filename

  puts "Writing to '#{filename}'..."
  CSV.open("#{filename}", "ab") do |csv|
    rows_array.each { |row| csv << row }
  end
end

def parse_contents
  delimited_rows = [COLUMN_HEADERS]
  violations = get_violations

  violations.each do |v|
    record ||= get_facility_info
    record[COLUMN_ORDER[:report_id]] = @filename.strip
    record[COLUMN_ORDER[:violation]] = v
    delimited_rows << record
  end

  delimited_rows
end

def get_violations
  violations = []
  @contents.each do |line|
    violations << line if line.start_with? "#"
  end
  violations
end

def get_facility_info
  fac_info = []
  i = 0

  while fac_info.length < (COLUMN_HEADERS.length - 1) do
    candidate = @contents[i].match(/^\w+\s?\w*\:\s/i)

    if candidate
      header = format_as_header candidate
    end

    if COLUMN_ORDER.has_key? header
      fac_info[COLUMN_ORDER[header]] ||= @contents[i].sub(candidate.to_s, "").strip
    end

    i += 1
  end

  fac_info
end

def format_as_header(str)
  header = str.to_s.downcase
  header.gsub!(": ", "")
  header.gsub!(" ", "_")
  header.to_sym
end
