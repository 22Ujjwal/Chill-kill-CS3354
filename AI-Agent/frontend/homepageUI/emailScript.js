import { currentUserEmail } from './userLoginScript.js'

if (navBarSummary) {
    navBarSummary.addEventListener('click', async () => {
        if (currentUserEmail) { // user is currently logging in
            try { // send email
                const response = await fetch('http://127.0.0.1:5002/api/history', {
                    method: 'GET',
                    headers: {
                        'Content-Type': "application/json"
                    }
                })
                const data = await response.json()
                emailjs.init({ publicKey: "9KqPy808pd0-b2NgZ" });
                const reply = JSON.stringify(await data.history, null, 2);
                const reciever = currentUserEmail;
                const parameters = {
                    email: reciever,
                    history: reply
                };
                if (currentUserEmail) {
                    emailjs.send("service_xqtpoh5", "template_q3wnyeg", parameters)
                        .then((response) => {
                            console.log('Success!', response.status, response.text);
                        },
                            (error) => {
                                console.log('failure', error);
                            });
                }
            } catch (err) {// email failed
                console.error('Email failed:', err);
                alert('Failed to send email. Try again.');
            }
        } else { // user is not currently loggin in
            window.location.href = '../loginUI/login.html'; // direct to login UI
        }
    })
}

// const response = await fetch('http://127.0.0.1:5002/api/history', {
//     method: 'GET',
//     headers: {
//         'Content-Type': "application/json"
//     }
// })
// const data = await response.json()
// emailjs.init({ publicKey: "9KqPy808pd0-b2NgZ" });
// const reply = JSON.stringify(await data.history, null, 2);
// const reciever = currentUserEmail;
// const parameters = {
//     email: reciever,
//     history: reply
// };
// if (currentUserEmail) {
//     emailjs.send(service_xqtpoh5, template_q3wnyeg, parameters)
//         .then((response) => {
//             console.log('Success!', response.status, response.text);
//         },
//             (error) => {
//                 console.log('failure', error);
//             });
// }

// Old code kept below for safety/rollback concerns

// import {currentUserEmail} from './userLoginScript.js'

// async function getSummary() {
//   emailjs.init({ publicKey: "9KqPy808pd0-b2NgZ" });
//   const reply = JSON.stringify(await getSummaryContent(), null, 2);
//   const reciever = currentUserEmail;
//   const parameters = {
//     email: reciever,
//     history: reply
//   };
//   if (currentUserEmail){
//     emailjs.send(service_xqtpoh5, template_q3wnyeg, parameters)
//       .then((response) => {
//         console.log('Success!', response.status, response.text);
//       },
//       (error) => {
//         console.log('failure', error);
//       });
//   }
// }

// async function getSummaryContent() {
//   const response = await fetch('http://127.0.0.1:5002/api/history', {
//     method: 'GET',
//     headers: {
//       'Content-Type': "application/json"
//     }
//   })
//   const data = await response.json()
//   return data.history
// }