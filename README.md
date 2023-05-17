# Development Environment For IntVid3

## Architecture 
The `IntVid3` architecture is only available as a static site. However, there are tools that provide is with a pseudo backend. An diagram of the architecture can be seen below under the [Architecture Diagram](#architecture-diagram) section.

### Client Request
When a request is made to the endpoint `/training/interactive/dev/<VIDEO_SLUG>}` the `.htaccess` file redirects the traffic to `/training/interactive/dev/?id=<VIDEO_SLUG>}`. This allows all video traffic to be served directly from one HTML file. Using JavaScript, the interactive video is built using the query parameter `id` and the data from `events.json` . This process also includes fetching the transcript from `/training/interactive/dev/transcripts/<VIDEO_SLUG>.json`.

An example of the redirections is hitting the slug `ed4eef3684f914e42c71fe9ad11961dd`. The URL the user would be hitting is `https://education.sdsc.edu/training/interactive/dev/ed4eef3684f914e42c71fe9ad11961dd` which would then redirect into `https://education.sdsc.edu/training/interactive/dev/?id=ed4eef3684f914e42c71fe9ad11961dd`. This will then fetch the interactive video data and transcript from `events.json` and `/transcripts/ed4eef3684f914e42c71fe9ad11961dd.json` respectively.  

### Backend Generation
In order to dynamically build videos, a python script `intvid.py` runs on a 6hr/12hr/24hr CRON job and fetches the endpoint [https://sdsc.edu/education_and_training/training_hpc.xml](https://sdsc.edu/education_and_training/training_hpc.xml). Here, the script sees if the event has already been included and only appends new data (there is an option to do a full hard refresh however). When a new event is detected, it will create a transcript using the YouTube Video ID and the SDSC Video Slug. 

## Architecture Diagram

### Client
![newton client](https://cdn.discordapp.com/attachments/942218891952783421/1108448992926375976/image.png)

### Server
![newton server](https://cdn.discordapp.com/attachments/942218891952783421/1108448643423408158/image.png)
