# Description

Script that allows to parse Blackboard Learn logs in bulk and isolate stack traces based on a search string passed to the script. The current supported logs along with the current support of each are described below:

| Type of Log     | Fully supported | Type of output                  |
| --------------- | --------------- | ------------------------------- |
| bb-access-log   | Full support    | Single line                     |
| bb-email-log    | Full support    | Single line                     |
| bb-services-log | Full support    | Multiline with full stack trace |
| bb-sqlerror-log | Partial support | Single line of match            |
| stdout-stderr   | Partial support | Single line of match            |

For the logs with partial support, given the nature of how those logs are written, there's no defined way to capture the entire stack trace from the file directly. The search will show what server has the hit and the line number for easy identification

# Requirements

The script requires Python3 to be installed (no additional packages are needed since the libraries used are included by default with Python), please make sure it's available before running the script, It also requires the logs to be already converted either by manually downloading them from the system through the UI and running the conversion script (available in the same download screen) or downloading directly from the S3 bucket which converts them directly (available for Learn Support only)

## Git and GitHub

If you're not using git on your system, we strongly recommend installing it and setting it up by following this guide: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

This will allow you to download the script and any subsequent updates easily. Once git is installed you can download this tool by running the following command on the folder where you want to save it:

```shell
git clone https://github.com/OneComputerGuy/logfinder.git
```

To retrieve/update the script with any available update, you only need to navigate on your command prompt window to the folder where the script is saved and running:

```shell
git pull
```

This will take care of the rest.

## For Windows users:

Make sure you can execute python3 directly from the command line by just running `python3 --version`, if you receive an error indicating that the command is not recognized, please follow these steps to add python to the environment variables of your system (remember to reboot your system after the change): https://www.educative.io/answers/how-to-add-python-to-path-variable-in-windows

If after this step CMD is still not recognizing the command, execute the script specifying the entire path where your Python installation is. To determine the location, follow these steps:

1. on your keyboard press Windows Key + R
2. On the "Run" window that opens up, type "%appdata%" without quotes
3. On the file explorer window that opens, go up a folder by clicking "AppData" in the address bar at the top
4. After navigating to the AppData folder, go to Local > Programs > Python > <current installed version> and locate the python executable
5. Once there, click the address bar at the top of the file explorer and copy the path

Once you have this path, you can use it to replace python3 when needed, e.g: To check the version of python installed with this approach you need to paste into the command prompt window this:

```shell
C:\> C:\Users\<yourUser>\AppData\Local\Programs\Python\<versionInstalled>\python --version
```

## For Ubuntu/Linux/WSL systems

Python should be installed by default with your installation, if not, you can install it using the following command:

```shell
sudo apt install python3
```

## For MacOS users:

Python usually comes installed by default, if it's not available/installed, there are two options for this. The first one is to manually download and install Python from the original site, the second option is to use Homebrew to install it (Homebrew is the unofficial package manager for MacOS).

To install Homebrew, follow the steps outlined in their site https://brew.sh/ and then, execute `brew install python`

# Usage:

The script will automatically walk through the folder you specify and get the logs from there without the need of manually specifying the logs available in that folder

The parameters the script receives are the following:

- `-i or --input`: **Required** - Path to the folder where the logs are physically stored. E.g: /Users/myUser/Desktop/logs (Must be a valid path or string representing a path)
- `-o or --output`: **Optional** - Path where the search will be stored, if the parameter is not passed, the results will be printed in the console. E.g: /Users/myUser/Desktop/logs (Must be a valid path or string representing a path)
- `-t or --type`: **Required** - Type of log that will be searched, valid options are:
  - access: Referring to the `tomcat/bb-access-log`
  - email: Referring to the `bb-email-log`
  - services: Referring to the `bb-services-log`
  - sql: Referring to the `bb-sqlerror-log`
  - standard: Referring to the `tomcat/stdout-stderr-log`
- `-s or --search`: **Required** - Search parameter or string that will be matched on all the selected logs

# Examples

**_Input command:_**

```shell
 python3 parser.py -i /Users/myUser/Desktop/logs -o /Users/Users/Desktop/ -t access -s '_177631_1'
```

**_Expected output:_**

File on the location `/Users/myUser/Desktop/` with the name `access-(current-timestamp)` with the matches of the search. The format is the following:

> File name: `access-01-09-23--14-53-32.txt`

