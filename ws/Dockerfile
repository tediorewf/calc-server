FROM ruby:2.7

WORKDIR /usr/src/app

COPY Gemfile Gemfile.lock ./
RUN bundle install
COPY server_websockets.rb .

CMD ./server_websockets.rb
