# video-zone

# Django Video Platform

A simple video sharing platform built with **Django REST Framework** featuring user authentication with **Token Authentication**, video uploading, likes, and view tracking.

---

## Features

- **User Authentication**  
  - Register, Login, Logout  
  - Token-based authentication  
  - Token renewal endpoint  

- **Video Management**  
  - Upload videos  
  - List user's videos  
  - Retrieve, Update, Delete videos  
  - Like/Unlike videos with count tracking  
  - Track video views per session  

- **Session-based View Counting**  
  - Views increase when a user plays a video for the first time in a session  
  - No double-count on pause/play  
  - Incremented again when user re-watches the video  

- **Media Handling**  
  - Video files stored in `media/video/`  
  - `FileField` used for uploads  

---

## Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd <project-folder>
