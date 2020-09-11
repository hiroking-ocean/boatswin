class WeatherInfoController < ApplicationController
      include WeatherInfoHelper
    
      def index
        @names = ImageID.new()
        gon.sorted = @names.sorted
        gon.chart = @names.chart
        gon.wind = @names.wind
        gon.wave = @names.wave
        gon.formated = @names.file_name_format
      end
    
    
end
