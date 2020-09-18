require 'test_helper'

class WeatherInfoControllerTest < ActionDispatch::IntegrationTest
  def setup
    @base_title = "| BOATSWAIN"
  end
  test "should get root" do
    get root_path
    assert_response :success
    assert_select "title", "天気情報 #{@base_title}"
    assert_select "li.active" do
      assert_select "a", "天気"
    end
  end
end
