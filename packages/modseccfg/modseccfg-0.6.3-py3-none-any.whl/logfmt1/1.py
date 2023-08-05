import re

line = open("/var/log/apache2/access.log", "r").readline()

rx = '(?P<remote_host>[\\w\\-.:]+) (?P<remote_logname>[\\w\\-.:]+) (?P<remote_user>[\\-\\w@.]+) \\[(?P<request_time>\\d[\\d:\\w\\s:./\\-+,;]+)\\] "(?P<request_line>(?P<request_method>\\w+) (?P<request_path>\\S+) (?P<request_protocol>[\\w/\\d.]+))" (?P<status>-|\\d\\d\\d) (?P<bytes_out>\\d+) "(?P<referer>[^"]*)" "(?P<user_agent>(?:[^"]+|\\\\")*)"'

print(re.match(rx, line))
