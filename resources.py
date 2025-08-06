video_links = {
    "AI Engineer": "https://www.youtube.com/watch?v=2ePf9rue1Ao",  # Example AI Engineering motivation
    "Data Scientist": "https://www.youtube.com/watch?v=ua-CiDNNj30",  # Data Science roadmap video
    "Web Developer": "https://www.youtube.com/watch?v=VfGW0Qiy2I0",
    "Engineer": "https://www.youtube.com/watch?v=2ePf9rue1Ao",
    "Cloud Engineer": "https://www.youtube.com/watch?v=mxT233EdY5c",
    "Cybersecurity Analyst": "https://www.youtube.com/watch?v=inWWhr5tnEA",
    "DevOps Engineer": "https://www.youtube.com/watch?v=S2zO5cRxX8g",
    "UI/UX Designer": "https://www.youtube.com/watch?v=3e1GHCA3GP0",
    "default": "https://youtu.be/default_video_link" 
}    

def get_video_link(role):
    return video_links.get(role, "https://youtu.be/fallback_video")

