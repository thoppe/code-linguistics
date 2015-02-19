# Helper script to make multiple calls to the linguist library
# this _greatly_ speeds up the computation time since the loading
# of the library is long.

require 'linguist/file_blob'
require 'linguist/language'

require 'json'

include Linguist

ARGV.each do |path|
  blob = Linguist::FileBlob.new(path, Dir.pwd)
  #blob.instance_variable_set(:@name, 'script')
  begin
    language = blob.language.name
  rescue
    language = ""
  end

  js = {
    :name => blob.name,
    :extension =>  blob.extension,
    :mime_type =>  blob.mime_type,
    :content_type =>  blob.content_type,
    :disposition  =>  blob.disposition,
    :size => blob.size,
    :sloc =>  blob.sloc,
    :loc  =>  blob.loc,
    :is_binary =>  blob.binary?,
    :is_text =>  blob.text?,
    :is_image =>  blob.image?,
    :is_generated =>  blob.generated?,
    :language => language.downcase
  }
  puts js.to_json()

end
