-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM crime_scene_reports;

--find out more info about crime scene (CASE ID = 295)
--Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
SELECT id, description FROM crime_scene_reports
WHERE year = '2021' AND month = '7' AND day = '28' AND street = 'Humphrey Street';

--Find more info through interviews
--| 161 | Ruth    | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
--| 162 | Eugene  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
--| 163 | Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- Key Infos: parking lot in that time. Withdrawing money on Leggett Street. Earliest flight tomorrow (July 29,2021), partner purchase plane ticket.

SELECT id, name, transcript FROM interviews
WHERE year = '2021' AND month = '7' AND day = '28';

--people info from bakery
SELECT id, activity, license_plate, hour, minute from bakery_security_logs
WHERE year = '2021' AND month = '7' AND day = '28' AND activity = 'entrance'
ORDER BY hour, minute;

--people info at the atm
SELECT id, account_number, transaction_type, amount FROM atm_transactions
WHERE year = '2021' AND month = '7' AND day = '28' AND atm_location = 'Leggett Street';

--people at the atm
SELECT p.name FROM atm_transactions AS a
JOIN bank_accounts AS b ON a.account_number = b.account_number
JOIN people AS p ON p.id = b.person_id
WHERE a.year = '2021' AND a.month = '7' AND a.day = '28' AND a.atm_location = 'Leggett Street'
AND a.transaction_type = 'withdraw';

--people at bakery within 10 minutes
SELECT p.name FROM bakery_security_logs as logs
JOIN people as p ON logs.license_plate = p.license_plate
WHERE logs.year = '2021' AND logs.month = '7' AND logs.day = '28' AND logs.hour = '10' AND logs.minute >= '15' AND logs.minute <= '25' AND logs.activity = 'exit'
ORDER BY p.name;

--people calling
SELECT p.name FROM phone_calls as c
JOIN people as p ON p.phone_number = c.caller
WHERE c.year = '2021' AND c.month = '7' AND c.day = '28' AND c.duration < 60;

--people leaving the airport
SELECT * FROM airports;

SELECT day, hour, minute, flights.id FROM flights
JOIN airports ON airports.id = flights.origin_airport_id
WHERE year = '2021' AND month = '7' AND day = '29' AND f.hour = '8' AND city = 'Fiftyville'
ORDER BY hour;

SELECT people.name FROM airports as a
JOIN flights as f ON f.origin_airport_id = a.id
JOIN passengers as p ON p.flight_id = f.id
JOIN people ON people.passport_number = p.passport_number
WHERE f.year = '2021' AND f.month = '7' AND f.day = '29';

--people at atm and the parking lot at time of stealing and calling
SELECT DISTINCT(p.name) FROM atm_transactions AS a
JOIN bank_accounts AS b ON a.account_number = b.account_number
JOIN people AS p ON p.id = b.person_id
JOIN bakery_security_logs as l ON l.license_plate = p.license_plate

WHERE a.year = '2021' AND a.month = '7' AND a.day = '28' AND a.atm_location = 'Leggett Street'

AND p.name IN
(SELECT p.name FROM bakery_security_logs as logs
JOIN people as p ON logs.license_plate = p.license_plate
WHERE logs.year = '2021' AND logs.month = '7' AND logs.day = '28' AND logs.hour = '10' AND logs.minute >= '15' AND logs.minute <= '25' AND logs.activity = 'exit'
ORDER BY p.name)

AND p.name IN
(SELECT p.name FROM phone_calls as c
JOIN people as p ON p.phone_number = c.caller
WHERE c.year = '2021' AND c.month = '7' AND c.day = '28' AND c.duration < 60)

AND p.name IN
(SELECT people.name FROM airports as a
JOIN flights as f ON f.origin_airport_id = a.id
JOIN passengers as p ON p.flight_id = f.id
JOIN people ON people.passport_number = p.passport_number
WHERE f.year = '2021' AND f.month = '7' AND f.day = '29' AND f.hour = '8');

-- city thief escaped to
SELECT airports.city FROM flights as f
JOIN airports ON airports.id = f.destination_airport_id
WHERE year = '2021' AND month = '7' AND day = '29' AND f.hour = '8'
AND origin_airport_id =
(SELECT airports.id FROM airports
JOIN flights ON origin_airport_id = airports.id
WHERE city = 'Fiftyville')
;

SELECT full_name FROM airports
WHERE id = 4;

--accomplice

SELECT name FROM people as p
JOIN phone_calls as c ON c.receiver = p.phone_number
WHERE c.year = '2021' AND c.month = '7' AND c.day = '28' AND c.duration < 60 AND c.caller = (SELECT phone_number FROM people WHERE name = 'Bruce')

