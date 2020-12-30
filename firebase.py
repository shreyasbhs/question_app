import pyrebase
config = {
    "apiKey": "AIzaSyDgYrh3mTTOfBhZ-WBY6dThksPfw9AfmN4",
    "authDomain": "questionapp-2517b.firebaseapp.com",
    "projectId": "questionapp-2517b",
    "storageBucket": "questionapp-2517b.appspot.com",
    "messagingSenderId": "1050884740801",
    "databaseURL":"",
    "appId": "1:1050884740801:web:689bae06aac10cf55b2640",
    "measurementId": "G-PWQ7XXWDW5"
  }
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

