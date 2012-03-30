
require "Win32API"

class IOHandler
	def search()
		items = {}
		for drive in self.get_drives do
			items.merge!(self.read_directory(drive[0..1]))
		end
		return items
	end
	def get_drives()
		getLogicalDriveStrings = Win32API.new('kernel32',
						      'GetLogicalDriveStrings',
						      ['L', 'P'], 'L')
		buf = "\0" * 1024
		len = getLogicalDriveStrings.call(buf.length, buf)
		return buf[0..len].split("\0")
	end
	def read_directory(dir='')
		if not File.directory?(dir)
			return nil
		end
		items = {}
		#puts dir + "\n"
		begin
			for item in Dir.entries(dir) do
				if item == '.' or item == '..'
					next
				end
				file = dir + '\\' + item
				if File.directory?(file)
					subdir = self.read_directory(file)
					if subdir.length > 0 then
						items = items.merge(subdir)
					end
				else
					items[file] = File.size(file)
				end
			end
		rescue SystemCallError => msg
			puts "Error: " + msg.to_s + "\n"
		end
		return items
	end
end

