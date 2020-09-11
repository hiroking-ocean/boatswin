module WeatherInfoHelper
      
  def add_class(index, if_active="active", if_false="")
    if index == 0
      return if_active
    else 
      return if_false
    end
  end

  def true_or_false(index)
    if index == 0
      return "true"
    else
      return "false"
    end
  end

  class ImageID
    # 属性値
    attr_reader :chart, :wind, :wave, :sorted

    def initialize()
      @rootdir = "app/assets/images/"
      @chartdir = "charts/"
      @winddir = "winds/" 
      @wavedir = "waves/"

      @chart = file_name_array(@rootdir, @chartdir)
      @wind = file_name_array(@rootdir, @winddir)
      @wave = file_name_array(@rootdir, @wavedir)
      @sorted = sort(@chart, @wind, @wave)
    end

    def parse(times)
      parsed = []
      times.each do |time|
        parse = DateTime.parse(time + "+0900")
        parsed.push(parse)
      end
      return parsed
    end

    
    def file_name_format(day = '%m月%d日', hour = '%H時')
      days = []
      hours = []
      index = []
      temp1 = []
      temp2 = []
      @sorted.each_with_index do |value, i|
        dt = DateTime.parse(value + "+0900")
        days.push(dt.strftime(day))
        if (days[(i - 1)] != days[i])
          index.push(temp2)
          hours.push(temp1)
          temp1 = []
          temp2 = []
        end
        temp1.push(dt.strftime(hour))
        temp2.push(value)
        if (@sorted[i + 1].nil?)
          hours.push(temp1)
          index.push(temp2)
        end
      end
      days.uniq!
      return { "day":days, "hour":hours, "index":index}
    end

    private
    
      def file_name_array(root, directry)
        array = []
        filenames = Dir::entries(root + directry)
        filenames.each do |name|
          if (name != ".") and (name != "..")
            array.push(File.basename(name, ".jpg"))
          end
        end
        return array.sort!
      end

      def with_extention(root, directry)
        withex = []
        array = file_name_array( root, directry)
        array.each do |item|
          withex.push(directry + item + ".jpg")
        end
        return withex
      end

      def sort(charts, winds, waves)
        sorted = []
        sorted.push(charts)
        sorted.push(winds)
        sorted.push(waves)
        sorted.flatten!
        sorted.uniq!
        sorted.sort!
        return sorted
      end


    # まず、すべてのファイルのナンバーを併せて整列させる
  end
end
