Rails.application.routes.draw do
  get '/', to: 'weather_info#index'
  get '*path', controller: 'application', action: 'render_404'
end
