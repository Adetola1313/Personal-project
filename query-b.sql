SELECT 
  s.location, 
  AVG(r.PM2_5) AS Avg_PM2_5, 
  AVG(r.VPM2_5) AS Avg_VPM2_5 
FROM 
  reading r
  JOIN station s ON r.stationId = s.stationId 
WHERE 
  YEAR(r.DateTime) = 2019
  AND HOUR(r.DateTime) = 8 
GROUP BY 
  r.StationID