```log
Search query: _177631_1
--------------------------------


--------------------------------
From server ip-100-100-100-100:
--------------------------------
<Line Number>: 67.234.4.149 127.0.0.1 connector-27 _3753132_1 [21/Aug/2023:21:50:12 -0500] "GET /avatar/user/_223146_1?ts=1692672611116 HTTP/1.1" 200 3241 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203" "_fbp=fb.1.1683819653682.1659006520; hubspotutk=94bfd836a4561f05a333a78386ab6d5a; lo-uid=f918fb12-1685969302299-ccc207be1360748b; _cbp=fb.1.1686690577309.2003507668; lo-visits=18; __hstc=243369562.94bfd836a4561f05a333a78386ab6d5a.1683819656199.1687478319264.1687481705396.17; _ga_4TFS1G3RTR=GS1.1.1687481702.17.1.1687481707.55.0.0; _uetvid=e656b950b9d411ec9ab8e1f2b7245873; _uetmsclkid=_uet53c9254501bc1270eb0241180dc609da; apt.uid=AP-PQQY5YJEHTTA-2-1688168881620-77228397.0.2.4cdfb9c6-5692-459e-92f3-9cb1989a9a7b; _ga=GA1.2.825527473.1683819653; BbClientCalenderTimeZone=America/New_York; AWSELB=F18985F10C2FA0DFE483D95F0C559502B0537A1060782149391442C075437D22E1648AF612D119B3218E563385DEFC3685084F3545FD74B8B885C5C255237756FB09E56C1F; AWSELBCORS=F18985F10C2FA0DFE483D95F0C559502B0537A1060782149391442C075437D22E1648AF612D119B3218E563385DEFC3685084F3545FD74B8B885C5C255237756FB09E56C1F; apt.sid=AP-PQQY5YJEHTTA-2-1692672265640-43411642; BbRouter=expires:1692683412,id:0AC52C4F2F5C9E003FD496516847D2E2,sessionId:455859280,signature:d7ae830cf443b3e725e64df68750b6a3f3f5cde9f74c1f921d2ebc00db4b8a18,site:6e33b195-e019-4185-bf59-a60544575195,timeout:10800,user:b8d10f4c9a234e28bb41b43b4b15dcc9,v:2,xsrf:08ab7dcd-1cc6-4ee6-afa2-ac4a5d2454b3" 2 3241

--------------------------------
From server ip-200-120-102-155:
--------------------------------
<Line Number>: 67.234.4.149 127.0.0.1 connector-27 _3753132_1 [21/Aug/2023:21:50:12 -0500] "GET /avatar/user/_223146_1?ts=1692672611116 HTTP/1.1" 200 3241 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203" "_fbp=fb.1.1683819653682.1659006520; hubspotutk=94bfd836a4561f05a333a78386ab6d5a; lo-uid=f918fb12-1685969302299-ccc207be1360748b; _cbp=fb.1.1686690577309.2003507668; lo-visits=18; __hstc=243369562.94bfd836a4561f05a333a78386ab6d5a.1683819656199.1687478319264.1687481705396.17; _ga_4TFS1G3RTR=GS1.1.1687481702.17.1.1687481707.55.0.0; _uetvid=e656b950b9d411ec9ab8e1f2b7245873; _uetmsclkid=_uet53c9254501bc1270eb0241180dc609da; apt.uid=AP-PQQY5YJEHTTA-2-1688168881620-77228397.0.2.4cdfb9c6-5692-459e-92f3-9cb1989a9a7b; _ga=GA1.2.825527473.1683819653; BbClientCalenderTimeZone=America/New_York; AWSELB=F18985F10C2FA0DFE483D95F0C559502B0537A1060782149391442C075437D22E1648AF612D119B3218E563385DEFC3685084F3545FD74B8B885C5C255237756FB09E56C1F; AWSELBCORS=F18985F10C2FA0DFE483D95F0C559502B0537A1060782149391442C075437D22E1648AF612D119B3218E563385DEFC3685084F3545FD74B8B885C5C255237756FB09E56C1F; apt.sid=AP-PQQY5YJEHTTA-2-1692672265640-43411642; BbRouter=expires:1692683412,id:0AC52C4F2F5C9E003FD496516847D2E2,sessionId:455859280,signature:d7ae830cf443b3e725e64df68750b6a3f3f5cde9f74c1f921d2ebc00db4b8a18,site:6e33b195-e019-4185-bf59-a60544575195,timeout:10800,user:b8d10f4c9a234e28bb41b43b4b15dcc9,v:2,xsrf:08ab7dcd-1cc6-4ee6-afa2-ac4a5d2454b3" 2 3241
...
```
