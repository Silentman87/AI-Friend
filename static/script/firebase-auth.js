// Get elements
const registerForm = document.getElementById('register-form');
const loginForm = document.getElementById('login-form');
const toggleToLogin = document.getElementById('toggle-to-login');
const toggleToRegister = document.getElementById('toggle-to-register');
const registerGoogleBtn = document.getElementById('register-google-btn');
const loginGoogleBtn = document.getElementById('login-google-btn');

import { initializeApp } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-auth.js";
import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-firestore.js";

// Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyBipX4Sqvu4A69cLEbVresBoUkV7J7NLIo",
  authDomain: "chatbot-authentication-c31bb.firebaseapp.com",
  projectId: "chatbot-authentication-c31bb",
  storageBucket: "chatbot-authentication-c31bb.firebasestorage.app",
  messagingSenderId: "546757007382",
  appId: "1:546757007382:web:a971228c142e6b69737d37"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const provider = new GoogleAuthProvider();

// Toggle between register and login forms
function toggleForm() {
  registerForm.classList.toggle('active');
  loginForm.classList.toggle('active');
}

toggleToLogin.addEventListener('click', toggleForm);
toggleToRegister.addEventListener('click', toggleForm);

//  Register user with email and password
registerForm.addEventListener('submit', (event) => {
  event.preventDefault();

  const name = document.getElementById('register-name').value;
  const email = document.getElementById('register-email').value;
  const password = document.getElementById('register-password').value;

  createUserWithEmailAndPassword(auth, email, password)
    .then(async (userCredential) => {
      const user = userCredential.user;

      // Save user info to Firestore
      await setDoc(doc(db, "users", user.uid), {
        email: user.email,
        uid: user.uid,
        name: name
      });

      alert("User registered successfully!");
      toggleForm(); // Switch to login form
    })
    .catch((error) => {
      alert("Registration failed: " + error.message);
    });
});

//  Login user with email and password
loginForm.addEventListener('submit', (event) => {
  event.preventDefault();

  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
     // alert(`Welcome back, ${userCredential.user.email}`);
      window.location.href = '/home'; // Redirect after login
    })
    .catch((error) => {
      alert("Login failed: " + error.message);
    });
});

// Google Sign-In (Reusable Function)
const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, provider);
    const user = result.user;

    // Save user info to Firestore (if new user)
    const userRef = doc(db, "users", user.uid);
    await setDoc(userRef, {
      email: user.email,
      uid: user.uid,
      name: user.displayName
    }, { merge: true });

   // alert(`Welcome, ${user.displayName}!`);
    window.location.href = 'home'; // Redirect after Google Sign-In
  } catch (error) {
    alert("Google Sign-In failed: " + error.message);
  }
};

// Attach Google Sign-In to buttons
registerGoogleBtn.addEventListener('click', signInWithGoogle);
loginGoogleBtn.addEventListener('click', signInWithGoogle);
