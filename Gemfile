source "https://rubygems.org"

gem "github-pages", group: :jekyll_plugins
gem "wdm", "~> 0.1.0" if Gem.win_platform?
gem "webrick", "~> 1.8"

# Copied from https://github.com/jekyll/jekyll/blob/master/Gemfile
# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library
platforms :jruby, :mswin, :mingw, :x64_mingw do
  gem "tzinfo", "~> 1.2"
  gem "tzinfo-data"
end

# If you have any plugins, put them here!
group :jekyll_plugins do
  gem "jekyll-paginate"
  gem "jekyll-sitemap"
  gem "jekyll-gist"
  gem "jekyll-feed"
  gem "jemoji"
  gem "jekyll-include-cache"
  gem "jekyll-algolia"
end

