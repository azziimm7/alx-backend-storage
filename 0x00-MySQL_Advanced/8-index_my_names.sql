-- Create an index for the first letter only
CREATE INDEX idx_name_first ON names (name(1));
