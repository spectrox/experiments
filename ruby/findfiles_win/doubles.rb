
require "Win32API"
require_relative "io"
require_relative "database"

io = IOHandler.new()
items = io.search()


items.each { |file, size| Item.create(:name => file, :basename => File.basename(file), :size => size) }

