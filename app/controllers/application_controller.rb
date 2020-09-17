class ApplicationController < ActionController::Base
    rescue_from ActiveRecord::RecordNotFound, with: :render_404
    rescue_from ActionController::RoutingError, with: :render_404
  
    def render_404
      render template: 'static_pages/error', status: 404, layout: 'application', content_type: 'text/html'
    end
  
    private
  
end
