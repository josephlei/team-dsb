require "./text_to_csv.rb"

TEST_SINGLE = ALL_TXT_REPORTS[0]
TEST_BATCH = [ALL_TXT_REPORTS[1], ALL_TXT_REPORTS[10], ALL_TXT_REPORTS[20]]

convert_to_csv TEST_SINGLE

TEST_BATCH.each do |report|
  convert_to_csv "#{INPUT_DIR}#{report}"
end
