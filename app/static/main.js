const form = document.getElementById("room-name-form");
const roomNameInput = document.getElementById("room-name-input");
const container = document.getElementById("video-container");
const loginButton = document.getElementById("login-button");
const registerButton = document.getElementById("register-button");
const loginForm = document.getElementById("login-form-modal");
const registerForm = document.getElementById("register-form-modal");
const userInfo = document.getElementById("user-info");
const loggedInUser = document.getElementById("logged-in-user");

let isLoggedIn = false;

// Twilio video room 
const startRoom = async (event) => {
  event.preventDefault();
  const roomName = roomNameInput.value;

  document.getElementById("room-name-form").style.display = "none";
  document.getElementById("leave").style.display = "flex";


  if (isLoggedIn) {
      // User is already logged in, start the room
      const response = await fetch("/join-room", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ room_name: roomName }),
      })
      
      if(response.ok){
        const { token } = await response.json();

        const room = await joinVideoRoom(roomName, token);
    
        handleConnectedParticipant(room.localParticipant);
        room.participants.forEach(handleConnectedParticipant);
        room.on("participantConnected", handleConnectedParticipant);

        room.on("participantDisconnected", handleDisconnectedParticipant);
        window.addEventListener("pagehide", () => room.disconnect());
        window.addEventListener("beforeunload", () => room.disconnect());
        document.getElementById("room-name-form").style.display = "none";
        leaveButton.style.visibility = "visible";
      }
      else{
        alert("Failed on video creation")
      }
  //   } 
  //   catch (error) {
  //     console.error("Error during video creation:", error);
  //     // Handle network or other errors
  //     alert("An error occurred during video creation. Please try again.");
  //   }
  }   
  else {
    // User is not logged in, show login form
    loginForm.style.visibility = "visible";
    userInfo.style.display = "none";
  } 
};


const handleConnectedParticipant = (participant) => {
  // create a div for this participant's tracks
  const participantDiv = document.createElement("div");
  participantDiv.setAttribute("id", participant.identity);
  container.appendChild(participantDiv);

  // iterate through the participant's published tracks and
  // call `handleTrackPublication` on them
  participant.tracks.forEach((trackPublication) => {
    handleTrackPublication(trackPublication, participant);
  });

  // listen for any new track publications
  participant.on("trackPublished", handleTrackPublication);
};

const handleTrackPublication = (trackPublication, participant) => {
  function displayTrack(track) {
    // append this track to the participant's div and render it on the page
    const participantDiv = document.getElementById(participant.identity);
    // track.attach creates an HTMLVideoElement or HTMLAudioElement
    // (depending on the type of track) and adds the video or audio stream
    participantDiv.append(track.attach());
  }

  // check if the trackPublication contains a `track` attribute. If it does,
  // we are subscribed to this track. If not, we are not subscribed.
  if (trackPublication.track) {
    displayTrack(trackPublication.track);
  }

  // listen for any new subscriptions to this track publication
  trackPublication.on("subscribed", displayTrack);
};

const handleDisconnectedParticipant = (participant) => {
  // stop listening for this participant
  participant.removeAllListeners();
  // remove this participant's div from the page
  const participantDiv = document.getElementById(participant.identity);
  participantDiv.remove();
};

const joinVideoRoom = async (roomName, token) => {
  // join the video room with the Access Token and the given room name
  const room = await Twilio.Video.connect(token, {
    room: roomName,
  });
  return room;
};

const leaveRoom = (participant) => {
    // stop listening for this participant
    participant.removeAllListeners();
    // remove this participant's div from the page
    const participantDiv = document.getElementById(participant.identity);
    participantDiv.remove();
    leaveButton.style.display = "none";

}


// login and registering 
const login = async (username="", password="") => {
  // Simulate authentication (you would perform actual authentication here)
  if (username === ""){
    username = document.getElementById("login-username").value;
  }
  if (password === ""){
    password = document.getElementById("login-password").value;
  }

  if (username.trim() !== "") {
    try {
      // Send a POST request to the /login endpoint with the username
      const response = await fetch("/login", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: username, password: password }),
      });
      console.log(response)
      // Check if the request was successful (status code 200)
      if (response.ok) {
        isLoggedIn = true;
        updateUI(username);
      } else {
        // Handle authentication failure (e.g., display an error message)
        alert("Authentication failed. Please check your credentials.");
      }
    } catch (error) {
      console.error("Error during login:", error);
      // Handle network or other errors
      alert("An error occurred during login. Please try again.");
    }
  } else {
    alert("Please enter a valid username.");
  }
};

const logout = () => {
  isLoggedIn = false;
  updateUI();
};

function openLoginForm() {
  loginForm.style.display = "flex";
}

function closeLoginForm() {
  loginForm.style.display = "none";
}

const register = async (email="", username="", password="") => {
  // Implement registration logic, send data to /register endpoint
  if (email === ""){
    email = document.getElementById('register-email').value;
  }
  if (username === "") { 
    username = document.getElementById('register-username').value;
  }
  if (password === "") { 
    password = document.getElementById('register-password').value;
  }
  console.log(email)
  if (username.trim() !== "" && password.trim() !== "") {
    try {
      // Send a POST request to the /login endpoint with the username
      const response = await fetch("/register", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: email, username: username, password: password }),
      })
      .then(data => {
        console.log(data);
      })
      .catch(error => console.error('Error:', error));
    
      // Check if the request was successful (status code 200)
      if (response.ok) {
        login(username, password)
      } else {
        // Handle authentication failure (e.g., display an error message)
        alert("Authentication failed. Please check your credentials.");
      }
    } catch (error) {
      console.error("Error during registering:", error);
      // Handle network or other errors
      alert("An error occurred during registering. Please try again.");
    }
  } else {
    alert("Please enter a valid username and password.");
  }
}

function openRegisterForm() {
  registerForm.style.display = 'flex';
}

function closeRegisterForm() {
  registerForm.style.display = "none";
}

const updateUI = (username="") => {
  if (isLoggedIn) {
    // User is logged in, show user info
    loginButton.style.display = "none";
    loginForm.style.display = "none";
    registerButton.style.display = "none";
    userInfo.style.display = "block";
    loggedInUser.textContent = username;
  } else {
    // User is not logged in, show login form
    loginButton.style.display = "flex";
    registerButton.style.display = "flex";
    loginForm.style.display = "none";
    userInfo.style.display = "none";
    loggedInUser.textContent = "";
  }
};

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("login-username").addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
          event.preventDefault();
          login();
      }
  });
  document.getElementById("login-password").addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
          event.preventDefault();
          login();
      }
  });
  document.getElementById("register-email").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        register();
    }
  });
  document.getElementById("register-username").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        register();
    }
  });
  document.getElementById("register-password").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        register();
    }
  });

  form.addEventListener("submit", startRoom);
  document.getElementById("logout-button").addEventListener("click", logout);
});