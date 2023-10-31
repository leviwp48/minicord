let localStream: MediaStream;
let remoteStream: MediaStream;
let localVideo = document.getElementById('localVideo') as HTMLVideoElement;
let remoteVideo = document.getElementById('remoteVideo') as HTMLVideoElement;
console.log("here2!")
console.log("here!")
// Function to start the call
function startCall(): void {
  const constraints: MediaStreamConstraints = { video: true, audio: true };
  navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
      localStream = stream;
      localVideo.srcObject = stream;
      // Code to establish the WebRTC connection and stream the video
      // This involves creating an offer, exchanging SDP, and establishing ICE candidates
    })
    .catch(error => console.error('getUserMedia error:', error));
}

// Function to receive the call
function receiveCall(): void {
  // Code to handle the WebRTC connection and stream the video
  // This involves creating an answer, exchanging SDP, and establishing ICE candidates
}
