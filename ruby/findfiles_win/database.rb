
require "rubygems"
require "active_record"

#ActiveRecord::Base.logger() = Logger.new(STDERR)
#ActiveRecord::Base.colorize_logging = false

is_new_db = false
if File.exists?('files.db') then
	File.unlink('files.db')
	is_new_db = true
end

ActiveRecord::Base.establish_connection(
	:adapter => 'sqlite3',
	:database => 'files.db'
)

if is_new_db then
	ActiveRecord::Schema.define do
		create_table :items do |table|
			table.column :name, :string
			table.column :basename, :string
			table.column :size, :integer
		end
	end
end

class Item < ActiveRecord::Base
end
