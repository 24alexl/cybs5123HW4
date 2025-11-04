CYBS 5123 - Graduate Analysis Report

API-Based Time Sync vs. Traditional NTP (UDP)

This report compares the API-based time synchronization solution (implemented for this assignment) with the standard time synchronization service (NTP over UDP) based on three metrics: Latency, Accuracy, and Resource Usage.

1. Comparison: Latency, Accuracy, and Resource Usage

Latency

API (HTTPS): High Latency. This approach is significantly slower. It requires a full TCP handshake (SYN, SYN-ACK, ACK), followed by a complete TLS (SSL) handshake for encryption (multiple round-trips), and finally the HTTP GET request and response. The entire process can take several hundred milliseconds to seconds, depending on network conditions.

NTP (UDP): Very Low Latency. NTP runs over UDP, a connectionless protocol. It sends a small packet and gets a small packet back. The protocol itself is designed for this high-frequency, low-overhead exchange. It doesn't have the overhead of TCP connections or TLS encryption, making it orders of magnitude faster per-request.

Accuracy

API (HTTPS): Low Accuracy. The time received from the API (e.g., the unixtime) is the time on the server when it processed the request. It does not account for the network latency (both ways) of the API call. By the time the script receives the time, it could be a second or more out of date. Furthermore, our script performs a "clock set," which is a hard, abrupt jump. This can be disruptive to system services that rely on monotonic (steadily increasing) time.

NTP (UDP): Extremely High Accuracy. NTP is not just a "time-fetcher"; it's a sophisticated protocol. The NTP daemon (ntpd or chronyd) constantly communicates with multiple time servers. It uses complex algorithms to factor out network jitter and round-trip delays, allowing it to calculate the actual time with millisecond (or better) precision. It also "steers" or "slews" the clock—gradually speeding it up or slowing it down to correct drift—which avoids the disruptive "jumps" of a hard set.

Resource Usage

API (HTTPS): High Resource Usage (in bursts). To run our script every 30 minutes via cron, the system must:

Start a cron process.

Launch a new shell.

Spin up the entire Python interpreter.

Load all imported modules (requests, datetime, etc.).

Perform a CPU and memory-intensive TLS encryption/decryption.
This is a "heavy" operation that causes a significant spike in CPU, memory, and I/O for a short period.

NTP (UDP): Very Low Resource Usage. An NTP daemon is a single, small, highly-efficient service that runs in the background. It uses minimal CPU and has a very small, stable memory footprint. Its network traffic consists of a few tiny UDP packets every few minutes. It is vastly more efficient for continuous timekeeping.

2. Opinion: Lightweight API-Based Approach

The lightweight, API-based approach is a "firewall-friendly workaround," not a true replacement for NTP.

Its primary and most significant advantage is its ability to function in highly-restricted network environments like the one described in the assignment. The lab's firewall blocks UDP, but it must allow HTTPS (port 443) for web browsing. This solution cleverly tunnels its "time" request over a protocol that is guaranteed to be open. It uses standard, ubiquitous technologies (HTTPS, JSON) that are simple to implement in any modern language, making it accessible and easy to debug.

However, its disadvantages are all the points listed in the comparison. It is less accurate, higher latency, and far less efficient than NTP. It's a "brute-force" solution (setting the clock) versus NTP's "elegant" one (steering the clock).

Conclusion: In a production environment where accuracy and stability are paramount, one would never choose this API method over NTP. However, in the specific, constrained environment of the OUPI lab, this approach is an excellent and practical solution. It perfectly solves the problem given the constraints, prioritizing "working" over "perfect." It's a great example of creative problem-solving in a locked-down IT environment.