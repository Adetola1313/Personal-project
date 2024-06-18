SELECT r.dateTime, s.location, MAX(r.NOx) AS MaxNOx
FROM reading r
JOIN station s ON r.stationID = s.stationID
WHERE YEAR(r.dateTime) = 2022
GROUP BY r.dateTime, s.location
ORDER BY MaxNox DESC
LIMIT 1
