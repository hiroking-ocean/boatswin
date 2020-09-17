Rails.application.routes.draw do
  root 'weather_info#index'
  
  get '*path', controller: 'application', action: 'render_404'
end
