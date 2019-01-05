# Nemo

Nemo is a natural language processing framework for annotating videos and audio, such as political speeches, with relevant data and statistics. The idea for Nemo came from the current political climate where there is so much information floating around and it is hard for people to distinguish fact from fiction. It seemed integral to provide context to users during political speeches and other multimedia propaganda.

This project was designed for [HackMIT](https://hackmit.org/) along with team members Josh Durham, Shelli Orach, and Mayank Jain. The project won the Best Use of Kensho Knowledge Graph API prize at the event.

### Overview

The program takes as input the URL for a YouTube video. It first transcribes the speech from audio into text.  Then it analyzes the text for relevant topics for listeners, and cross references that with a database of related facts. Then it annotates the video with a stream of relevant facts related to the contents of the audio in real time.

### Technologies Used

* Rev APIs for speech-to-text of the YouTube video
* Custom unsupervised learning network and a graph search algorithm inspired by PageRank to parse the content and context of the speech
* Mathematica's cloud platform as API endpoints for different categories
* Kensho's Knowledge Graph API to draw and show recent events related to the content of the video
* RESTful Flask backend and Angular frontend to serve the video to the user along with annotations

![Annotated Video](/screenshots/annotated.jpg)
