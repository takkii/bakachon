# frozen_string_literal: true

require 'fileutils'
require 'open3'
require 'readline'

# Create runner.
class CleanRunner
  def self.delete
    puts ''
    puts 'Enter yes/no to delete, tab completion is available.'
    puts ''

    sel = %w[yes no].map!(&:freeze).freeze

    Readline.completion_proc = proc {|word|
      sel.grep(/\A#{Regexp.quote word}/)
    }

    gold_exist = 'bakachon_log'.to_s

    while (line = Readline.readline(""))
      line.chomp!

      if line.match?(sel[0])
        FileUtils.rm_rf(File.expand_path("~/#{gold_exist}"))
        puts ''
        puts 'Deleted, the existing bakachon log folder.'
        puts ''
        break
      elsif line.match?(sel[1])
        puts ''
        puts 'You selected No, No action will be taken.'
        puts ''
        break
      else
        puts ''
        puts 'Please enter yes or no as an argument.'
        puts ''
        break
      end
    end
  end

  def self.run
    gold_exist = 'bakachon_log'.to_s

    if Dir.exist?(File.expand_path("~/#{gold_exist}"))
      puts ''
      puts 'Already have a bakachon log folder.'
      delete
    else
      FileUtils.mkdir("#{gold_exist}")
      FileUtils.mv("#{File.dirname(__FILE__)}/#{gold_exist}", File.expand_path('~/'))
      puts ''
      puts 'Created, bakachon log folder.'
      puts ''
    end
  end
end

begin
  CleanRunner.run
rescue StandardError => e
  puts e.backtrace
ensure
  GC.compact
end

__END__
