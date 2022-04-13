#!/usr/bin/env ruby

require 'em-websocket'

EM.run do
  @concurrent_client_count = 0
  @shared_variables = {}

  EM::WebSocket.run(host: '0.0.0.0', port: 28_563) do |ws|
    ws.onopen do |_handshake|
      @concurrent_client_count += 1
      p "#{@concurrent_client_count} concurrent clients are connected"
    end

    ws.onclose { @concurrent_client_count -= 1 }

    ws.onmessage do |query|
      p "Data received: #{query}"
      words = query.split(' ')

      if words.length != 4
        ws.send write_err.concat('\r\n')
      else
        answer = write_answer(words[1], words[2], words[3]).concat('\r\n')
        ws.send answer
      end
    end
  end

  def write_answer(operation, operand1, operand2)
    answer = get_answer(operation, operand1, operand2)

    return write_err if answer.nil?

    p "Answer: #{answer}"
    "OK #{answer}"
  end

  def write_err
    p 'An error occurred.'
    'ERR'
  end

  def get_answer(operation, operand1, operand2)
    parsed_operand1 = parse_operand operand1
    parsed_operand2 = parse_operand operand2

    return nil if parsed_operand1.nil? && parsed_operand2.nil?

    answer = nil

    case operation
    when '+'
      answer = parsed_operand1 + parsed_operand2
    when '*'
      answer = parsed_operand1 * parsed_operand2
    when '-'
      answer = parsed_operand1 - parsed_operand2
    when '/'
      answer = parsed_operand1 / parsed_operand2
    when '='
      answer = @shared_variables[operand1] = parsed_operand2 if variable_name? operand1
    end

    answer
  end

  def parse_operand(operand)
    if variable_name? operand
      @shared_variables[operand]
    else
      begin
        Float(operand)
      rescue ArgumentError
        nil
      end
    end
  end

  def variable_name?(candidate)
    variable_name_regexp = /^[a-zA-Z_][a-zA-Z0-9_]*$/
    variable_name_regexp.match? candidate
  end
end
