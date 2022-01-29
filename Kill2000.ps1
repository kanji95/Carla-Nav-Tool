$processPID =  $($(netstat -aon | findstr 2000)[0] -split '\s+')[-1]
taskkill /f /pid $processPID