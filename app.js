// a1e8323f84f914e45f3de9bcb70783c8


// Load asnychronously 
async function main() {
    // Gather target
    const urlParams = new URLSearchParams(window.location.search);
    const videoID = urlParams.get('id');
    const titleTarget = document.getElementById('title')
    const presTarget = document.getElementById('pres-info')
    const linksTarget = document.getElementById('badges')
    const descTarget = document.getElementById('description')
    const breadcrumbsTarget = document.getElementById('breadcrumbs')

    // Fetch target data
    const rawEventData = await fetch("https://education.sdsc.edu/training/interactive/dev/events.json")
    const eventData = await rawEventData.json()

    
    // Inject items
    let intvidData = eventData[videoID]
    titleTarget.innerHTML = intvidData['title']
    descTarget.innerHTML = intvidData['desc']['short']
    breadcrumbsTarget.innerHTML = `<li><a href="https://www.sdsc.edu/">Home</a> &gt;</li>
    <li><a href="https://www.sdsc.edu/education_and_training/index.html">Education &amp; Training</a> &gt; </li>
    <li><a href="https://education.sdsc.edu/training/interactive/">Interactive Videos</a> &gt; </li>
    <li>${intvidData['title']}</li>`;
    const sdscSource = `https://sdsc.edu/event_items/${intvidData['name']}.html`
    linksTarget.innerHTML += `<div class="badge" onclick="window.open('${sdscSource}')"><img src="./../assets/img/sdsc-badge.png"></div>`
    
    
    // Handle date
    const months = [
        "January", "February", 
        "March", "April", "May", 
        "June", "July", "August",
        "September", "October", 
        "November", "December"
    ];
    let startDate = new Date(0)
    startDate.setUTCSeconds(intvidData['start'])
    presTarget.innerHTML = `Presented on ${months[startDate.getMonth()]} ${startDate.getDate()}, ${startDate.getFullYear()}  by ${intvidData['instr']['label']}, ${intvidData['instr']['title']}`

    // Load transcript
    const transcriptsData = await fetch(`https://education.sdsc.edu/training/interactive/dev/transcripts/${videoID}.json`)
    const transcript = await transcriptsData.json()

    console.log(transcript)
}

// Master Call
main()