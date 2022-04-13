#!/usr/bin/env ruby
# frozen_string_literal: true

require 'em-websocket'

EM.run do
  @concurrent_client_count = 0
  
  EM::WebSocket.run(host: '0.0.0.0', port: 28_563) do |ws|
    ws.onopen do |handshake|
      @concurrent_client_count += 1
      puts "#{@concurrent_client_count} concurrent clients are connected"
    end

    ws.onclose { @concurrent_client_count -= 1 }

    ws.onmessage do |query|
      puts "Data received: #{query}"
      words = query.split(" ")
      answer = "#{(eval words[2]+words[1]+words[3]).to_s}\r\n"
      ws.send answer
      puts "Answer: #{answer}"
    end
  end
end
